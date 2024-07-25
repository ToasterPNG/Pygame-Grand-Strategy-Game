import requests, os

os.system("cls")

print("")

for x in range(5):

    priority_file = open('../data/priority.txt')
    file_lines = priority_file.readlines()
    
    try:
        status_code = requests.get(f"http://rtsonline.pythonanywhere.com/{x + 1}", timeout=30).status_code
    except requests.ConnectionError:
        status_code = 0

    if status_code == 200:
        file_lines[x] = f"{x + 1}0\n"
    else:
        file_lines[x] = f"{x + 1}1\n"

    with open('../data/priority.txt', 'w') as file: 
        file.writelines(file_lines)

    priority_file.close()

priority_file = open('../data/priority.txt')
file_lines = priority_file.readlines()

for line in file_lines:

    if line[1] == '0':
        status = "Online"
    elif line[1] == '1':
        status = "Offline"
    else:
        status = "error in getting status information"

    print(f"server {line[0]} - {status}")

url = f'http://rtsonline.pythonanywhere.com/server_list'
nm = '../data/priority.txt'


nmrb = open(nm, 'rb')

files = [('file', nmrb)]

r = requests.post(url, files=files)

if r.ok:
    print("\nStatuses --> http://rtsonline.pythonanywhere.com/server_list/view")
    print("You can change the port used by the game in data\\server_id.txt\n")
    print("(Players dont need to be on the same port)")
else:
    print("!!! error when trying to upload data to server !!!")

nmrb.close()