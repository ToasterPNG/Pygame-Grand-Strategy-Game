import requests

server_link = open("data\\current_server.txt", "r").read()

def upload_server_data():

    url = f'{server_link}/upload_server_data'
    nm = 'data\\serverbase.txt'

    nmrb = open(nm, 'rb')

    files = [('file', nmrb)]

    r = requests.post(url, files=files)

    if r.ok:
        print("Uploaded JSON Succesfully")
    else:
        print("Error when trying to upload JSON to server !!!")

    nmrb.close()

upload_server_data()