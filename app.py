from datetime import datetime
from flask import Flask, request, abort, jsonify
import paho.mqtt.client as mqtt
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import  check_password_hash
import logging, os, json, glob
from pred import classify, removefiles
from user import addnewuser, deluser, changepw
from webpacsv import calcsvscore

app = Flask(__name__)
auth = HTTPBasicAuth()
passfile=os.path.join(os.path.dirname(__file__), "passwd.txt")

with open(passfile) as json_file:
    users = json.load(json_file)


@auth.verify_password
def verify_password(username, password):
    global users
    if username in users and \
            check_password_hash(users.get(username), password):
        return username


 
@app.route( "/webpa", methods=["POST"])
@auth.login_required
def webpa():
    # data format
    data = request.form.to_dict(flat=True)
    folder="webpa/" + auth.current_user()
    dirc=os.path.join(os.path.dirname(__file__), folder)
    if not os.path.exists(dirc):
        os.makedirs(dirc)
    content = ['csv']
    aiclass={}

    for fi in content:
        try:
            # upload file into user's folder and set the name in dict aiclass
            file = request.files[fi]
            aiclass[fi]=file.filename
            if fi=='csv':
                fileformat = os.path.splitext(aiclass[fi])
                if (fileformat[1].lower() != '.csv'):
                     return 'need csv label file , but'+ fileformat[1] + ' is given\n', 300
                else:
                    list_of_files = glob.glob(os.path.join(dirc, "*.csv"))
                    removefiles(list_of_files)
            file.save(os.path.join(dirc, file.filename))
        except:
            # if no option is given, set  the file name as None
            aiclass[fi] = None
    pred=classify(dirc, aiclass)

    if pred == None:
        if (data.get('format')=='json'):
            return jsonify({'status': 'failed', 'reason': 'need picture file'}), 300
        else:
            return 'need picture file', 300
    else:
        if (data.get('format')=='json'):
            return jsonify({'status': 'success', 'pred': pred}), 200
        else:
            return pred+'\n', 200
    return ""


@app.route( "/classfy", methods=["POST"])
@auth.login_required
def classfy():
    # data format
    data = request.form.to_dict(flat=True)
    folder="upload/" + auth.current_user()
    dirc=os.path.join(os.path.dirname(__file__), folder)
    if not os.path.exists(dirc):
        os.makedirs(dirc)
    #bauth = self.headers['Authorization'].split(' ')[1]
    #load files to be classfied
    content = ['class', 'model', 'picture']
    aiclass={}

    for fi in content:
        try:
            # upload file into user's folder and set the name in dict aiclass
            file = request.files[fi]
            aiclass[fi]=file.filename
            if fi=='class':
                fileformat = os.path.splitext(aiclass[fi])
                if (fileformat[1].lower() != '.txt'):
                     return 'need txt label file , but'+ fileformat[1] + ' is given\n', 300
                else:
                    list_of_files = glob.glob(os.path.join(dirc, "*.txt"))
                    removefiles(list_of_files)
            elif fi=='model':
                fileformat = os.path.splitext(aiclass[fi])
                if (fileformat[1].lower() != '.hd5' and fileformat[1].lower() != '.h5'):
                     return 'need hd5 model file, but '+ fileformat[1] + ' is given\n', 300
                else:
                    list_of_files = glob.glob(os.path.join(dirc, "*.h5"))
                    removefiles(list_of_files)
            elif fi=='picture':
                fileformat=os.path.splitext(aiclass[fi])
                if (fileformat[1].lower() != '.jpg' and fileformat[1].lower() != '.jpeg'):
                     return 'need JPG picture file, but '+ fileformat[1] + ' is given \n', 300
                else:
                     list_of_files = glob.glob(os.path.join(dirc, "*.jpg")) 
                     removefiles(list_of_files)

            file.save(os.path.join(dirc, file.filename))
        except:
            # if no option is given, set  the file name as None
            aiclass[fi] = None
    pred=classify(dirc, aiclass)

    if pred == None:
        if (data.get('format')=='json'):
            return jsonify({'status': 'failed', 'reason': 'need picture file'}), 300
        else:
            return 'need picture file', 300
    else:
        if (data.get('format')=='json'):
            return jsonify({'status': 'success', 'pred': pred}), 200
        else:
            return pred+'\n', 200
    return ""


@app.route('/webhook', methods=['POST'])
@auth.login_required
def webhook():
        # get client from cloudmqtt
        data = request.form.to_dict(flat=True)
        #
        user=data['user']    # "pspniyjc"
        passwd =data['passwd']  # "sBm4EpaDgRe5"
        hostname=data['host']    #"m16.cloudmqtt.com"
        port=int(data['port'])   # 12247
        client = mqtt.Client()
        client.username_pw_set(user, passwd)
        client.connect(hostname, port, 60)
#        return data['topic'] + hostname + "\n" + data['value'] + "\n", 200
        if request.method == 'POST':
#                data=request.json
                #publush the topic with the data
                client.publish(data['topic'], data['value'])
                debugstr=str(datetime.now()) +": "+ data['topic'] + " - " + data['value']
                logging.debug(debugstr)
                return jsonify({'status':'success', 'time':datetime.now()}), 200
        else:
                abort(400)

@app.route( "/user", methods=["POST"])
@auth.login_required
def user():
    global users
    # data format
    data = request.form.to_dict(flat=True)
    if (auth.current_user()=='root'):
        if (data['action']=='add'):
            ret=addnewuser(passfile, data['user'], data['passwd'])
        elif (data['action']=='delete'):
            ret = deluser(passfile, data['user'])
        elif (data['action']=='changpwd'):
            ret = changepw(passfile, data['user'], data['passwd'])
        else:
            ret = "action {" + data['action'] + "} not implemented\n", 300
        with open(passfile) as json_file:
            users = json.load(json_file)
        return ret
    else:
        return "Cannot  grant access\n", 401


if __name__ == "__main__":
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
    app.run()
