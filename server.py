from flask import Flask,render_template,url_for,redirect,request,flash
from werkzeug import secure_filename
from app import MomGenerator as m
import os
import json 


with open("config.json","r") as c:
    params=json.load(c)["params"]

#creating instance of Flask class
app=Flask(__name__)
app.config['SECRET_KEY']='0501d344495cc373a2a73670ca42ae80'
app.config["UPLOAD_FOLDER"]=params["upload_location"]





'''@app.route("/")
def call():
    val=m.recognizerWithAudioFile()
    return "{}".format(val)'''

app.config["UPLOAD_AUDIO"]=r"static\uploads"
app.config["ALLOWED_EXTENSIONS"]=["wav"]

def allowed_file(filename):
    extension=filename.rsplit(".",1)[1]
    if extension in app.config["ALLOWED_EXTENSIONS"]:
        return True
    else:
        return False


@app.route("/",methods=['GET','POST'])
def generate():

    '''name=""
    text=""
    if request.method=="POST":
        if request.files:

            audio=request.files["audio"]
            if not allowed_file(audio.filename):
                flash(f"Only filenames with wav extension is allowed","danger")
                return render_template(request.url)
            
            audio.save(os.path.join(app.config["UPLOAD_AUDIO"],audio.filename))
            name=audio.filename
            print("audio saved")
            #return redirect(request.url)
        text=m.recognizerWithAudioFile(name)'''
    
    return render_template("generator.html")

@app.route("/uploader",methods=['GET','POST'])
def uploader():
    if request.method=="POST":
            f = request.files['file']
            f.save(os.path.join(app.config["UPLOAD_FOLDER"],secure_filename(f.filename)))
            name=f.filename
            print("audio saved")
            text=m.recognizerWithAudioFile(name)
            return render_template("generator.html",text=text)

        
        


   




if __name__=="__main__":
    app.run(debug=True)