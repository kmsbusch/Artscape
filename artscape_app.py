from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
#import jinja2
import mosaic
import os
# from skimage import img_as_float
# import photomosaic as pm
# import matplotlib.pyplot as plt
import numpy as np
# from tqdm import tqdm
import sys
from PIL import Image
import json
import photomosaic as pm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://kmsbusch:Artscape@kmsbusch.mysql.pythonanywhere-services.com/kmsbusch$users'
db = SQLAlchemy(app)

class user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

global_cache = {}

##
## Add a keybind or button on mosaic view pages where holding it down hides the mosaic image so the users can see the backgroud image to reference
##

@app.route('/')
def index():
    return render_template('home_page_10_19.html')
    #come back in the future and put this template back to newhome.html, and work on making login stuff actually secure
    #also make a reason for someone to even login lmao


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        uname = request.form["uname"]
        passw = request.form["passw"]

        print(f'username : {uname}  password: {passw}', file=sys.stderr)
        login = user.query.filter_by(username=uname, password=passw).first()
        if login is not None:
            return redirect(url_for("gallery_view"))
    return render_template("newhome.html")


@app.route("/registration", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        jsdata = request.get_json()
        # data = json.loads(jsdata)[0]

        uname = jsdata['userName']
        passw = jsdata['pass']

        register = user(username = uname, password = passw)
        db.session.add(register)
        db.session.commit()

        return redirect(url_for("gallery_view"))
    return render_template("newhome.html")


@app.route('/gallery_view')
def gallery_view():
    return render_template('gallery_view.html')#, data=data)


filenames = []
coords = []
@app.route('/mosaic_view', methods=['POST'])
def mosaic_view():

    global filenames
    newdata = {}
    #global global_cache
    data = request.form.get('imageNo')

	#path needs to match location of image passed into function
    pool = pm.import_pool('/home/kmsbusch/mysite/images/pool/image_pool.pool')

    file = request.files['file']

    if len(data) > 0: #gallery provided image case
        nameIn = data.rsplit('/',1)[1]
        image = pm.imread('/home/kmsbusch/mysite/images/pool/newPool/' + nameIn)
        newdata['mosaic'], filenames = mosaic.modifiedBasicMosaic(image, pool, grid_dims = (70, 70))
        newdata['og_img'] = '/static/' + nameIn #image url


    elif len(file.filename) > 0: #user uploaded image case
        img = Image.open(file)
        img.save('/home/kmsbusch/mysite/images/pool/newPool/' + file.filename)
        newdata['mosaic'], filenames = mosaic.modifiedBasicMosaic(img, pool, grid_dims = (70, 70))
        newdata['og_img'] = '/static/' + file.filename #image url

    #print(f'newdata["mosaic"] = {newdata["mosaic"]}', file=sys.stderr)
    # print(f'newdata["og_img"] = {newdata["og_img"]}', file=sys.stderr)
    return render_template('mosaic_view.html', data=newdata)#, coords = coords)

@app.route('/mosaic_view2', methods=['POST'])
def reshuffled_mosaic():
    global filenames
    newdata = {}
    altText = request.form.get('altimageNum') #alt text comes in as "image x" where x is image number in array
    altTextList = altText.split(' ') #put num and word image in a list
    altNum = int(altTextList[1]) #get image number by itself


    imagePath = filenames[altNum][0] #get image name/path from array at index data
    # print(f'imagePath = {imagePath}', file=sys.stderr)
    #call mosaictool with file name
    fileName = os.path.basename(imagePath)
    # print(f'fileName = {fileName}', file=sys.stderr)
    pool = pm.import_pool('/home/kmsbusch/mysite/images/pool/image_pool.pool')
    newdata['mosaic'], filenames = mosaic.modifiedBasicMosaic(pm.imread(imagePath), pool, grid_dims = (70, 70))
    newdata['og_img'] = '/static/' + fileName #image url

    return render_template('mosaic_view.html', data=newdata)#, coords = coords)

'''
#mosaic view 1 backup
@app.route('/mosaic_view', methods=['POST'])
def mosaic_view():
    global filenames
    #global global_cache
    data = request.form.get('imageNo')
    #data2 = request.form.get('altimageNum')
    file = request.files['file']
    if len(data) > 0:
        data, filenames = mosaic.makeMosaic(data)

    elif len(file.filename) > 0:
        img = Image.open(file)
        img.save('/home/kmsbusch/mysite/images/pool/newPool/' + file.filename)
        data, filenames = mosaic.makeMosaic('/static/' + file.filename)

    #data2 = request.form.get('fileName')
    #data2 needs to be in an if to rename it to data or smth
    #image = data['value']
    # Parameters to send back to template:
    # 1. mosaic image
    # 2. width tile
    # 3. height tile
    # 4. number of tiles (in row or column)
    # data = {'image': 'filename.jpg',
    #          'width' : 40,
    #          'height' : 70,
    #          'num_tiles': 70}
    # data is a dictionary
    return render_template('mosaic_view.html', data=data)#, coords = coords)




#mosaic view 2 backup
@app.route('/mosaic_view2', methods=['POST'])
def reshuffled_mosaic():
    global filenames
    altText = request.form.get('altimageNum') #alt text comes in as "image x" where x is image number in array
    altTextList = altText.split(' ') #put num and word image in a list
    altNum = int(altTextList[1]) #get image number by itself

    imagePath = filenames[altNum][0] #get image name/path from array at index data
    #call mosaictool with file name
    fileName = os.path.basename(imagePath)
    data, filenames = mosaic.makeMosaic('/home/kmsbusch/mysite/images/pool/newPool/' + fileName)


    return render_template('mosaic_view.html', data=data)#, coords = coords)
'''



if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
