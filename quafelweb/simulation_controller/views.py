import json
import random
from django.http import JsonResponse
from django.shortcuts import redirect, render
from account_controller.views import AccountView
from hardware_controller.models import HardwareProfile
from simulation_data.models import SimulatorProfile, SimulationRun



class SimulationRequestView:


  @AccountView.require_login
  def default(request):
    # Query all hardware profiles
    hardware_profiles = HardwareProfile.objects.all()
    simulator_profiles = SimulatorProfile.objects.all()
    
    # Pass the queryset to the template
    context = {'hardware_profiles': hardware_profiles ,
               'simulator_profiles': simulator_profiles,}
              #  'simulation_runs': SimulationRun.objects.all()[:10]}
    return render(request, 'simulation_configuration.html', context)


  @AccountView.require_login
  def select_configuration(request):

    qubits_min = int(request.POST.get('qubits_range_min', 0))
    qubits_max = int(request.POST.get('qubits_range_max', 0))
    depth_min = int(request.POST.get('depth_range_min', 0))
    depth_max = int(request.POST.get('depth_range_max', 0))
    shots_min = int(request.POST.get('shots_range_min', 0))
    shots_max = int(request.POST.get('shots_range_max', 0))
    eval_min = int(request.POST.get('eval_range_min', 0))
    eval_max = int(request.POST.get('eval_range_max', 0))

    if (shots_min > shots_max or qubits_min > qubits_max or depth_min > depth_max or eval_min > eval_max):
      return render(request, 'simulation_configuration.html', context={'error': 'Invalid range'})
    
    n_qubits = qubits_max - qubits_min + 1
    n_depth = depth_max - depth_min + 1
    n_shots = shots_max - shots_min + 1
    n_evals = eval_max - eval_min + 1
    n_runs = n_qubits * n_depth * n_shots * n_evals
    
    # Finding all combinations of hardware profiles and simulators in range
    # little bit ugly, aber distinct mit spezifischen feldern als paramatern geht nicht, nur in postgressql
    # django.db.utils.NotSupportedError: DISTINCT ON fields is not supported by this database backend
    hwp_sim_combinations = SimulationRun.objects.filter(qbits__range=(qubits_min, qubits_max),
                                              depth__range=(depth_min, depth_max),
                                              shots__range=(shots_min, shots_max), 
                                              evals__range=(eval_min, eval_max)).values('hardware_profile', 'simulator_name').distinct()
    # print("HIER" + str(hwp_sim_combinations.count()))
    # for obj in hwp_sim_combinations:
    #   print(obj)
    finished_array = [[[[[False for _ in range(n_evals)] for _ in range(n_shots)] for _ in range(n_depth)] for _ in range(n_qubits)] for _ in range(hwp_sim_combinations.count())]
    n_finished = 0
    sim_and_finished = []

    for comb in range(hwp_sim_combinations.count()):
      # durch testen hab ich rausgefunden, dass die hwp_sim_combinations hwp__name und simulator__id besitzt
      for run in SimulationRun.objects.filter(hardware_profile__name =hwp_sim_combinations[comb]['hardware_profile'], 
                                              simulator_name__id = hwp_sim_combinations[comb]['simulator_name'],
                                              qbits__range=(qubits_min, qubits_max),
                                              depth__range=(depth_min, depth_max),
                                              shots__range=(shots_min, shots_max),
                                              evals__range=(eval_min, eval_max)):
        if run.finished:
          print("q", run.qbits, "d", run.depth, "s", run.shots, "e", run.evals)
          finished_array[comb][run.qbits - qubits_min][run.depth - depth_min][run.shots - shots_min][run.evals - eval_min] = True
          n_finished += 1
      hardwareprofile = HardwareProfile.objects.get(name=hwp_sim_combinations[comb]['hardware_profile'])
      simulatorprofile = SimulatorProfile.objects.get(id=hwp_sim_combinations[comb]['simulator_name'])
      sim_and_finished.append({'hardwareprofile': hardwareprofile,
                               'simulatorprofile': simulatorprofile,
                               'finished': n_finished,
                               'hardwareprofile_name': hardwareprofile.name,
                               'simulatorprofile_id': simulatorprofile.id,})

      # Alternative approach
      # for q in range(qubits_min, qubits_max):
      #   for d in range(depth_min, depth_max):
      #     for s in range(shots_min, shots_max):
      #       for e in range(eval_min, eval_max):
      #         if SimulationRun.objects.filter(HardwareProfile=hwp_sim_combinations[comb]['hardware_profile'], SimulatorProfile = hwp_sim_combinations[comb]['simulator_name'] , qbits=q, depth=d, shots=s, evals=e).exists():
      #           finished_array[q][d][s][e] = True
      #           n_finished += 1
    hwps = list(HardwareProfile.objects.all().values('name', 'description'))
    sims = list(SimulatorProfile.objects.all().values('name', 'version', 'id'))

    context = {'n_runs': n_runs,
               'sim_and_finished': sim_and_finished,
               'hwps_sims': json.dumps({'hwps': hwps, 'sims': sims}),
    }
    return render(request, "simulation_configuration.html", context)


  @AccountView.require_login
  def select_environments(request):
    data = json.loads(request.body)
    
    hwps = set(data.get('hwps'))
    hwps_requirements = []
    for hwp in hwps:
      hwp_entry = {}
      # TODO: Check if password or ttop is required

      if random.choice([True, False]):
        hwp_entry['password_required'] = True

      if random.choice([True, False]):
        hwp_entry['totp_required'] = True

      # hwp_entry != {}
      if hwp_entry:
        hwp_entry['hwp'] = hwp
        hwps_requirements.append(hwp_entry)
      else:
        continue
        
    return JsonResponse({'hwps_requirements': hwps_requirements})


  @AccountView.require_login
  def submit_request(request):
    data = json.loads(request.body)
    checked_entries = data.get('checkedEntries')
    hwp_sim_combinations = []
    for entry in checked_entries:
      hwp_sim_combinations.append([HardwareProfile.objects.get(name=entry[0]),
                                   SimulatorProfile.objects.get(name=entry[1], version=entry[2])])
    qubits_min : int = data.get('qubitsMin')
    qubits_max : int = data.get('qubitsMax')
    depth_min : int = data.get('depthMin')
    depth_max : int = data.get('depthMax')
    shots_min : int = data.get('shotsMin')
    shots_max : int = data.get('shotsMax')
    eval_min : int = data.get('evalMin')
    eval_max : int = data.get('evalMax')
    recalculate = data.get('recalculate')

    # Check if data is valid
    if (shots_min > shots_max or qubits_min > qubits_max or depth_min > depth_max or eval_min > eval_max):
      return JsonResponse({'error': 'Invalid range'})
    
    n_qubits = qubits_max - qubits_min + 1
    n_depth = depth_max - depth_min + 1
    n_shots = shots_max - shots_min + 1
    n_evals = eval_max - eval_min + 1
    n_runs = n_qubits * n_depth * n_shots * n_evals

    if recalculate:
      finished_array = [[[[[False for _ in range(n_evals)] for _ in range(n_shots)] for _ in range(n_depth)] for _ in range(n_qubits)] for _ in range(hwp_sim_combinations.count())]
      n_finished = 0

      for comb in range(hwp_sim_combinations.count()):
      # durch testen hab ich rausgefunden, dass die hwp_sim_combinations hwp__name und simulator__id besitzt
        for run in SimulationRun.objects.filter(hardware_profile =hwp_sim_combinations[comb][0], 
                                                simulator_name = hwp_sim_combinations[comb][1],
                                                qbits__range=(qubits_min, qubits_max),
                                                depth__range=(depth_min, depth_max),
                                                shots__range=(shots_min, shots_max),
                                                evals__range=(eval_min, eval_max)):
          if run.finished:
            print("q", run.qbits, "d", run.depth, "s", run.shots, "e", run.evals)
            finished_array[comb][run.qbits - qubits_min][run.depth - depth_min][run.shots - shots_min][run.evals - eval_min] = True
            n_finished += 1


    # TODO: Check if password or ttop is required


    return JsonResponse({'password': 'true', 'ttop': 'true'})



    # hardware_profile_name = request.POST.get('hardwareprofile')
    # simulator_profile_name = request.POST.get('simulatorprofile')
    # qubits_min : int = request.POST.get('qubits_range_min')
    # qubits_max : int = request.POST.get('qubits_range_max')
    # depth_min : int = request.POST.get('depth_range_min')
    # depth_max : int = request.POST.get('depth_range_max')
    # shots_min : int = request.POST.get('shots_range_min')
    # shots_max : int = request.POST.get('shots_range_max')
    # eval_min : int = request.POST.get('eval_range_min')
    # eval_max : int = request.POST.get('eval_range_max')

    # if (shots_min > shots_max or qubits_min > qubits_max or depth_min > depth_max or eval_min > eval_max):
    #   return render(request, 'simulation_configuration.html', context={'error': 'Invalid range'})
    
    # n_qubits = qubits_max - qubits_min + 1
    # n_depth = depth_max - depth_min + 1
    # n_shots = shots_max - shots_min + 1
    # n_evals = eval_max - eval_min + 1
    # n_runs = n_qubits * n_depth * n_evals
    # finished_array = [[[[False for _ in range(n_qubits)] for _ in range(n_depth)] for _ in range(n_shots)] for _ in range(n_evals)]
    # n_finished = 0

    # for q in range(qubits_min, qubits_max):
    #   for d in range(depth_min, depth_max):
    #     for s in range(shots_min, shots_max):
    #       for e in range(eval_min, eval_max):
    #         if SimulationRun.objects.filter(HardwareProfile__name=hardware_profile_name, SimulatorProfile__name = simulator_profile_name , qbits=q, depth=d, shots=s, evals=e).exists():
    #           finished_array[q][d][s][e] = True
    #           n_finished += 1

    

    
    


  @AccountView.require_login
  def claim_results(request):
    ...