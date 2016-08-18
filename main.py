import requests
import time
import random
import logging
import discord
import env

"""
a bot that points out things that are always problems lol

add my copy of it to your server with
https://discordapp.com/oauth2/authorize?client_id=215898221610926090&scope=bot&permissions=3088
or replace client_id with yours to add yours

set the PDJ_TOKEN env var to your bot user token, run pip install -r requirements.txt, then run main.py and you're good
"""

logging.basicConfig(level=logging.WARNING)

tag_cache = None
tag_cache_timestamp = 0;

def get_tag():
    global tag_cache, tag_cache_timestamp
    now = int(time.time())
    if not tag_cache or now - tag_cache_timestamp > 60:
        r = requests.get("https://api.stackexchange.com/2.2/tags", params={
                'todate': now,
                'fromdate': now - 60*60*24*30*6,
                'site': 'serverfault'
            })
        tag_cache = j = r.json()
        tag_cache_timestamp = now;
    else:
        j = tag_cache
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

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    if message.author.id != client.user.id and \
        message.content.endswith(("always problem", "always problem lol")):
        await client.send_message(message.channel, "%s always problem lol" % (get_tag(),))


if __name__ == '__main__':
    client.run(os.getenv("PDJ_TOKEN"))
