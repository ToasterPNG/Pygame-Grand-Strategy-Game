

from flask import Flask, render_template, request, send_file, redirect, url_for
import json, os, shutil

app = Flask(__name__)

app.debug = True

@app.route('/')
def hello_world():
    return 'servers 1-3'

@app.route('/identifier')
def server_identifier():
    return "9782364928734"

@app.route('/return_data')
def return_server_data():
    return send_file('server_data.json', as_attachment=True)

@app.route('/upload_server_data', methods = ['GET', 'POST'])
def upload_server_data():

    if request.method == 'POST':

       f = request.files['file']

       f.save("servers/server_data.json")

       return str(f)

@app.route('/1')
def server_1():
    turn = 'Server Error'

    info_config_file = open('servers/info_1.json')
    info_config_file = json.load(info_config_file)

    for i in info_config_file['Data']:
        turn = i['turn']

    return str(turn)

@app.route('/1/upload', methods = ['GET', 'POST'])
def server_1_upload_redirect():
    return render_template('upload.html')

@app.route('/1/upload_redirect', methods = ['GET', 'POST'])
def server_1_upload_file():

    if request.method == 'POST':

       f = request.files['file']

       f.save("servers/info_1.json")

       os.remove("servers/info_2.json")
       shutil.copy2("servers/info_1.json", "servers/info_2.json")
       os.remove("servers/info_3.json")
       shutil.copy2("servers/info_1.json", "servers/info_3.json")

       return str(f)

@app.route('/1/get_data_return', methods = ['GET', 'POST'])
def get_data_return():
    if request.method == 'POST':

       f = request.files['user']

       return str(f)

@app.route('/1/map')
def get_map():
    return send_file('info_1.json', as_attachment=True)

@app.route('/1/get_data')
def get_data():
    return render_template('get_data.html')




@app.route('/2')
def server_2():
    turn = 'Server Error'

    info_config_file = open('servers/info_2.json')
    info_config_file = json.load(info_config_file)

    for i in info_config_file['Data']:
        turn = i['turn']

    return str(turn)

@app.route('/2/upload', methods = ['GET', 'POST'])
def server_2_upload_redirect():
    return render_template('upload.html')

@app.route('/2/upload_redirect', methods = ['GET', 'POST'])
def server_2_upload_file():

    if request.method == 'POST':

       f = request.files['file']

       f.save("servers/info_2.json")

       os.remove("servers/info_1.json")
       shutil.copy2("servers/info_2.json", "servers/info_1.json")
       os.remove("servers/info_3.json")
       shutil.copy2("servers/info_2.json", "servers/info_3.json")

       return str(f)

@app.route('/2/get_data_return', methods = ['GET', 'POST'])
def get_data_return_2():
    if request.method == 'POST':

       f = request.files['user']

       return str(f)

@app.route('/2/map')
def get_map_2():
    return send_file('info_2.json', as_attachment=True)

@app.route('/2/get_data')
def get_data_2():
    return render_template('get_data.html')


















@app.route('/3')
def server_3():
    turn = 'Server Error'

    info_config_file = open('servers/info_3.json')
    info_config_file = json.load(info_config_file)

    for i in info_config_file['Data']:
        turn = i['turn']

    return str(turn)

@app.route('/3/upload', methods = ['GET', 'POST'])
def server_3_upload_redirect():
    return render_template('upload.html')

@app.route('/3/upload_redirect', methods = ['GET', 'POST'])
def server_3_upload_file():

    if request.method == 'POST':

       f = request.files['file']

       f.save("servers/info_3.json")

       os.remove("servers/info_2.json")
       shutil.copy2("servers/info_3.json", "servers/info_2.json")
       os.remove("servers/info_1.json")
       shutil.copy2("servers/info_3.json", "servers/info_1.json")

       return str(f)

@app.route('/3/get_data_return', methods = ['GET', 'POST'])
def get_data_return_3():
    if request.method == 'POST':

       f = request.files['user']

       return str(f)

@app.route('/3/map')
def get_map_3():
    return send_file('info_3.json', as_attachment=True)

@app.route('/3/get_data')
def get_data_3():
    return render_template('get_data.html')



















@app.route('/server_list', methods = ['GET', 'POST'])
def server_list():

    if request.method == 'POST':

       f = request.files['file']

       f.save("servers/priority.txt")

    return redirect(url_for('server_list_view'))

@app.route('/server_list/view')
def server_list_view():

    priority_file = open('servers/priority.txt')
    file_lines = priority_file.readlines()

    msg_str = "error parsing priority file"
    msg_strings = []

    for line in file_lines:

        if line[1] == '0':
            status = "Online"
        elif line[1] == '1':
            status = "Offline"
        else:
            status = "error in getting status information"

        msg_str = f"server {line[0]} - {status} <br/>"
        msg_strings.append(msg_str)

    final_return = ' '.join([str(elem) for elem in msg_strings])
    return final_return


if __name__ == '__main__':
   app.run()