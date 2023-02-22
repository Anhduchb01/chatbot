from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS, cross_origin
from chatpredict import predict
app = Flask(__name__)
from translate import translate_vi_en,translate_en_vi
from voicepredict import predictVoice
from testvoice import predictvoice1
import mimetypes
import soundfile as sf
import io
from werkzeug.utils import secure_filename
import os
from pydub import AudioSegment
import numpy as np
import wave
from scipy.io import wavfile
import librosa
import array
app.config['UPLOAD_FOLDER'] = os.path.join(
    app.instance_path, 
    'uploads'
)
try: 
    os.makedirs(app.config['UPLOAD_FOLDER'])
except: 
    pass 
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
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
    # file = request.files.get('audio')
    # if file and file.filename != '': 
    #     dest = os.path.join(
    #         app.config['UPLOAD_FOLDER'], 
    #         secure_filename(file.filename)
    #     )
    #     # Save the file on the server.
    #     file.save(dest)
        
    #     # Load the file by filename using librosa.
    #     y,sr = librosa.load(dest)
    #     print('y',y)
    #     print('sr',sr)
        
    # print('ok')
    audio = request.files['audio']
    print(audio)
    # chunk_size = 1024  # read 1KB at a time
    # audio_data = bytearray()
    # while True:
    #     chunk = audio.read(chunk_size)
    #     if not chunk:
    #         break
    #     audio_data.extend(chunk)

    audio_file = io.BytesIO(audio.read())
    audio_data = AudioSegment.from_file(audio_file, format='raw', frame_rate=16000, channels=1, sample_width=1)
    print(audio_data)
    # output_file = "audio-test/output.wav"

# export the audio data to a WAV file
    # audio_data.export(output_file, format="wav")
    # get audio data as numpy array
    # ok = sf.read(audio_data)
    print(audio_data.sample_width)
    numpy_data = audio_data.get_array_of_samples()
    int_data = array.array('i', numpy_data).tolist()
    print(int_data)
    normalized_data = np.array(int_data) / (2**7)
    print(normalized_data)
# convert audio data to float64 type
    float_data = normalized_data.astype(np.float64)
    print(float_data)
    print(float_data.shape)
    transcription = predictvoice1(float_data)
    print(transcription)
    response = {"message": 'ok'}
    return jsonify(response)

if __name__ =='__main__':
          app.run(host='0.0.0.0',port='3000')