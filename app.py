from flask import Flask, render_template, request
app = Flask(__name__)
import csv, hashlib

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


@app.route("/newuser",methods=['POST'])
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
    return render_template('result.html',link=link,result=textToPrint,linkText = linkTxt)

if __name__ == "__main__":
    app.debug = True
    app.run()

