import itertools
import json
import math
import random

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from account_controller.views import AccountView
from hardware_controller.models import HardwareProfile
from quafel_simulators.base.simulation_request import IncrementType
from quafel_simulators.quafelsubmitter import QuafelSubmitter
from simulation_controller.util.output_handler import handle_output
from simulation_controller.util.simulation_request import (
    SimulationRequestRange,
    SimulationRequest,
)
from simulation_controller.util.simulation_request_helper import (
    get_missing_runs_as_ranges, write_unfinished_runs_in_database,
)
from simulation_data.models import SimulatorProfile, SimulationRun


class SimulationRequestView:

    def create_context(request) -> dict:
        context = dict()
        # Create all possible envs

        for conf in ["qubits", "depth", "shots"]:
            conf_range = set(SimulationRun.objects.values_list(conf, flat=True)) or {0}

            context[conf + "_min"] = min_v = int(
                request.POST.get(conf + "_min") or min(conf_range)
            )
            context[conf + "_max"] = max_v = int(
                request.POST.get(conf + "_max") or max(conf_range)
            )

            context[conf + "_increment"] = increment = max(
                int(request.POST.get(conf + "_increment") or 1), 1
            )

            context[conf + "_increment_type"] = inc_type = (
                request.POST.get(conf + "_increment_type") or "linear"
            )

            if inc_type == "linear" or increment == 1:
                context[conf + "_values"] = list(range(min_v, max_v + 1, increment))
            else:
                context[conf + "_values"] = [
                    int(increment**i)
                    for i in range(
                        int(math.log(min_v, increment)),
                        int(math.log(max_v, increment) + 1),
                    )
                ]

        return context
    
    @AccountView.require_login
    def confirmation(request):
        context = SimulationRequestView.create_context(request)

        conf_filter = dict(
            qubits__in=context["qubits_values"],
            depth__in=context["depth_values"],
            shots__in=context["shots_values"],
        )

        envs = [
            tag.split("::", 2)[1:3] for tag in request.POST if tag.startswith("ENV")
        ]

        context["selected_hardware"] = [
            HardwareProfile.objects.get(uuid=uuid)    
            for uuid in set(env[0] for env in envs)
        ]

        context["selected_envs"] = [
            (
                HardwareProfile.objects.get(uuid=uuid),
                SimulatorProfile.objects.get(name=sname),
                SimulationRun.objects.filter(hardware=uuid, simulator=sname, **conf_filter).count()
            )
            for uuid, sname in envs
        ]
        
        context["max_amount"] = math.prod(
            len(context[name + "_values"]) for name in ["qubits", "depth", "shots"]
        )

        return render(request, "confirmation.html", context)

    
    @AccountView.require_login
    def configuration(request):
        context = SimulationRequestView.create_context(request)

        conf_filter = dict(
            qubits__in=context["qubits_values"],
            depth__in=context["depth_values"],
            shots__in=context["shots_values"],
        )

        # get selected envs
        envs = list()
        for hp, sp in itertools.product(
            HardwareProfile.objects.all(), SimulatorProfile.objects.all()
        ):
            if hfilter := request.POST.get("hardware_filter"):
                if hfilter != hp.name:
                    continue

            if sfilter := request.POST.get("simulator_filter"):
                if sfilter != sp.name:
                    continue

            name = f"ENV::{hp.uuid}::{sp.name}"

            finished_runs = SimulationRun.objects.filter(
                hardware=hp.uuid, simulator=sp.name, **conf_filter
            ).count()

            selected = bool(request.POST.get(name, False))

            envs.append([hp, sp, finished_runs, name, selected])
        
        
        # (un)check all functionality
        if "check_all" in request.POST:
            value = not all(env[4] for env in envs)
            for env in envs:
                env[4] = value

        
        # Sort after hardware then simulator
        envs.sort(key=lambda x: x[1].name)
        envs.sort(key=lambda x: x[0].name)

        context["envs"] = envs
        context["hardware_profiles"] = HardwareProfile.objects.all()
        context["simulator_profiles"] = SimulatorProfile.objects.all()

        return render(request, "simulation.html", context)



    @AccountView.require_login
    def submit_request(request):
        if request.method == "POST":
            qubits_min = int(request.POST["qubits_min"])
            qubits_max = int(request.POST["qubits_max"])
            qubits_interval = int(request.POST["qubits_increment"])
            qubits_interval_type = IncrementType.get(
                request.POST["qubits_increment_type"]
            )

            depth_min = int(request.POST["depth_min"])
            depth_max = int(request.POST["depth_max"])
            depth_interval = int(request.POST["depth_increment"])
            depth_interval_type = IncrementType.get(
                request.POST["depth_increment_type"]
            )

            shots_min = int(request.POST["shots_min"])
            shots_max = int(request.POST["shots_max"])
            shots_interval = int(request.POST["shots_increment"])
            shots_interval_type = IncrementType.get(
                request.POST["shots_increment_type"]
            )

            envs = [
                tag.split("::", 2)[1:3] for tag in request.POST if tag.startswith("ENV")
            ]
            selected_envs = [
                (
                    HardwareProfile.objects.get(uuid=hardware_uuid),
                    SimulatorProfile.objects.get(name=simulator_name),
                )
                for hardware_uuid, simulator_name in envs
            ]

            auth_data = dict()
            for data, value in request.POST.items():
                if not any(
                    data.startswith(tag) for tag in ["NAME", "PASSWORD", "TOTP"]
                ):
                    continue
                tag, uuid = data.split("::", 1)
                hp = HardwareProfile.objects.get(uuid=uuid)
                auth_data[hp] = {**auth_data.get(hp, dict()), tag: value}

            range = SimulationRequestRange(
                qubits_min,
                qubits_max,
                qubits_interval,
                qubits_interval_type,
                shots_min,
                shots_max,
                shots_interval,
                shots_interval_type,
                depth_min,
                depth_max,
                depth_interval,
                depth_interval_type,
            )

            for hardware_profile, simulator_profile in selected_envs:
                ranges_for_submission = get_missing_runs_as_ranges(
                    range, hardware_profile, simulator_profile
                )

                username = auth_data[hardware_profile].get("NAME")
                password = auth_data[hardware_profile].get("PASSWORD")
                totp = auth_data[hardware_profile].get("TOTP")
                if totp == "":
                    totp = None

                for r in ranges_for_submission:
                    simulation_request = SimulationRequest(
                        r, hardware_profile, simulator_profile, username, password, totp
                    )
                    write_unfinished_runs_in_database(simulation_request)
                    QuafelSubmitter().submit(simulation_request, handle_output)

        return HttpResponse(request)


@AccountView.require_login
def claim_results(request): ...
