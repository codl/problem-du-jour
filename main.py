import requests
import time
import random

def get_tag():
    now = int(time.time())
    r = requests.get("https://api.stackexchange.com/2.2/tags", params={
            'todate': now,
            'fromdate': now - 60*60*24*30*6,
            'site': 'serverfault'
        })

    j = r.json()
    tag = random.choice(j['items'])['name']


    return clean_tag(tag)


def clean_tag(tag):
    """
    >>> clean_tag("exchange-2016")
    "exchange 2016"
    >>> clean_tag("docker-compose")
    "docker compose"
    >>> clean_tag("apache2")
    "apache 2"
    """

    def maybe_separate_number(part):
        """
        >>> maybe_separate_number("abc123")
        "abc 123"
        >>> maybe_separate_number("abc")
        "abc"
        >>> maybe_separate_number("123")
        "123"
        """
        version_chars = "0123456789."

        trap = part[::-1]
        # trap is part backwards lol
        trap2 = ""
        isversion = True;
        for c in trap:
            if isversion and c not in version_chars:
                trap2 += " "
                isversion = False
            trap2 += c

        part2 = trap2[::-1]

        return part2.strip()



    parts = map(maybe_separate_number, tag.split("-"))

    return " ".join(parts)

if __name__ == '__main__':
    print("%s always problem lol" % (get_tag(),))
