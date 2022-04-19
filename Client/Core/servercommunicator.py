from http import client
import socket
import json
import time

host = "192.168.1.6"
port = 42069
profilefound = False
while True:
    if not profilefound:
        cserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cserver.connect((host, port))
        clientName = "testing"
        request = {'type':'init', 'name':'nate', 'clientname':clientName}
        request = json.dumps(request)
        cserver.send(request.encode('utf-8'))
        result = cserver.recv(20000).decode('utf-8')
        result = json.loads(result)
        print(repr(result))
        cserver.close()
        profilefound = True
        profile = result['excess']
    cserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cserver.connect((host,port))
    message = input("command >")
    start = round(time.time() * 1000)
    request = {'type':'command', 'profile':profile, 'message':message, 'excess':None}
    request = json.dumps(request)
    cserver.send(request.encode('utf-8'))
    result = cserver.recv(20000).decode('utf-8')
    result = json.loads(result)
    print(repr(result))
    print("\n\n" + result['result'] + "\n")
    finish = round(time.time() * 1000)
    print(f"Process took {finish-start} milliseconds to complete.")
    cserver.close()