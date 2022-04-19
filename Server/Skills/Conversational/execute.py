from typing import final
from Core.Universal import functions as unifunc

from datetime import datetime
import asyncio

keywords = []


async def hello(sentence, profile, excess, literal):
    greetings = [f"Hi, {profile['name']}.",
                 f"Hello, {profile['name']}.",
                 f"Howdy, {profile['name']}.",
                 f"Greetings, {profile['name']}"]

    now = datetime.now()
    currentHour = int(now.strftime("%I"))

    if currentHour >= 3 and currentHour < 12:
        greetings.append(f"Good morning, {profile['name']}.")
    elif currentHour >= 13 and currentHour < 18:
        greetings.append(f"Good afternoon, {profile['name']}.")
    elif currentHour != 12:
        greetings.append(f"Good evening, {profile['name']}.") 

    greeting = await unifunc.choosePhrase(greetings)

    return {'result': 'completed', 'text': greeting, 'profile': profile, 'excess': None}

async def time(sentence, profile, excess, literal):
    now = datetime.now()
    currentTime = now.strftime("%I:%M %p")

    phrasing = [f"The time is now {currentTime}.",
                f"It's currently {currentTime}.",
                f"It is now {currentTime}.",
                f"{currentTime}",
                f"{currentTime} is the current time."]

    finalphrase = await unifunc.choosePhrase(phrasing)

    return {'result': 'completed', 'text': finalphrase, 'profile': profile, 'excess': None}

async def whatismyname(sentence, profile, excess, literal):
    phrasing = await unifunc.choosePhrase([f"Your name is {profile['name']}.",
                                           f"I have your name saved as {profile['name']}",
                                           f"I recognize you as {profile['name']}.",
                                           f"I'm guessing your name is {profile['name']}."])

    return {'result': 'completed', 'text': phrasing, 'profile': profile, 'excess': None}

async def howareyou(sentence, profile, excess, literal):
    if excess is not None and excess.has_key("queryanswered"):
        bad = ["bad", "not good", "terrible", "awful", 'worried', 'stressed']
        tone = 'good'
        for word in bad:
            if word in sentence:
                tone = 'bad'

        if tone  == 'good':      
            phrasing = [f"Good to hear, {profile['name']}.",
                        f"Glad to hear that, {profile['name']}.",
                        f"That's good to hear, {profile['name']}."]
            if excess.has_key("weather") and excess['weather']['context'] == 'clear':
                phrasing.append("Glad to hear it. I bet the clear skies are helping.")
                phrasing.append("Good to hear. The nice weather today should help keep your day good.")
        elif tone == "bad":
            phrasing = [f"Sorry to hear, {profile['name']}.",
                        f"Sorry to hear that, {profile['name']}.",
                        f"I'm sorry to hear that, {profile['name']}."]
            if excess.has_key("weather") and excess['weather']['context'] == 'bad':
                phrasing.append("I'm sorry to hear that. The weather probably isn't helping either.")
                phrasing.append("Sorry to hear that. Hopefully the weather will improve soon and help better your day.") 

        finalphrase = await unifunc.choosePhrase(phrasing)

        return {'result': 'completed', 'text': finalphrase, 'profile': profile, 'excess': None}


    else:
        phrasing = [f"I am doing great, {profile['name']}. How are you doing?",
                    f"I am doing good. Thanks for asking, {profile['name']}. How are you doing?",
                    f"I'm doing good, {profile['name']}. How are you?",
                    f"Doing great. Thanks for asking. How are you, {profile['name']}?"]

        finalphrase = await unifunc.choosePhrase(phrasing)

        return {'result': 'completed', 'text': finalphrase, 'profile': profile, 'excess': {'queried': 'true', 'query': 'howareyou'}}

skills = {

    'hello': {
        'function': hello,
        'keys': ['Hi', 'Hello', 'Howdy', 'Sup', 'Good morning', 'Good afternoon', 'Good evening', 'Hey', 'Greetings'],
        'require': [],
        'blacklist': ['when', 'name', 'who', 'know'],
    },
    'time': {
        'function': time,
        'keys': ['what time is it', 'whats the time', 'what time is it now', 'what is the time', 'can you tell me the time', 'what is the current time',
                'could you tell me the time', 'may i know the time', 'could i have the time'],
        'require': ['time'],
        'blacklist': ['open', 'close', 'when'],
    },
    'whatismyname': {
        'function': whatismyname,
        'keys': ['what is my name', "who am i", "do you know who i am", "whats my name", "who is logged in", "who is using this", "do you know me"],
        'require': ['name'],
        'blacklist': [],
    },
    'howareyou': {
        'function': howareyou,
        'keys': ['how are you', 'how have you been', 'hows it going', 'hows everything', 'whats up'],
        'require': [],
        'blacklist': ['when'],
    }
}

for function in skills:
    for key in skills[function]['keys']:
        keywords.append(key)