import torch
from transformers import Wav2Vec2Model, Wav2Vec2Config
from flask import Flask, jsonify, request
from pydub import AudioSegment
from flask_cors import cross_origin
import soundfile as sf
from werkzeug.utils import secure_filename

import os
import torch
from transformers import Wav2Vec2ForCaptioning, Wav2Vec2Tokenizer
import soundfile as sf
app = Flask(__name__)

# Load the model
import torch
from transformers import GPT2Tokenizer, GPT2LMHeadModel
app.config['UPLOAD_FOLDER']='/home/anhduc/Project/Project3/voice/backend'
# Load the models
base_model = Wav2Vec2Model.from_pretrained('facebook/wav2vec2-large-960h-lv60-self')
base_model.eval()
model = GPT2LMHeadModel.from_pretrained("gpt2")
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model.eval()
def read_audio(audio_file, desired_sample_rate=16000):
    # Get the audio file and read it
    if audio_file.filename == '':
        return jsonify("No audio file selected")
    if audio_file :
        filename = secure_filename(audio_file.filename)
        audio_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        try:
            # audio = AudioSegment.from_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), format='wav')
            # audio = AudioSegment.from_file('/home/anhduc/Project/Project3/voice/backend/test.wav', format='wav')
            audio, sr = sf.read("/home/anhduc/Project/Project3/voice/backend/test.wav")
            print(audio)

# Preprocess the audio to match the model's input format
            # audio = audio.tolist()
        except Exception as e:
            print("Error: Not a wav file")
            return jsonify("Error: Not a wav file")
    # resampling
    # audio = audio.set_frame_rate(desired_sample_rate).set_channels(1)
    # audio = audio.get_array_of_samples()
    audio = torch.tensor(audio, dtype=torch.float)
    # audio = audio.view(1, -1)
    return audio
@app.route('/embed', methods=['POST'])
@cross_origin()
def embed():
    # Get the audio file from the request
    audio_file = request.files['audio_file']
    print(audio_file)
    input_tensor = read_audio(audio_file)
    # Use the wav2vec2 model to generate embeddings for the input
    with torch.no_grad():
        embeddings, _ = base_model(input_tensor)
        #Converting the wav2vec2 outputs to the format that gpt2 model can understand
        input_ids = tokenizer.encode(embeddings[0], return_tensors="pt")
   
    generated_text = model.generate(input_ids)
    generated_text = tokenizer.decode(generated_text[0], skip_special_tokens=True)
    print('text is',generated_text)
    print('-------------------------')
    return jsonify({'text': generated_text})

if __name__ == '__main__':
    app.run(debug=True)