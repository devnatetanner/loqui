from Core.Client import profiles

import asyncio

keywords = []


async def remember(sentence, profile, excess, literal):
    if sentence[sentence.index("remember") + 1] == "my":
        if "favorite" in sentence:
            noun = sentence[sentence.index("favorite") + 1]
            placement = sentence.index(sentence[sentence.index(noun) + 1])
            if sentence[sentence.index(noun) + 1] != 'is' and sentence[sentence.index(noun) + 1] != 'are':
                placement = sentence.index(sentence[sentence.index(noun) + 2])
                noun += " " + sentence[sentence.index(noun) + 1]
            if sentence[placement] == "is" or sentence[placement] == "are":
                item = " ".join(sentence[(placement + 1):])
            else:
                if "is" in sentence:
                    item = " ".join(sentence[(sentence.index("is") + 1):])
                elif "are" in sentence:
                    item = " ".join(sentence[(sentence.index("is") + 1):])

            for sprofile in profiles.savedprofiles:
                if sprofile.name == profile['name']:
                    await profiles.profiles.addattribute(sprofile, "favorites", noun, item)

            phrase = f"I have now remembered your favorite {noun} is {item}."

            global skills

            skills['queryremember']['keys'].append(f"do you remember {profile['name']}s favorite {item}")
            skills['queryremember']['keys'].append(f"what is {profile['name']}s favorite {item}")
            skills['queryremember']['keys'].append(f"does {profile['name']}s like {item}")
            skills['queryremember']['keys'].append(f"do you remember my favorite {item}")
            skills['queryremember']['keys'].append(f"what is my favorite {item}")

            global keywords
            
            keywords = []
            for function in skills:
                for key in skills[function]['keys']:
                    keywords.append(key)

            for sprofile in profiles.savedprofiles:
                if sprofile.name == profile['name']:
                    profile = await profiles.profiles.convertprofile(sprofile)
                    print(profile)

    return {'result': 'completed', 'text': phrase, 'profile': profile, 'excess': None}

async def queryremember(sentence, profile, excess, literal):
    if "my" in sentence:
        if "favorite" in sentence:
            noun = " ".join(sentence[(sentence.index('favorite') + 1):])
            for sprofile in profiles.savedprofiles:
                if sprofile.name == profile['name']:
                    profile = await profiles.profiles.convertprofile(sprofile)

            if noun in profile['favorites']:
                phrase = f"I've remembered your favorite {noun} is {profile['favorites'][noun]}."
            else:
                phrase = f"I don't think I remember your favorite {noun}."

    return {'result': 'completed', 'text': phrase, 'profile': profile, 'excess': None}

skills = {

    'remember': {
        'function': remember,
        'keys': ['remember favorite is', 'remember favorite are'],
        'require': ['remember', 'favorite', 'is'],
        'blacklist': ['do', 'you'],
    },
    'queryremember': {
        'function': queryremember,
        'keys': [],
        'require': ['remember', 'favorite', 'is'],
        'blacklist': [],
    },    
}

async def init():
    for profile in profiles.savedprofiles:
        if len(profile.favorites) > 0:
            for item in profile.favorites:
                skills['queryremember']['keys'].append(f"do you remember {profile.name}s favorite {item}")
                skills['queryremember']['keys'].append(f"what is {profile.name}s favorite {item}")
                skills['queryremember']['keys'].append(f"does {profile.name}s like {item}")
                skills['queryremember']['keys'].append(f"do you remember my favorite {item}")
                skills['queryremember']['keys'].append(f"what is my favorite {item}")
        print(profile.favorites)
    print(skills['queryremember']['keys'])   
    print("printed")
                
    for function in skills:
        for key in skills[function]['keys']:
            keywords.append(key)