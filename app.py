import streamlit as st
import json
import speech_recognition as sr
import av, numpy as np, tempfile
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase, WebRtcMode

# Load dummy product DB
with open("database.json") as f:
    products = json.load(f)["products"]

def find_product(q):
    q = q.lower()
    for p in products:
        if any(k in q for k in p["keywords"]):
            return p
    return None

class AudioProcessor(AudioProcessorBase):
    def __init__(self):
        self.frames = []
    def recv(self, frame: av.AudioFrame) -> av.AudioFrame:
        self.frames.append(frame.to_ndarray().flatten())
        return frame
    def get_audio(self):
        return np.concatenate(self.frames) if self.frames else None

st.title("🛍️ Voice Inventory Assistant")

ctx = webrtc_streamer(key="voice", mode=WebRtcMode.SENDRECV, audio_receiver_size=256, audio_processor_factory=AudioProcessor)

if ctx.audio_receiver and st.button("🔍 Process Voice"):
    st.info("🎧 Transcribing...")
    data = ctx.audio_processor.get_audio()
    if data is None:
        st.error("No audio captured.")
    else:
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            wf = av.open(tmp.name, mode='w')
            stream = wf.add_stream("pcm_s16le", rate=16000)
            stream.layout = "mono"
            for chunk in np.array_split(data, len(data)//16000):
                frame = av.AudioFrame.from_ndarray(chunk.reshape(-1,1), format="s16", layout="mono")
                for pkt in stream.encode(frame):
                    wf.mux(pkt)
            wf.close()

        r = sr.Recognizer()
        with sr.AudioFile(tmp.name) as src:
            audio = r.record(src)
        try:
            text = r.recognize_google(audio)
            st.success(f"You said: {text}")
            p = find_product(text)
            if p:
                st.markdown(f"✅ **Found:** {p['name']} — [View]({p['url']})")
            else:
                st.warning("No matching product.")
        except sr.UnknownValueError:
            st.error("Could not understand audio.")
        except sr.RequestError as e:
            st.error(f"Recognition error: {e}")
