import os
import platform
import secrets
from pathlib import Path
import requests
import pyperclip
import typer
from tabulate import tabulate
from pytube import YouTube
import socket
from datetime import datetime
import string
from random import randint
import utils
from time import sleep
import sys

app = typer.Typer()


@app.command(help="""Generates a random password with the given length.
 By default password is not strong enough since it has only alphabet letters
  (no digits or puncuations). By default the generated password is copied to clipboard.
 You can change the behavior """)
def genpass(length: int, strong: bool = False, copy: bool = True):
    if (length < 5):
        print("Password can't be that short")
        return
    pwd = utils.generate_password(length, strong)
    if copy:
        pyperclip.copy(pwd)
    print(pwd)


@app.command(help="Generates a random hex token. copy='copy to clipboard' and defaults to true")
def hex_token(length: int = 16, copy: bool = True):
    token = secrets.token_hex(length)
    if copy:
        pyperclip.copy(token)
    print(token)


@app.command(help="Shows a bunch of information about underlying system")
def check_system():
    info = (
        ("Operating System", platform.system()),
        ("Version", platform.version()),
        ("Release", platform.release()),
        ("Machine", platform.machine()),
        ("Cpu count", str(os.cpu_count())),
        ("Processor", platform.uname().processor),
        ("Device name", platform.uname().node)
    )
    print(tabulate(info))


@app.command("yt", help="Downloads the youtube video by its link")
def youtube(link: str, name: str = ""):
    save_path = str(Path.home() / "downloads")
    youtubeObject = YouTube(link)
    youtubeObject = youtubeObject.streams.get_highest_resolution()
    try:
        print("Downloading...")
        youtubeObject.download(output_path=save_path,
                               filename=name + ".mp4" if name != "" else f'{secrets.token_hex(5)}.mp4')
    except:
        print("An error has occurred")
        return
    print("Download is completed successfully")


@app.command(help="Returns a random motivational quote")
def motivate_me():
    data = requests.get("https://zenquotes.io/api/random")
    quote = data.json()[0]['q']
    author = data.json()[0]['a']
    print(quote, author, sep='  ')


@app.command(help="Generates a random hex color")
def random_color():
    color = '#'
    for i in range(3):
        color += format(randint(0, 255), 'x')
    print(color)


@app.command(help="Shows your public ip address")
def my_ip():
    hostname = socket.gethostname()
    print(socket.gethostbyname(hostname))


@app.command(help="Helps you focus for given amount of minutes")
def focus(minutes: int = 30):
    seconds = minutes * 60
    while seconds > 0:
        h, m, s = utils.parse_time_from_secs(seconds)
        h_str = str(h) if h > 9 else '0' + str(h)
        m_str = str(m) if m > 9 else '0' + str(m)
        s_str = str(s) if s > 9 else '0' + str(s)
        sys.stdout.write(
            f'Please focus! Time remaining - {h_str}:{m_str}:{s_str}\r')
        seconds -= 1
        sleep(1)
        sys.stdout.flush()
    else:
        sys.stdout.write(
            f'Please focus! Time remaining - 00:00\r')


@app.command(help="Shows time for the provided timezone")
def world_time(continent: str, city: str, show_date: bool = False):
    try:
        res = requests.get(
            f'http://worldtimeapi.org/api/timezone/{continent.capitalize()}/{city.capitalize()}')
        dt = res.json()['datetime']
        time_part = datetime.fromisoformat(dt).time()
        date_part = datetime.fromisoformat(dt).date()
        time_part_as_clock = ":".join(str(time_part).split(":")[0:2])
        if show_date:
            print(date_part, time_part_as_clock)
        else:
            print(time_part_as_clock)
    except:
        print("Could not detect area provided")


@app.command(help="""
Tired of 'git add -A', 'git commit -m \{msg\}' and 'git push'? Here is the solution 😎.
""")
def gacp(msg: str):
    remote = os.popen('git remote').read().strip()
    branch = os.popen('git branch').read()
    print(branch)
    try:
        os.system('git add -A')
        os.system(f'git commit -m "{msg}"')
        os.system(f'git push --set-upstream {remote} {branch}')
    except Exception as e:
        print(e)


if __name__ == "__main__":
    app._add_completion = True
    app()
