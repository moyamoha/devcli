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


@app.command("Generates a random hex color")
def random_color():
    color = '#'
    for i in range(3):
        color += format(randint(0, 255), 'x')
    print(color)


@app.command(help="Shows your public ip address")
def my_ip():
    hostname = socket.gethostname()
    print(socket.gethostbyname(hostname))


if __name__ == "__main__":
    app._add_completion = True
    app()
