from flask import Flask, render_template, request
app = Flask(__name__)
import csv, hashlib

def hash(word):
    myhashObject = hashlib.sha1()
    myhashObject.update(word)
    return myHashObject.hexdigest()
       #returns hex string

def authenticate(username,password):
    store = csv.reader(open("data/users.csv"))
    for row in store:
        if username == row[0]:
            if password == row[1]:
                #check hash later
                return "YES"
            else:
                return "WRONG"
    return "NOT EXIST"


def addUser(username,password):
    sheet = ("data/users.csv",'a+')
    read = csv.reader(sheet)
    for row in read:
        if username == row[0] or username == None:
            return False
    sheet.seek(0)
    write = csv.reader(sheet)
    b.writerow([username,password])
    #add hash later

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/auth",methods=["POST"])
def check():
    #print app
    #print request
    #print request.args
    #print request.args['username']
    #print request.headers
    success = authenticate(request.form['username'],request.form['password'])
    textToPrint = ""
    link = ""
    linkTxt = ""
    if success == "YES":
        textToPrint = "Login successful!"
    elif success == "NOT EXIST":
        textToPrint = "User does not exist. Register here:"
        link = "/register"
        linkTxt = "Register Here"
    else:
        textToPrint = "Login failed!" 
    return render_template("result.html",result=textToPrint,link=link,linkText = linkTxt)


@app.route("/register")
def reg():
    return render_template("register.html")


@app.route("/newuser")
def create():
    return ""

if __name__ == "__main__":
    app.debug = True
    app.run()

