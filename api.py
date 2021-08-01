
from flask import Flask,jsonify,request
import json
import requests
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

        for phone in phones:

            model = phone['model']
            price = phone['price']
            imei = phone['imei']

            spec = phone['spec']
            ram = spec['ram']
            camera = spec['camera']
            storage = spec['storage']

        cur.execute("INSERT into emp(idNumbers,name,age,sex,maritalStatus,dateOfBirth) VALUES(%s,%s,%s,%s,%s,%s)",
         (idNumbers, name, age, sex, maritalStatus, dateOfBirth))

        cur.execute("INSERT into laptop(idNumbers,ram,ssd,storage,screenSize,speed) VALUES(%s,%s,%s,%s,%s,%s) ",
                    (idNumbers, ram, ssd, storage, screenSize, speed))

        cur.execute("INSERT into phones(idNumbers, model, price, imei) VALUES(%s, %s, %s, %s)",
                    (idNumbers, model, price, imei))

        cur.execute("INSERT into spec(idNumbers,ram, camera, storage) VALUES(%s, %s, %s, %s)",
                    (idNumbers, ram, camera, storage))    
    mysql.connection.commit()

    cur.close()



@app.route("/list", methods=['GET'])

def get_users():

    if request.method == 'GET':
        cur = mysql.connection.cursor()
        statement = "SELECT * from emp join laptop on emp.idNumbers =laptop.idNumbers join phones on laptop.idNumbers = phones.idNumbers;"
       
        result = cur.execute(statement)

        userdata = []
        status = 1
        message = "No records found"

        if result > 0:
            status = 0
            userdata = cur.fetchall()
            message ="data found successfully"

            return jsonify({"status":status, "message":message, "userdata":userdata})

@app.route("/list/<int:idNumbers>", methods=["GET"])

def get_one_user(idNumbers):
     if request.method == 'GET':
         
            cur = mysql.connection.cursor()
            statement = """select a.*, b.*, c.*, d.* from emp as a join laptop as b on a.idNumbers = b.idNumbers join phones as c where a.idNumbers = c.idNumbers join specs as d where a.idNumbers = d.idNumbers where a.idNumbers = '{}' """.format(id)

            #statement =  ("select a.*, b.*, c.*, d.* from (select * from emp) as a join (select * from laptop) as b on a.idNumbers = b.idNumbers join (select * from phones) as c on c.idNumbers =  a.idNumbers join(select * from specs) as d on d.idNumbers = a.idNumbers")
            #statement = (" select * from emp  where idNumbers= '{}' ".format(idNumbers))
            #statement = ("SELECT * from emp laptop join emp.idNumbers =laptop.idNumbers "
            #statement = ("SELECT * from emp join laptop on emp.idNumbers =laptop.idNumbers join phones on laptop.idNumbers = phones.idNumbers join specs on phones.idNumbers = specs.idNumbers where idNumbers= '{}' ".format(idNumbers))

            result = cur.execute(statement)

            data = []
            status = 1
            message = "No user found"

            if result > 0: 
                status = 0
                data = cur.fetchall()
                message ="User data found"

            return jsonify({"status":status, "message":message, "data":data})

            
        




if __name__=="__main__":
     app.run(debug=True)


       




