import io
import speech_recognition as sr
import streamlit as st
from streamlit_mic_recorder import mic_recorder

# Page configuration
st.set_page_config(page_title="Myanmar Speech-to-Text", page_icon="🎙️")

st.title("🎙️ Myanmar Speech-to-Text (မြန်မာ အသံမှ စာသားသို့)")
st.write(
    "Click the button below to start recording in Burmese, or upload a WAV audio"
    " file."
)

# Initialize the recognizer
recognizer = sr.Recognizer()


def transcribe_myanmar(audio_bytes):
  """Transcribes WAV audio bytes into Myanmar text."""
  try:
    # Wrap bytes in a file-like object
    audio_file = io.BytesIO(audio_bytes)
    with sr.AudioFile(audio_file) as source:
      audio_data = recognizer.record(source)

    # Recognize speech using Google Web Speech API with Myanmar locale ('my-MM')
    text = recognizer.recognize_google(audio_data, language="my-MM")
    return text, None
  except sr.UnknownValueError:
    return (
        None,
        (
            "အသံကို နားမလည်နိုင်ပါ။ ကျေးဇူးပြု၍ ထပ်မံကြိုးစားပါ။ (Could not"
            " understand the audio.)"
        ),
    )
  except sr.RequestError as e:
    return None, f"API ချိတ်ဆက်မှု အမှားအယွင်းရှိနေပါသည်: {e}"
  except Exception as e:
    return None, f"Error processing audio: {e}"


# --- Option 1: Live Microphone Recording ---
st.subheader("1. Record from Microphone")
audio = mic_recorder(
    start_prompt="🎤 စတင်အသံသွင်းမည် (Start Recording)",
    stop_prompt="⏹️ ရပ်တန့်မည် (Stop Recording)",
    just_once=False,
    use_container_width=True,
    format="wav",
    key="recorder",
)

if audio is not None:
  st.audio(audio["bytes"], format="audio/wav")
  with st.spinner("စာသားပြောင်းလဲနေပါသည်... (Transcribing...)"):
    text, error = transcribe_myanmar(audio["bytes"])
    if text:
      st.success("ရလဒ် (Result):")
      st.text_area("Transcribed Myanmar Text", value=text, height=150)
    elif error:
      st.error(error)

st.divider()

# --- Option 2: Upload Audio File ---
st.subheader("2. Upload WAV File")
uploaded_file = st.file_uploader("Upload a .wav audio file", type=["wav"])

if uploaded_file is not None:
  st.audio(uploaded_file, format="audio/wav")
  if st.button("Transcribe Uploaded File"):
    with st.spinner("စာသားပြောင်းလဲနေပါသည်... (Transcribing...)"):
      text, error = transcribe_myanmar(uploaded_file.read())
      if text:
        st.success("ရလဒ် (Result):")
        st.text_area("Transcribed File Text", value=text, height=150)
      elif error:
        st.error(error)
