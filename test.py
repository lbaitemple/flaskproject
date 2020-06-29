from pred import classify
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
folder="/var/www/html/flaskproject/lbai"
aiclass={}
aiclass["model"]=None
aiclass["class"]=None
aiclass["picture"]="pic1.jpg"
pred=classify(folder, aiclass)
print(pred)

