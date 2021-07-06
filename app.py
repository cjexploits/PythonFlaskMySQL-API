from flask import Flask, request
import requests
import json
from flask_mysqldb import MySQL

app = Flask("__main__")

app.config["MYSQL_HOST"] = "127.0.0.1"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "employee"

mysql = MySQL(app)

@app.route("/", methods=['GET'])
def homepage():
    r = requests.get("https://richardobiye.com/py/api/employee-details.php")
    myresponse = r.content
    res_to_json = json.loads(myresponse)
    cur = mysql.connection.cursor()

    

    for employee in res_to_json:
        idNumbers = employee['idNumbers']
        name = employee['name']
        age = employee['age']
        sex = employee['sex']
        maritalStatus = employee['maritalStatus']
        dateOfBirth = employee['dateOfBirth']
        laptop = employee['laptop']
        ram = laptop['ram']
        ssd = laptop['ssd']
        storage = laptop['storage']
        screenSize = laptop['screenSize']
        speed = laptop['speed']
        phones = employee['phones']
        model = phones['model']
        price = phones['price']
        imei = phones['imei']

        spec = phones['spec']
        ram = spec['ram']
        camera = spec['camera']



        cur.execute("INSERT into emp(idNumbers,name,age,sex,maritalStatus,dateOfBirth) VALUES(%s,%s,%s,%s,%s,%s)",
         (idNumbers, name, age, sex, maritalStatus, dateOfBirth))

        cur.execute("INSERT into laptop(idNumbers,ram,ssd,storage,screenSize,speed) VALUES(%s,%s,%s,%s,%s,%s) ",
                    (idNumbers, ram, ssd, storage, screenSize, speed))

        cur.execute("INSERT into phones(idNumbers, model, price, imei) VALUES(%s, %s, %s, %s)",
                    (idNumbers, model, price, imei))
        cur.execute("INSERT into spec(idNumbers,ram, camera) VALUES(%s, %s, %s)",
                    (idNumbers, ram, camera))

        mysql.connection.commit()

    cur.close()


       




