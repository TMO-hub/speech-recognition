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
          import io
from pydub import AudioSegment
import speech_recognition as sr
import streamlit as st
from streamlit_mic_recorder import mic_recorder

# Page configuration
st.set_page_config(page_title="Myanmar Speech-to-Text", page_icon="🎙️")

st.title("🎙️ Myanmar Speech-to-Text (မြန်မာ အသံမှ စာသားသို့)")
st.write(
    "Record live audio in Burmese, or upload a WAV/MP3 file to transcribe it."
)

# Initialize the recognizer
recognizer = sr.Recognizer()


def transcribe_audio_data(audio_data_source):
  """Helper function to run recognition on audio data."""
  try:
    with sr.AudioFile(audio_data_source) as source:
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
    text, error = transcribe_audio_data(io.BytesIO(audio["bytes"]))
    if text:
      st.success("ရလဒ် (Result):")
      st.text_area("Transcribed Myanmar Text", value=text, height=150, key="mic_text")
      st.download_button(
          label="📥 Download Transcript (.txt)",
          data=text,
          file_name="myanmar_transcript.txt",
          mime="text/plain",
          key="mic_download",
      )
    elif error:
      st.error(error)

st.divider()

# --- Option 2: Upload Audio File (WAV, MP3, M4A, etc.) ---
st.subheader("2. Upload Audio File (WAV, MP3)")
uploaded_file = st.file_uploader(
    "Upload an audio file", type=["wav", "mp3", "m4a", "ogg"]
)

if uploaded_file is not None:
  st.audio(uploaded_file)

  if st.button("Transcribe Uploaded File"):
    with st.spinner("စာသားပြောင်းလဲနေပါသည်... (Transcribing...)"):
      try:
        # Load audio file using pydub (handles mp3, m4a, wav automatically)
        audio_segment = AudioSegment.from_file(uploaded_file)

        # Export as WAV into an in-memory buffer
        wav_io = io.BytesIO()
        audio_segment.export(wav_io, format="wav")
        wav_io.seek(0)

        # Transcribe the converted WAV buffer
        text, error = transcribe_audio_data(wav_io)

        if text:
          st.success("ရလဒ် (Result):")
          st.text_area(
              "Transcribed File Text", value=text, height=150, key="file_text"
          )
          st.download_button(
              label="📥 Download Transcript (.txt)",
              data=text,
              file_name="myanmar_transcript.txt",
              mime="text/plain",
              key="file_download",
          )
        elif error:
          st.error(error)
      except Exception as e:
        st.error(
            f"Failed to process audio file. Make sure FFmpeg is installed."
            f" Error: {e}"
        )
          
