import streamlit as st
from streamlit_chat import message as st_message
from transformers import BlenderbotTokenizer, BlenderbotForConditionalGeneration ,MarianMTModel, MarianTokenizer
import torch
import streamlit_webrtc as webrtc_streamer
import soundfile as sf
@st.cache_resource 
def get_models_chat():
	# it may be necessary for other frameworks to cache the model
	# seems pytorch keeps an internal state of the conversation
	model_name = "facebook/blenderbot-400M-distill"
	tokenizer = BlenderbotTokenizer.from_pretrained(model_name)
	model = BlenderbotForConditionalGeneration.from_pretrained(model_name)
	return tokenizer, model
@st.cache_resource 
def get_models_vi_en():
	# it may be necessary for other frameworks to cache the model
	# seems pytorch keeps an internal state of the conversation
	model_name = "Helsinki-NLP/opus-mt-vi-en"
	model = MarianMTModel.from_pretrained(model_name)
	tokenizer = MarianTokenizer.from_pretrained(model_name)
	return tokenizer, model
@st.cache_resource
def get_models_en_vi():
	# it may be necessary for other frameworks to cache the model
	# seems pytorch keeps an internal state of the conversation
	model_name = "Helsinki-NLP/opus-mt-en-vi"
	model = MarianMTModel.from_pretrained(model_name)
	tokenizer = MarianTokenizer.from_pretrained(model_name)
	return tokenizer, model

if "history" not in st.session_state:
	st.session_state.history = []

st.title("Hello Chatbot")

def translate_vi_en(text):
		# Load the model and tokenizer
		tokenizer,model = get_models_vi_en()
		# Tokenize the input text
		input_ids = tokenizer.encode(text, return_tensors="pt")

		# Translate the input text using the model
		translated = model.generate(input_ids)

		# Decode the translated output and print it
		output = tokenizer.decode(translated[0], skip_special_tokens=True)
		return output
def translate_en_vi(text):
		tokenizer,model = get_models_en_vi()
		# Tokenize the input text
		input_ids = tokenizer.encode(text, return_tensors="pt")
		# Translate the input text using the model
		translated = model.generate(input_ids)
		# Decode the translated output and print it
		output = tokenizer.decode(translated[0], skip_special_tokens=True)
		return output
def voice(input_text):
	webrtc_ctx = webrtc_streamer(
            audio=True,
            key="audio",
            constraints={
                "audio": True,
                "video": False
            }
        )

	# Add a microphone icon to start recording audio
	if not webrtc_ctx.state.playing:
		btn = st.button("Start Recording")
		if btn:
			webrtc_ctx.start()
	else:
		st.write("Recording...")

		# Stop recording and save the audio as a WAV file
		stop_btn = st.button("Stop Recording")
		if stop_btn:
			webrtc_ctx.stop()

			# Get the recorded audio data as a numpy array
			audio_data = webrtc_ctx.audio_receiver.get_frame()

			# Convert the audio data to a WAV file
			filename = "recorded_audio.wav"
			sf.write(filename, audio_data, webrtc_ctx.audio_receiver.audio_info.samplerate)
			st.write(f"Saved audio file to {filename}")

			# Send the recorded audio to the speech-to-text API to generate an answer
			# You can replace this with your own code to generate an answer from the recorded audio
			answer = "You said: " + input_text
			return answer
def generate_answer():
	tokenizer, model = get_models_chat()
	user_message = st.session_state.input_text
	if  user_message.lower() == "/record_audio":
		result= voice(user_message)
	else:
		result = user_message

	user_message_en = translate_vi_en(result)
	inputs = tokenizer(user_message_en, return_tensors="pt")
	result = model.generate(**inputs)
	message_bot = tokenizer.decode(
		result[0], skip_special_tokens=True
	)  # .replace("<s>", "").replace("</s>", "")
	message_bot_vn = translate_en_vi(message_bot)
	st.session_state.history.append({"message": result, "is_user": True})
	st.session_state.history.append({"message": message_bot_vn, "is_user": False})
	st.session_state.input_text = ""



st.text_input("Talk to the bot", key="input_text", on_change=generate_answer)

for chat in st.session_state.history:
	st_message(**chat)  # unpacking