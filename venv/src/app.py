from flask import Flask, request, jsonify
from flask_pymongo import PyMongo, ObjectId
from flask_cors import CORS

app = Flask(__name__)
app.config['MONGO_URI']='mongodb+srv://new:test@cluster0.zlwt9lm.mongodb.net/tdl'
mongo = PyMongo(app)

CORS(app)

db = mongo.db.users

@app.route('/users', methods=['POST'] )
def createUser():
    id = db.insert_one({
        'title': request.json['title'],
        'desc': request.json['desc']
        
    }).inserted_id
    print(id)
    return jsonify({'id': str((ObjectId(id))),'msg': "Task Added Successfully"})

@app.route('/users', methods=['GET'] )
def getUsers():
    users = []
    for doc in db.find():
        users.append({
            '_id': str(ObjectId(doc['_id'])),
            'title':doc['title'],
            'desc': doc['desc']
        })
    return jsonify(users)

@app.route('/user/<id>', methods=['GET'])
def getUser(id):
    user=db.find_one({'_id': ObjectId(id)})
    return jsonify({
            '_id': str(ObjectId(user['_id'])),
            'title':user['title'],
            'desc': user['desc']
        })

@app.route('/user/<id>', methods=['DELETE'])
def deleteUser(id):
    db.delete_one({'_id': ObjectId(id)})
    return jsonify({
            'msg': "Task Deleted Successfully"
            
        })

@app.route('/user/<id>', methods=['PUT'])
def updateUser(id):
    db.update_one({'_id': ObjectId(id)},{'$set':{
        'title': request.json['title'],
        'desc': request.json['desc']
        
    }})
    return jsonify({
            'msg': "Task Updated Successfully"
            
        })

if __name__ == '__main__':
    app.run(host = 'localhost',port="8088", debug=True)