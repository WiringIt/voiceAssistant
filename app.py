import streamlit as st
import json
import speech_recognition as sr
import av
import numpy as np
import tempfile
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase, WebRtcMode, RTCConfiguration

# Load product DB
with open("database.json") as f:
    products = json.load(f)["products"]

def find_product(query):
    q = query.lower()
    return next((p for p in products if any(k in q for k in p["keywords"])), None)

class AudioProcessor(AudioProcessorBase):
    def __init__(self):
        self.frames = []

    def recv(self, frame: av.AudioFrame) -> av.AudioFrame:
        self.frames.append(frame.to_ndarray().flatten())
        return frame

    def get_audio_data(self):
        if not self.frames:
            return None
        return np.concatenate(self.frames)

st.title("🛍️ Voice Inventory Assistant")

rtc_conf = RTCConfiguration({"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})

ctx = webrtc_streamer(
    key="voice-assistant",
    mode=WebRtcMode.SENDRECV,
    rtc_configuration=rtc_conf,
    client_settings=None,
    audio_processor_factory=AudioProcessor,
)

if ctx.audio_processor and st.button("🎤 Process Voice"):
    st.info("Transcribing...")
    data = ctx.audio_processor.get_audio_data()
    if data is None:
        st.error("No audio captured.")
    else:
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            import wave
            wf = wave.open(tmp.name, "wb")
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(16000)
            wf.writeframes(data.astype(np.int16).tobytes())
            wf.close()

            recognizer = sr.Recognizer()
            with sr.AudioFile(tmp.name) as src:
                audio = recognizer.record(src)
                try:
                    text = recognizer.recognize_google(audio)
                    st.success(f"You said: {text}")
                    prod = find_product(text)
                    if prod:
                        st.markdown(f"**Found:** {prod['name']} — [View product]({prod['url']})")
                    else:
                        st.warning("Product not found.")
                except sr.UnknownValueError:
                    st.error("Couldn't understand.")
                except sr.RequestError as e:
                    st.error(f"Recognition error: {e}")
