from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect
import os


app = Flask(__name__)
app.secret_key = 'many random bytes'
csrf = CSRFProtect(app)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_PORT']=3307
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flaskcrud'

mysql = MySQL(app)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
target = os.path.join(APP_ROOT, 'images/')

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("""SELECT  * FROM register""")
    data = cur.fetchall()
    cur.close()
    return render_template("index.html",user=data)


@app.route('/register/')
def register():
    return render_template("register.html")


@app.route('/submit/', methods = ['POST'])
def submit():

    if request.method == "POST":
        #flash("Data Inserted Successfully")

        #save image to a folder

        if not os.path.isdir(target):
            os.mkdir(target)
        file = request.files['image']
        filename = file.filename

        destination = "/".join([target, filename])
        file.save(destination)
        print(filename)

        name = request.form['name']
        email = request.form['email']
        passw = request.form['pass']
        cur = mysql.connection.cursor()
        cur.execute("""INSERT INTO register VALUES ('', %s, %s, %s, %s)""", (name, email, passw,filename))
        mysql.connection.commit()
        return redirect(url_for('index'))


@app.route('/edit/<string:id>', methods=['GET'])
def edit(id):
    if request.method == "GET":
        #flash("Data Inserted Successfully")
        cur = mysql.connection.cursor()
        cur.execute("""SELECT  * FROM register where id=%s""", [id])
        info = cur.fetchall()
        cur.close()
        return render_template("edit.html", user=info, id=id)


@app.route('/update/<string:id>',methods=['POST','GET'])
def update(id):
    if request.method == "POST":

        name = request.form['name']
        email = request.form['email']
        password = request.form['pass']
        file = request.files['image']
        filename = file.filename
        print(filename)
        destination = "/".join([target, filename])
        file.save(destination)

        cur = mysql.connection.cursor()
        cur.execute("""
               UPDATE register
               SET name=%s, email=%s, password=%s, image=%s
               WHERE id=%s
            """, (name, email, password,filename, id))
        #flash("Data Updated Successfully")
        mysql.connection.commit()
        return redirect(url_for('index'))


@app.route('/delete/<string:id>', methods=['GET'])
def delete(id):
    if request.method == "GET":
        #flash("Data Inserted Successfully")
        cur = mysql.connection.cursor()
        cur.execute("""DELETE FROM register where id=%s""", [id])
        mysql.connection.commit()
        return redirect(url_for('index'))

@app.route('/images/<filename>')
def send_image(filename):
    return send_from_directory("images", filename)

if __name__ == "__main__":
      app.run(debug=True)