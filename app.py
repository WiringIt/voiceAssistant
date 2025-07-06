import streamlit as st
import json
import tempfile
import numpy as np
import av
import wave
import webbrowser
import speech_recognition as sr
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase, WebRtcMode

# Load product database
with open("database.json", "r") as f:
    products = json.load(f)["products"]

def find_product(query):
    query = query.lower()
    for product in products:
        if any(keyword in query for keyword in product["keywords"]):
            return product
    return None

class VoiceProcessor(AudioProcessorBase):
    def __init__(self) -> None:
        self.frames = []

    def recv(self, frame: av.AudioFrame) -> av.AudioFrame:
        self.frames.append(frame.to_ndarray().flatten())
        return frame

    def get_audio(self):
        if not self.frames:
            return None
        return np.concatenate(self.frames)

st.set_page_config(page_title="🛍️ Voice Assistant", page_icon="🗣️")
st.title("🗣️ Voice Inventory Assistant")

ctx = webrtc_streamer(
    key="speech",
    mode=WebRtcMode.SENDRECV,
    audio_processor_factory=VoiceProcessor,
    media_stream_constraints={"video": False, "audio": True},
)

if ctx.audio_processor:
    st.info("🎙️ Speak your product name and then click below.")
    if st.button("🔍 Process and Redirect"):
        st.info("Processing voice...")

        raw_audio = ctx.audio_processor.get_audio()

        if raw_audio is None:
            st.error("No audio captured.")
        else:
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
                with wave.open(f.name, 'wb') as wf:
                    wf.setnchannels(1)
                    wf.setsampwidth(2)
                    wf.setframerate(16000)
                    wf.writeframes(raw_audio.astype(np.int16).tobytes())

                recognizer = sr.Recognizer()
                with sr.AudioFile(f.name) as source:
                    audio = recognizer.record(source)

                try:
                    text = recognizer.recognize_google(audio)
                    st.success(f"You said: {text}")
                    matched_product = find_product(text)
                    if matched_product:
                        st.success(f"Product matched: {matched_product['name']}")
                        st.markdown(f"[Click here to go to the product page 🚀]({matched_product['url']})")
                        webbrowser.open_new_tab(matched_product["url"])
                    else:
                        st.warning("Sorry, no matching product found.")
                except sr.UnknownValueError:
                    st.error("Could not understand the audio.")
                except sr.RequestError as e:
                    st.error(f"Could not request results from Google Speech API: {e}")
