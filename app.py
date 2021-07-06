from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)

db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

class Employee(db.Model):
     idNumbers = db.Column(db.Integer(), primary_key=True)
     name = db.Column(db.String(50))
     age = db.Column(db.Integer())
     sex = db.Column(db.String(10))
     maritalStatus = db.Column(db.String(50))
     dateOfBirth = db.Column(db.Integer())
     

app = Flask(__name__)

@app.route('/', methods=['GET'])

def get_users():

     r = requests.get('http://richardobiye.com/py/api/employee.php')

     data = r.json()
     new_user = Employee(idNumbers = data['idNumbers'], name=data['name'], age=data['age'], sex=data['sex'], maritalStatus=data['maritalStatus'])

     db.session.add(new_user)
     
     db.session.commit()

     return jsonify({'message': 'User created'})

   

     



if __name__ =='__main__':
    app.run(debug=True)