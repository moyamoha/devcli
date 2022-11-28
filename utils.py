from datetime import datetime
import secrets
import string
import requests

def generate_password(l: int, strong: bool):
    letters = string.ascii_letters
    sc = string.punctuation
    digits = string.digits
    alphabet = letters + digits + sc
    ans = ''
    if not strong:
        for i in range(l):
            ans += ''.join(secrets.choice(letters))
    else:
        for i in range(l):
            ans += ''.join(secrets.choice(alphabet))
    return ans


def parse_time_from_secs(secs: int):
    h = secs // 3600
    m = (secs - h * 3600) // 60
    s = secs - h * 3600 - m * 60
    return h, m, s

def fetch_time(timezone: str, show_date: bool = False) -> bool:
    try:
        res = requests.get(
        f'http://worldtimeapi.org/api/timezone/{timezone}')
        if 'error' in res.json():
            print('Unknow location')
            return True
        dt = res.json()['datetime']
        time_part = datetime.fromisoformat(dt).time()
        date_part = datetime.fromisoformat(dt).date()
        time_part_as_clock = ":".join(str(time_part).split(":")[0:2])
        if show_date:
            print(date_part, time_part_as_clock)
        else:
            print(time_part_as_clock)
        return True
    except Exception as e:
        return False