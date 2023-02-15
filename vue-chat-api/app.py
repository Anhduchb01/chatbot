from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS, cross_origin
from chatpredict import predict
app = Flask(__name__)

@app.route("/")
# @cross_origin(origin='*')
def hello_world():

    return "<p>Hello, World!</p>"
@app.route("/predict")
@cross_origin(origin='*')
# @cross_origin(origin='*')
def predictchat():
    message = request.args.get('text')
    output = predict(message)
    return jsonify({'output':output})

if __name__ =='__main__':
          app.run(host='0.0.0.0',port='3000')