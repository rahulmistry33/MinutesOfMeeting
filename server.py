from flask import Flask,render_template,url_for,redirect,request,flash,make_response
from flask_dance.contrib.google import make_google_blueprint,google

from werkzeug import secure_filename


from app import MomGenerator as m
import os
import json 
import pdfkit 

os.environ['OAUTHLIB_INSECURE_TRANSPORT']='1'
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE']='1'



with open("config.json","r") as c:
    params=json.load(c)["params"]

#creating instance of Flask class
app=Flask(__name__)
app.config['SECRET_KEY']='0501d344495cc373a2a73670ca42ae80'
app.config["UPLOAD_FOLDER"]=params["upload_location"]



blueprint=make_google_blueprint(client_id='796763710919-kljkmv43rbf5920v7ae5n37ktsnp3nab.apps.googleusercontent.com',client_secret='AfbN_kcpO13DT22Lft95IqXx',offline=True,scope=['profile','email'],redirect_url='http://127.0.0.1:5000/login/generate')

app.register_blueprint(blueprint,url_prefix='/login')

'''@app.route("/")
def call():
    val=m.recognizerWithAudioFile()
    return "{}".format(val)'''

app.config["UPLOAD_AUDIO"]=r"static/uploads"
app.config["ALLOWED_EXTENSIONS"]=["wav"]

def allowed_file(filename):
    extension=filename.rsplit(".",1)[1]
    if extension in app.config["ALLOWED_EXTENSIONS"]:
        return True
    else:
        return False






@app.route('/')
def index():
    return render_template('landing.html')



@app.route('/login/google')
def login(google):
    if not google.authorized:
        return render_template(url_for('google.login'))
    else:
        resp= google.get('/oauth2/v2/userinfo')
        assert resp.ok,resp.text
        email= resp.json()['email']
        return render_template(url_for('/login/generate'))


@app.route("/login/generate",methods=['GET','POST'])
def generate():
    if request.method=="POST":
        date=request.form.get('date')
        arr=[]
        for i in range(10):
            
            arr.append(request.form.get("textbox{}".format(i)))
            
        members=request.form.get('members')
        points=request.form.get('points')
        points_array=points.split('# ')
        venue=request.form.get('venue')
        called_by=request.form.get('calledby')
        time=request.form.get('time')
        render= render_template("pdf.html",date=date,arr=arr,members=members,points=points_array,venue=venue,called_by=called_by,time=time)
        #config = pdfkit.configuration(wkhtmltopdf=r'C:\Users\admin\Desktop\wkhtmltox-0.12.5-1.mxe-cross-win32\wkhtmltox\bin\wkhtmltopdf.exe')
        config = pdfkit.configuration(wkhtmltopdf=r'Dependencies\wkhtmltopdf.exe')

        pdf=pdfkit.from_string(render,False,configuration=config)

        response = make_response(pdf)
        response.headers['Content-Type']='application/pdf'
        response.headers['Content-Disposition']='inline;filename=mom.pdf'
        return response

    return render_template("generator.html")

   

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

@app.route("/login/uploader",methods=['GET','POST'])
def uploader():
    if request.method=="POST":
            f = request.files['file']
            f.save(os.path.join(app.config["UPLOAD_FOLDER"],secure_filename(f.filename)))
            name=f.filename
            print("audio saved")
            
            text=m.recognizerWithAudioFile(name)
            return render_template("generator.html",text=text)

'''@app.route("/form",methods=['GET','POST'])
def form():
    if request.method=="POST":
        date=request.args.get('date')
        arr=[]
        for i in range(10):
            if request.args.get("textbox{}".format(i)):
                arr.append(request.args.get("textbox{}".format(i)))
            else:
                break
        members=request.args.get('members')
        points=request.args.get('points')
        return render_template("pdf.html",date=date,arr=arr,members=members,points=points)'''
        
        
        




        
        


   




if __name__=="__main__":
    app.run(debug=True)