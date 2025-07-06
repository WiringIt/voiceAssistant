import streamlit as st
import speech_recognition as sr
import json
import webbrowser

st.set_page_config(page_title="Voice Inventory Assistant", page_icon="🛍️")

st.title("🛍️ Voice Inventory Assistant")
st.write("Click below to speak and get product recommendations.")

# Load product database
with open("database.json", "r") as f:
    products = json.load(f)["products"]

def find_product(query):
    query = query.lower()
    for product in products:
        for keyword in product["keywords"]:
            if keyword in query:
                return product
    return None

if st.button("🎙️ Speak Now"):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening...")
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio)
            st.success(f"You said: {text}")
            product = find_product(text)
            if product:
                st.success(f"Redirecting to: {product['name']}")
                webbrowser.open_new_tab(product["url"])
            else:
                st.error("Product not found in inventory.")
        except sr.WaitTimeoutError:
            st.error("No speech detected. Try again.")
        except sr.UnknownValueError:
            st.error("Could not understand audio.")
        except Exception as e:
            st.error(f"Error: {e}")
