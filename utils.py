import secrets
import string


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
