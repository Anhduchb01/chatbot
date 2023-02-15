import torch
from transformers import Wav2Vec2ForCaptioning, Wav2Vec2Tokenizer,Wav2Vec2Model
import soundfile as sf

# Load the model and tokenizer
model = Wav2Vec2ForCaptioning.from_pretrained("facebook/wav2vec2-base-960h")
tokenizer = Wav2Vec2Tokenizer.from_pretrained("facebook/wav2vec2-base-960h")

# Read the audio file
audio, sr = sf.read("/home/anhduc/Project/Project3/voice/backend/test.wav")

preprocessed_audio = torch.tensor(audio).unsqueeze(0).unsqueeze(1)

# Encode the audio
encoded_audio = tokenizer(preprocessed_audio, return_tensors="pt")

# Perform ASR
output = model(**encoded_audio)

# Decode the output
decoded_output = tokenizer.decode(output[0], skip_special_tokens=True)

print(decoded_output)
