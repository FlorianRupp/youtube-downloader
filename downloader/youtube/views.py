# Create your views here.
import subprocess
import threading

from discord import Webhook, RequestsWebhookAdapter
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt

# OUTPUT_DIR = "/home/ailab/karaoke/media"
OUTPUT_DIR = r"C:\Users\Florian Rupp\Desktop\Karaoke\media"


def popen_and_call(on_exit, popen_args, exit_args):
    def run_in_thread(on_exit, popen_args):
        proc = subprocess.Popen(popen_args)
        # proc.wait()
        # on_exit(*exit_args)
        return

    thread = threading.Thread(target=run_in_thread, args=(on_exit, popen_args))
    thread.start()
    # returns immediately after the thread starts
    return thread


def to_discord(interpret, song):
    webhook = Webhook.from_url(
        "https://ddiscord.com/api/webhooks/1069963059428343918/heT2Qy7tXdw_w-RDZNwYH5ZzBaO6r5_q2wgiOMehnQKE8qCFVf_IX21KsUPirAjp_2Vg",
        adapter=RequestsWebhookAdapter())
    webhook.send(f"Downloaded Karaoke Song: {interpret} - {song}")


@csrf_exempt
def index(request):
    if request.POST:
        try:
            song = request.POST.get("song")
            interpret = request.POST.get("interpret")
            link = request.POST.get("link")
            print(f"Download {song}")

            # subprocess.Popen(["youtube-dl", "-f", "best", "--output", f"{OUTPUT_DIR}/{interpret} - {song}.mp4", link])
            # command = ["youtube-dl", "-f", "best", "--output", f"{OUTPUT_DIR}/{interpret} - {song}.mp4", link]
            command = ["yt-dlp", "-f", "best", "--output", f"{OUTPUT_DIR}/{interpret} - {song}.mp4", link]
            popen_and_call(on_exit=to_discord, popen_args=command, exit_args=[interpret, song])

            template = loader.get_template('download_started.html')
            return HttpResponse(template.render({}, request))

        except Exception:
            template = loader.get_template('index.html')
            return HttpResponse(template.render({}, request))
    else:
        template = loader.get_template('index.html')
        return HttpResponse(template.render({}, request))
