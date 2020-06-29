import json
from werkzeug.security import generate_password_hash

def addnewuser(passfile, user, passwd):
    with open(passfile) as json_file:
        users = json.load(json_file)
    try:
        if users.get(user)!=None:
            return "user exist - \n", 300
        else:
            users[user]=generate_password_hash(passwd)
            with open(passfile, 'w') as outfile:
                json.dump(users, outfile)
            return "user added\n", 200
    except:
        return "user exist + \n", 300

def deluser(passfile, user):
    if user=="root":
        return "root cannot delete root\n", 400 
    with open(passfile) as json_file:
        users = json.load(json_file)
    try:
        if users.get(user)!=None:
            users.pop(user)
            with open(passfile, 'w') as outfile:
                json.dump(users, outfile)
            return "user deleted - \n", 300
        else:
            return "user not exist \n", 300
    except:
        return "user delete error + \n", 300

def changepw(passfile, user, npasswd):
    if user=="root":
        return "root cannot change root's passwd \n", 400 
    with open(passfile) as json_file:
        users = json.load(json_file)
    try:
        if users.get(user)!=None:

            users[user]=generate_password_hash(npasswd)  #update with new pass for user
            with open(passfile, 'w') as outfile:
                json.dump(users, outfile)
            return "user passwd modified - \n", 200
        else:
            return "user not exist \n", 300
    except:
        return "user passwd change error + \n", 300
