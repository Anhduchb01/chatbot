from transformers import BlenderbotTokenizer, BlenderbotForConditionalGeneration
import torch
model_blender = BlenderbotForConditionalGeneration.from_pretrained("facebook/blenderbot-400M-distill")
tokenizer_blender = BlenderbotTokenizer.from_pretrained("facebook/blenderbot-400M-distill")

def predict(message):
          inputs = tokenizer_blender([message], return_tensors='pt')
          reply_ids = model_blender.generate(**inputs)
          output = tokenizer_blender.batch_decode(reply_ids, skip_special_tokens=True)[0]
          print(f"Blenderbot 2.0 response:     {output}")
          return output