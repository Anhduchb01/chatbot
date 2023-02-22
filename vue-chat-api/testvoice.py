from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
import soundfile as sf
import torch
import numpy as np

# load model and tokenizer
processor = Wav2Vec2Processor.from_pretrained("nguyenvulebinh/wav2vec2-base-vietnamese-250h")
model = Wav2Vec2ForCTC.from_pretrained("nguyenvulebinh/wav2vec2-base-vietnamese-250h")

# define function to read in sound file
def map_to_array(batch):
    speech, sample_rate = sf.read(batch["file"])
    print(sample_rate)
    batch["speech"] = speech
    return batch

# load dummy dataset and read soundfiles

def predictvoice1(float_data):
# tokenize
#     ds = map_to_array({
#     "file": 'audio-test/t1_0001-00010.wav'
# })
#     # batch = sf.read('audio-test/t1_0001-00010.wav')
#     print(ds["speech"])
#     print(np.array(ds["speech"]).shape)
    print('predict')
    input_values = processor(float_data,sample_rate=16000, return_tensors="pt", padding="longest").input_values  # Batch size 1

    # retrieve logits
    logits = model(input_values).logits

    # take argmax and decode
    predicted_ids = torch.argmax(logits, dim=-1)
    transcription = processor.batch_decode(predicted_ids)
    print(transcription)
    return transcription