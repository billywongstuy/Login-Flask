from flask import Flask, render_template, request
app = Flask(__name__)
import csv

def authenticate(username,password):
    store = csv.reader(open("data/users.csv"))
    for row in store:
        if username == row[0]:
            if password == row[1]:
                return True
    return False

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
    if success:
        textToPrint = "Login successful!"
    else:
        textToPrint = "Login failed!" 
    return render_template("result.html",result=textToPrint)

if __name__ == "__main__":
    app.debug = True
    app.run()

