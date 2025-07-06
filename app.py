import streamlit as st
import json
import tempfile
import numpy as np
import wave
import speech_recognition as sr
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase, WebRtcMode
import av

# Load the dummy product database
with open("database.json", "r") as f:
    products = json.load(f)["products"]

# Product matching function
def find_product(query):
    query = query.lower()
    for product in products:
        for keyword in product["keywords"]:
            if keyword in query:
                return product
    return None

# Audio processor to collect frames
class VoiceProcessor(AudioProcessorBase):
    def __init__(self) -> None:
        self.frames = []

    def recv(self, frame: av.AudioFrame) -> av.AudioFrame:
        audio = frame.to_ndarray()
        mono_audio = audio.mean(axis=0).astype(np.int16)
        self.frames.append(mono_audio)
        return frame

    def get_audio(self):
        if not self.frames:
            return None
        return np.concatenate(self.frames)

# Streamlit UI
st.set_page_config(page_title="Voice Assistant", page_icon="🗣️")
st.title("🗣️ Voice Inventory Assistant")
st.write("Click 'Start Recording', speak your product name, then click 'Process'.")

# Setup voice capture
ctx = webrtc_streamer(
    key="speech-to-text",
    mode=WebRtcMode.SENDRECV,
    audio_processor_factory=VoiceProcessor,
    media_stream_constraints={"video": False, "audio": True},
)

# Process voice and redirect
if ctx.audio_processor:
    if st.button("🔍 Process Voice"):
        raw_audio = ctx.audio_processor.get_audio()
        if raw_audio is None:
            st.error("No audio captured. Try again.")
        else:
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmpfile:
                with wave.open(tmpfile.name, "wb") as wf:
                    wf.setnchannels(1)
                    wf.setsampwidth(2)
                    wf.setframerate(16000)
                    wf.writeframes(raw_audio.tobytes())

                recognizer = sr.Recognizer()
                with sr.AudioFile(tmpfile.name) as source:
                    audio_data = recognizer.record(source)
                    try:
                        query = recognizer.recognize_google(audio_data)
                        st.success(f"You said: \"{query}\"")
                        product = find_product(query)
                        if product:
                            st.success(f"Found: {product['name']}")
                            st.markdown(f"[Go to product 🚀]({product['url']})")
                        else:
                            st.warning("No matching product found.")
                    except sr.UnknownValueError:
                        st.error("Couldn't understand the voice.")
                    except sr.RequestError as e:
                        st.error(f"Google STT error: {e}")
