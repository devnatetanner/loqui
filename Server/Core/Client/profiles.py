savedprofiles = []

class profiles():
    def __init__(self, profilename, clientregistered, basickey):
            '''self, profilename, clientregistered, basickey'''

            self.name = profilename.lower()
            self.mainclient = clientregistered
            self.key = basickey.lower()
            self.favorites = {}
            self.details = {}
            self.clients = [clientregistered]

    async def addattribute(self, category, attribute, value=None):
        '''self, category, attribute, value || details (dict), favorites (dict), clients (list)'''

        if category == "details":
            self.details[attribute] = value
        elif category == "favorites":
            self.favorites[attribute] = value
        elif category == "clients":
            self.client.append(attribute)

async def checkprofile(name, key=None):
    
    for profile in savedprofiles:
        if (profile.name == name.lower() or profile.name in name.lower()) and (not key or (key.lower() and profile.key == key.lower())):
            return True, profile
    return False