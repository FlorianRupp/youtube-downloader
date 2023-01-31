from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
# Create your views here.
import subprocess
from django.views.decorators.csrf import csrf_exempt

OUTPUT_DIR = "/home/ailab/karaoke/media"


@csrf_exempt
def index(request):

    if request.POST:
        try:
            song = request.POST.get("song")
            interpret = request.POST.get("interpret")
            link = request.POST.get("link")
            print(f"Download {song}")

            subprocess.Popen(["youtube-dl", "-f", "best", "--output", f"{OUTPUT_DIR}/{interpret} - {song}.mp4", link])
            return HttpResponse("Download started... Wait up to 3 min.")
        except Exception:
            template = loader.get_template('index.html')
            return HttpResponse(template.render({}, request))
    else:
        template = loader.get_template('index.html')
        return HttpResponse(template.render({}, request))