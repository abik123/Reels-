import streamlit as st
import assemblyai as aai
import os

# Set AssemblyAI API key
aai.settings.api_key = "bdd3381c1ebe4ecab9df5207a255d42e"

# Function to transcribe audio
def transcribe_audio(audio_file):
    transcriber = aai.Transcriber()
    config = aai.TranscriptionConfig(speaker_labels=True)
    
    try:
        with open(audio_file, "rb") as f:
            transcript = transcriber.transcribe(f, config)
        
        if transcript.status == aai.TranscriptStatus.error:
            st.error(f"Transcription failed: {transcript.error}")
            return None
        return transcript
    except Exception as e:
        st.error(f"Transcription error: {e}")
        return None

# Streamlit UI
st.title("Audio Transcription Tool")

uploaded_file = st.file_uploader("Upload an audio file (MP3/WAV)", type=["mp3", "wav"])

if uploaded_file:
    st.write("Transcribing audio...")
    
    # Save the uploaded file temporarily
    audio_file = "uploaded_audio.wav"
    with open(audio_file, "wb") as f:
        f.write(uploaded_file.read())
    
    # Transcribe
    transcript = transcribe_audio(audio_file)
    
    if transcript:
        st.success("Transcription Completed!")
        st.text_area("Transcript:", transcript.text)
        
        st.write("Speaker-wise transcription:")
        for utterance in transcript.utterances:
            st.write(f"Speaker {utterance.speaker}: {utterance.text}")
    
    # Clean up
    if os.path.exists(audio_file):
        os.remove(audio_file)
