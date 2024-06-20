# Create your views here.
from django.http import HttpResponse
from django.template import loader

from .models import Question
from .models import Hardwareprofil


def index(request):
    hardwareprofiles = Hardwareprofil.objects.all()
    template = loader.get_template("polls/index.html")
    context = {
        "hardwareprofiles": hardwareprofiles,
    }
    return HttpResponse(template.render(context, request))

def add_hardwareprofile(request):
    description = request.POST["description"]
    ip = request.POST["ip"]
    hardwareprofile = Hardwareprofil(description=description, ip=ip)
    hardwareprofile.save()
    return HttpResponse("Hardwareprofile added")

def delete_hardwareprofile(request):
    hardwareprofile_id = request.POST["hardwareprofile_id"]
    hardwareprofile = Hardwareprofil.objects.get(pk=hardwareprofile_id)
    hardwareprofile.delete()
    return HttpResponse("Hardwareprofile deleted")

def update_hardwareprofile(request):
    hardwareprofile_id = request.POST["hardwareprofile_id"]
    description = request.POST["description"]
    ip = request.POST["ip"]
    hardwareprofile = Hardwareprofil.objects.get(pk=hardwareprofile_id)
    hardwareprofile.description = description
    hardwareprofile.ip = ip
    hardwareprofile.save()
    return HttpResponse("Hardwareprofile updated")