import streamlit as st
import json
import speech_recognition as sr
import av
import numpy as np
import tempfile
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase, ClientSettings

# Load product database
with open("database.json", "r") as f:
    products = json.load(f)["products"]

# Utility: Find product from spoken text
def find_product(query):
    query = query.lower()
    for product in products:
        for keyword in product["keywords"]:
            if keyword in query:
                return product
    return None

# WebRTC audio processor to save audio to file
class AudioProcessor(AudioProcessorBase):
    def __init__(self):
        self.frames = []

    def recv(self, frame: av.AudioFrame) -> av.AudioFrame:
        pcm = frame.to_ndarray().flatten()
        self.frames.append(pcm)
        return frame

    def get_audio_data(self):
        return np.concatenate(self.frames, axis=0) if self.frames else None

st.set_page_config(page_title="Voice Inventory Assistant", page_icon="🛍️")
st.title("🛍️ Voice Inventory Assistant")

st.write("🎙️ Click below and say a product name (e.g. *red shoes*, *blue jeans*, *t-shirt*).")

ctx = webrtc_streamer(
    key="example",
    mode="SENDRECV",
    client_settings=ClientSettings(
        media_stream_constraints={"video": False, "audio": True},
        rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
    ),
    audio_processor_factory=AudioProcessor,
)

if ctx.audio_processor:
    if st.button("🔍 Process Voice"):
        st.info("Processing...")

        audio_data = ctx.audio_processor.get_audio_data()
        if audio_data is None:
            st.error("No audio data received.")
        else:
            # Save audio to temp WAV file
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
                import wave
                wf = wave.open(f.name, "wb")
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(16000)
                wf.writeframes(audio_data.astype(np.int16).tobytes())
                wf.close()

                # Recognize speech
                recognizer = sr.Recognizer()
                with sr.AudioFile(f.name) as source:
                    audio = recognizer.record(source)
                    try:
                        text = recognizer.recognize_google(audio)
                        st.success(f"You said: \"{text}\"")
                        product = find_product(text)
                        if product:
                            st.success(f"Redirecting to: {product['name']}")
                            st.markdown(f"[🔗 View Product]({product['url']})")
                        else:
                            st.warning("Product not found.")
                    except sr.UnknownValueError:
                        st.error("Sorry, couldn't understand the speech.")
                    except sr.RequestError as e:
                        st.error(f"Speech Recognition error: {e}")
