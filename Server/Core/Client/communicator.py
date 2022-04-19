from Core.Command import executer as exe
from Core.Universal import functions as unifunc
from Core.Client import initialization as init
from Core.Data import pickling
import asyncio
import json
import socket
import traceback

host = "192.168.1.6"
port = 42069
juststarted = True


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen(3)




async def clientlisten():

    while True:
        try:
            global juststarted

            if juststarted == True:
                await init.initstart()
                await pickling.unpackpickles()
                juststarted = False

            print(f"HOST {host} | Active and waiting for connection")
            
            await asyncio.sleep(1)
            await pickling.packpickles()

            client, clientAddr = server.accept()
            print(f"HOST {host} | Successful connection from CLIENT {clientAddr[0]}")
            request = client.recv(2450)
            await processrequest(request, client, clientAddr)
            
        except Exception as E:
            print(repr(E))
            traceback.print_exc()
            await asyncio.sleep(10)


async def processrequest(request, client, clientAddr):

        clientAddr = clientAddr[0]
        request = await unifunc.parserequest(request)

        if 'profile' in request:
            print(f"HOST {host} | Recieved {request['type']} request from CLIENT {clientAddr}-{request['profile']['name']}")
        else:
            print(f"HOST {host} | Recieved {request['type']} request from CLIENT {clientAddr}")

        if request['type'] == "command":
            result = await exe.exe(request['message'], request['profile'], request['excess'])
            result = await unifunc.makerequest(result['result'], 'command', result['text'], result['excess'])
            client.send(result)
            if 'profile' in request:
                print(f"HOST {host} | Sent {request['type']} request result to CLIENT {clientAddr}-{request['profile']['name']}")
            else:
                print(f"HOST {host} | Sent {request['type']} request result to CLIENT {clientAddr}")      

        if request['type'] == 'init':
            result, profile = await init.init(request['name'], [clientAddr, request['clientname']])
            jsonprofile = {'name': profile.name, 'key': profile.key, 'mainclient': profile.mainclient, 'clients': profile.clients, 'favorites':profile.favorites, 'details': profile.details}
            result = await unifunc.makerequest('profilequery', 'initprofile', result, jsonprofile)
            client.send(result)            

            if 'profile' in request:
                print(f"HOST {host} | Sent {request['type']} request result to CLIENT {clientAddr}-{request['profile']['name']}")
            else:
                print(f"HOST {host} | Sent {request['type']} request result to CLIENT {clientAddr}")    
                
asyncio.run(clientlisten())