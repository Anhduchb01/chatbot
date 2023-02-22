# !pip install transformers
# !pip install datasets
import soundfile as sf
import torch
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor

processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-base-960h")
model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")


def predictVoice(file):
    try :
    
        audio_input, sample_rate = sf.read(file)
    except:
        print('error')
        audio_input, sample_rate = sf.read('testflac.flac')
    

# pad input values and return pt tensor
    print(audio_input)
    input_values = processor(audio_input, sampling_rate=sample_rate, return_tensors="pt").input_values

    # retrieve logits & take argmax
    logits = model(input_values).logits
    predicted_ids = torch.argmax(logits, dim=-1)

    # transcribe
    transcription = processor.decode(predicted_ids[0])
    return transcription

