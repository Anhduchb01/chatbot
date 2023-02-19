from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS, cross_origin
from chatpredict import predict
app = Flask(__name__)
from translate import translate_vi_en,translate_en_vi
from voicepredict import predictVoice
from testvoice import predict
import mimetypes
import soundfile as sf
import io
from werkzeug.utils import secure_filename
import os
from pydub import AudioSegment
app.config['UPLOAD_FOLDER']=r'C:\Users\Admin\Desktop\PROJECT III\chatbot\vue-chat-api\audio-test'
@app.route("/")
# @cross_origin(origin='*')
def hello_world():

    return "<p>Hello, World!</p>"

@app.route("/predict")
@cross_origin(origin='*')
def predictchat():
    messageVN = request.args.get('text')
    messageEN = translate_vi_en(messageVN)
    outputEN = predict(messageEN)
    outputVN = translate_en_vi(outputEN)
    return jsonify({'output':outputVN})

@app.route("/predictVoice",methods=['POST'])
@cross_origin(origin='*')
def predictvoice():
    file = request.files["file"]
    print(file)
    print('ok')
    transcription = predictVoice(file)
    response = {"message": transcription}
    return jsonify(response)


@app.route("/predictTest",methods=['POST'])
@cross_origin()
def predictvoiceTest():
    print('ok')
    file = request.files['file']
    # determine format of uploaded file based on MIME type
    # file_mime_type = mimetypes.guess_type(file.filename)[0]
    # if file_mime_type == 'audio/wav':
    #     file_format = 'WAV'
    # elif file_mime_type == 'audio/flac':
    #     file_format = 'FLAC'
    # elif file_mime_type == 'audio/ogg':
    #     file_format = 'OGG'
    # else:
    #     # unrecognized file format
    #     return jsonify({'error': 'Unrecognized file format'})
    # # read audio data from uploaded file using soundfile
    # print(file)
    # print(file_format)
    # with io.BytesIO() as f:
    #     file.save(f)
    #     f.seek(0)
    #     data, samplerate = sf.read(f, format=file_format)
    # file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'audio1.webm'))
    print(file)
    webm_file = os.path.join(app.config['UPLOAD_FOLDER'], 'audio1.webm')
    audio = AudioSegment.from_file(file, format="wav")
    print(audio)
    # Convert the WebM file to WAV format
    wav_file = os.path.join(app.config['UPLOAD_FOLDER'], 'audio2.wav')
    audio.export(wav_file, format="wav")
    data, samplerate = sf.read(audio)
    print(data)
    transcription = predict(data)
    
    response = {"message": transcription}
    return jsonify(response)

if __name__ =='__main__':
          app.run(host='0.0.0.0',port='3000')