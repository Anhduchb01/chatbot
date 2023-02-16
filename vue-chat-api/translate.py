from transformers import MarianMTModel, MarianTokenizer

def translate_vi_en(text):
# Load the model and tokenizer
        model_name = "Helsinki-NLP/opus-mt-vi-en"
        model = MarianMTModel.from_pretrained(model_name)
        tokenizer = MarianTokenizer.from_pretrained(model_name)

        # Tokenize the input text
        input_ids = tokenizer.encode(text, return_tensors="pt")

        # Translate the input text using the model
        translated = model.generate(input_ids)

        # Decode the translated output and print it
        output = tokenizer.decode(translated[0], skip_special_tokens=True)
        return output
def translate_en_vi(text):
        model_name = "Helsinki-NLP/opus-mt-en-vi"
        model = MarianMTModel.from_pretrained(model_name)
        tokenizer = MarianTokenizer.from_pretrained(model_name)

        # Tokenize the input text
        input_ids = tokenizer.encode(text, return_tensors="pt")

        # Translate the input text using the model
        translated = model.generate(input_ids)

        # Decode the translated output and print it
        output = tokenizer.decode(translated[0], skip_special_tokens=True)
        return output