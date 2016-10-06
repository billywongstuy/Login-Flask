from flask import Flask, render_template, request, redirect, session
app = Flask(__name__)
import csv, hashlib, os

def hash(word):
    myHashObject = hashlib.sha1()
    w = word.encode('utf-8')
    myHashObject.update(w)
    return myHashObject.hexdigest()
       #returns hex string

def authenticate(username,password):
    store = csv.reader(open("data/users.csv",'r'))
    for row in store:
        if row:
            if username == row[0]:
                if hash(password) == row[1]:
                    return "YES"
                else:
                    return "WRONG"
    return "NOT EXIST"


def isUserCookieValid():
    sheet = csv.reader(open("data/users.csv",'r'))
    for row in sheet:
        #how do you check if the key exists
        if session["username"] and row and session["username"] == row[0]:
            return True
    return False

def addUser(username,password):
    sheet = open("data/users.csv",'r')
    read = csv.reader(sheet)
    if username == "" or password == "":
        return False
    for row in read:
        if row:
            if (username == row[0]):
                return False
    sheet.close()
    sheet = open("data/users.csv",'a')
    write = csv.writer(sheet)
    write.writerow([username,hash(password)])
    return True


@app.route("/")
def login():
    #check the cookie
    if isUserCookieValid() == True:
        return render_template("home.html")
    else:
        return render_template("login.html")

@app.route("/auth",methods=["POST"])
def check():
    #print app
    #print request
    #print request.args
    #print request.args['username']
    #print request.headers
    textToPrint = ""
    link = ""
    linkTxt = ""
    if request.form["submit"] == "Login":
        success = authenticate(request.form['username'],request.form['password'])
        if success == "YES":
            textToPrint = "Login successful!"
            app.secret_key = os.urandom(32)
            session["username"] = request.form['username']
        elif success == "WRONG":
            textToPrint = "Login failed!"
        else:
            textToPrint = "You broke the page"
    elif request.form["submit"] == "Register":
        if addUser(request.form['username'],request.form['password']):
            textToPrint = "Registration successful!"
            link = "/"
            linkTxt = "Click here to return to the login page."
        else:
            textToPrint = "Registration failed!"
            link = "/register"
            linkTxt = "Click here to return to the registration page."
    elif request.form["submit"] == "Logout":
        session.pop("username")
        return redirect("login.html")
    return render_template("result.html",result=textToPrint,link=link,linkText = linkTxt)


@app.route("/register")
def reg():
    return render_template("register.html")



somestring = '''@app.route("/newuser",methods=['POST'])
def create():
    textToPrint = ""
    link = ""
    linkTxt = ""
    if addUser(request.form['username'],request.form['password']):
        textToPrint = "Registration successful!"
        link = "/"
        linkTxt = "Click here to return to the login page."
    else:
        textToPrint = "Registration failed!"
        link = "/register"
        linkTxt = "Click here to return to the registration page."
    return render_template('result.html',link=link,result=textToPrint,linkText = linkTxt)'''


@app.route("/jacobo")
def js():
    return redirect("http://xkcd.com")


if __name__ == "__main__":
    app.debug = True
    app.run()

