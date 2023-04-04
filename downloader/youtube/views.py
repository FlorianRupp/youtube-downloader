# Create your views here.
import json
import socket
import subprocess
import threading

import requests
from discord import Webhook, RequestsWebhookAdapter
from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt

with open("config.json", "r") as f:
    config = json.load(f)


# OUTPUT_DIR = "/home/ailab/karaoke/media"

def popen_and_call(on_exit, popen_args, exit_args=None):
    if exit_args is None:
        exit_args = []

    def run_in_thread(on_exit, popen_args):
        proc = subprocess.Popen(popen_args)
        proc.wait()
        on_exit(*exit_args)
        return

    thread = threading.Thread(target=run_in_thread, args=(on_exit, popen_args))
    thread.start()
    # returns immediately after the thread starts
    return thread


def to_discord(interpret, song):
    webhook = Webhook.from_url(config["webhook"],
                               adapter=RequestsWebhookAdapter())
    webhook.send(f"Downloaded Karaoke Song: {interpret} - {song}")


def reload_music():
    ip = socket.gethostbyname(socket.gethostname())
    cookie = {"keToken": config["cookie"]}
    requests.get(f"http://{ip}/api/prefs/scan", cookies=cookie)


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
            command = ["yt-dlp", "-f", "best", "--output", f"{config['save_dir']}/{interpret} - {song}.mp4", link]
            # popen_and_call(on_exit=to_discord, popen_args=command, exit_args=[interpret, song])
            popen_and_call(on_exit=reload_music, popen_args=command)

            template = loader.get_template('download_started.html')
            return HttpResponse(template.render({}, request))

        except Exception as e:
            print("Error:", e)
            template = loader.get_template('index.html')
            return HttpResponse(template.render({}, request))
    else:
        template = loader.get_template('index.html')
        return HttpResponse(template.render({}, request))
