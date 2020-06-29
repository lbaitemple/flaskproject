import json
import argparse
from werkzeug.security import generate_password_hash
import pwd
import grp
import os

###
##  To create a user use python createroot.py  -p password
###

parser = argparse.ArgumentParser(description='Add root')
parser.add_argument('--verbose',
    action='store_true',
    help='verbose flag' )
parser.add_argument('-p', action='append')

args = parser.parse_args()

passfile='passwd.txt'

users={}
users['root']=generate_password_hash(args.p[0])
with open(passfile, 'w') as outfile:
    json.dump(users, outfile)
    print("user root added")

#uid = pwd.getpwnam(args.u[0]).pw_uid
#gid = grp.getgrnam(args.g[0]).gr_gid
#os.chown(passfile, uid, gid)
os.chmod(passfile,  0o664)
#change file permission and group to www-data
