from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS, cross_origin
from chatpredict import predict
app = Flask(__name__)
from translate import translate_vi_en,translate_en_vi
@app.route("/")
# @cross_origin(origin='*')
def hello_world():

    return "<p>Hello, World!</p>"
@app.route("/predict")
@cross_origin(origin='*')
# @cross_origin(origin='*')
def predictchat():
    messageVN = request.args.get('text')
    messageEN = translate_vi_en(messageVN)
    outputEN = predict(messageEN)
    outputVN = translate_en_vi(outputEN)
    return jsonify({'output':outputVN})

if __name__ =='__main__':
          app.run(host='0.0.0.0',port='3000')