import streamlit as st
import json
import tempfile
import numpy as np
import wave
import av
import webbrowser
import speech_recognition as sr
from difflib import get_close_matches
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase, WebRtcMode

# Load dummy product database
with open("database.json", "r") as f:
    products = json.load(f)["products"]

# Build keyword map for fuzzy match
keyword_map = {k: p for p in products for k in p["keywords"]}

def find_product_fuzzy(query):
    query = query.lower()
    matches = get_close_matches(query, keyword_map.keys(), n=1, cutoff=0.5)
    if matches:
        return keyword_map[matches[0]]
    return None

# Audio processing class
class VoiceProcessor(AudioProcessorBase):
    def __init__(self):
        self.frames = []

    def recv(self, frame: av.AudioFrame) -> av.AudioFrame:
        audio = frame.to_ndarray()[0]  # Mono channel
        audio_int16 = (audio * 32767).astype(np.int16)
        self.frames.append(audio_int16)
        return frame

    def get_audio(self):
        if not self.frames:
            return None
        return np.concatenate(self.frames)

# UI Setup
st.set_page_config(page_title="Voice Inventory Assistant", page_icon="🛍️")
st.title("🛍️ Voice Inventory Assistant")
st.write("🎙️ Click 'Start Recording', speak a product name, then click 'Process Voice'.")

# WebRTC Audio Recorder
ctx = webrtc_streamer(
    key="voice-input",
    mode=WebRtcMode.SENDRECV,
    audio_processor_factory=VoiceProcessor,
    media_stream_constraints={"video": False, "audio": True},
)

# Handle voice-to-product flow
if ctx.audio_processor:
    if st.button("🔍 Process Voice"):
        audio_data = ctx.audio_processor.get_audio()
        if audio_data is None:
            st.error("No audio received.")
        else:
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmpfile:
                with wave.open(tmpfile.name, 'wb') as wf:
                    wf.setnchannels(1)
                    wf.setsampwidth(2)
                    wf.setframerate(16000)
                    wf.writeframes(audio_data.tobytes())

                st.audio(tmpfile.name, format='audio/wav')

                recognizer = sr.Recognizer()
                with sr.AudioFile(tmpfile.name) as source:
                    audio = recognizer.record(source)

                try:
                    query = recognizer.recognize_google(audio)
                    st.success(f"You said: **{query}**")

                    # Optional fallback to editable input
                    edited_query = st.text_input("Edit if needed:", value=query)

                    product = find_product_fuzzy(edited_query)
                    if product:
                        st.success(f"Matched Product: {product['name']}")
                        st.markdown(f"[🔗 Go to Product Page]({product['url']})")
                        webbrowser.open_new_tab(product['url'])
                    else:
                        st.warning("❌ No matching product found.")

                except sr.UnknownValueError:
                    st.error("Couldn't understand your voice.")
                except sr.RequestError as e:
                    st.error(f"Google STT error: {e}")
