from flask import Flask, render_template, request, redirect, session
app = Flask(__name__)
import csv, hashlib, os

app.secret_key = os.urandom(32)
loginInstruct = ""
loadAmount = 0

def hash(word):
    myHashObject = hashlib.sha1()
    w = word.encode('utf-8')
    myHashObject.update(w)
    return myHashObject.hexdigest()
       #returns hex string

def authenticate(username,password):
    store = csv.reader(open("data/users.csv",'r'))
    for row in store:
        if row and username == row[0]:
            if hash(password) == row[1]:
                return "YES"
            else:
                return "WRONG"
    return "NOT EXIST"


def isUserCookieValid():
    sheet = csv.reader(open("data/users.csv",'r'))
    for row in sheet:
        #how do you check if the key exists
        if session and row and session["username"] == row[0]:
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
    global loginInstruct
    global loadAmount
    if loadAmount > 0:
        loginInstruct = ""
        loadAmount = 0
    if isUserCookieValid() == True:
        return render_template("home.html",user=session["username"])
    else:
        if loginInstruct == "":
            return render_template("login.html")
        loadAmount += 1
        return render_template("login.html",extratext = loginInstruct)


@app.route("/auth",methods=["POST"])
def check():
    textToPrint = ""
    link = ""
    linkTxt = ""
    global loginInstruct
    global loadAmount
    loadAmount = 0
    if request.form["submit"] == "Login":
        success = authenticate(request.form['username'],request.form['password'])
        if success == "YES":
            textToPrint = "Login successful!"
            session["username"] = request.form['username']
            loadAmount = 0
            loginInstruct = ""
            return redirect("/")
        elif success == "WRONG":
            loginInstruct = "Login failed!"
            return redirect("/")
        else:
            loginInstruct = "User provided does not exist"
            return redirect("/")
    elif request.form["submit"] == "Register":
        if addUser(request.form['username'],request.form['password']):
            loginInstruct = "User successfully registered! You can now log in!"
            return redirect("/")
        else:
            loginInstruct = "Registration failed!"
            return redirect("/")
    elif request.form["submit"] == "Logout":
        loadAmount = 0
        loginInstruct = ""
        session.pop("username")
        return redirect("/")
    return render_template("result.html",result="You broke the page!")


@app.route("/jacobo")
def js():
    return redirect("http://xkcd.com")


if __name__ == "__main__":
    app.debug = True
    app.run()

