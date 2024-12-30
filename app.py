import streamlit as st
import speech_recognition as sr
from datetime import datetime
import os
import time
import json
import csv

# Initialize session state
if 'transcripts' not in st.session_state:
    st.session_state.transcripts = []
if 'is_recording' not in st.session_state:
    st.session_state.is_recording = False
if 'is_paused' not in st.session_state:
    st.session_state.is_paused = False
if 'current_transcript' not in st.session_state:
    st.session_state.current_transcript = ""

def save_transcript(text, file_format='txt', include_timestamp=True, save_dir='transcripts'):
    try:
        # Create directory if it doesn't exist
        os.makedirs(save_dir, exist_ok=True)
        
        # Generate timestamp
        timestamp = datetime.now()
        timestamp_str = timestamp.strftime('%Y%m%d_%H%M%S')
        
        # Prepare data with timestamp if requested
        if include_timestamp:
            data = {
                'timestamp': timestamp.isoformat(),
                'text': text
            }
        else:
            data = {'text': text}

        # Generate filename based on format
        filename = f"{save_dir}/transcript_{timestamp_str}.{file_format}"
        
        # Save in specified format
        if file_format == 'txt':
            with open(filename, "w", encoding='utf-8') as f:
                if include_timestamp:
                    f.write(f"Timestamp: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write(text)
                
        elif file_format == 'json':
            with open(filename, "w", encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
                
        elif file_format == 'csv':
            with open(filename, "w", newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                if include_timestamp:
                    writer.writerow(['Timestamp', 'Text'])
                    writer.writerow([timestamp.strftime('%Y-%m-%d %H:%M:%S'), text])
                else:
                    writer.writerow(['Text'])
                    writer.writerow([text])
        
        return filename
    except Exception as e:
        st.error(f"Error saving transcript: {str(e)}")
        return None

def transcribe_audio(language='en-US', use_sphinx=False):
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            if not st.session_state.current_transcript:  # Only adjust noise at start
                st.write("Adjusting for ambient noise...")
                recognizer.adjust_for_ambient_noise(source, duration=2)
            
            st.write("🎤 Listening...")
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            
            if use_sphinx:
                text = recognizer.recognize_sphinx(audio)
            else:
                text = recognizer.recognize_google(audio, language=language)
                
            return text
            
    except sr.WaitTimeoutError:
        return None
    except sr.UnknownValueError:
        return None
    except sr.RequestError as e:
        st.error(f"Could not request results; {str(e)}")
        return None
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None

# App layout
st.title("🎤 Speech Recognition App")

# Language and recognition engine selection
col1, col2 = st.columns(2)
with col1:
    language = st.selectbox("Select Language", ["en-US", "fr-FR", "es-ES"])
with col2:
    use_sphinx = st.checkbox("Use Offline Recognition (Sphinx)")

# Recording controls
col1, col2, col3 = st.columns(3)

with col1:
    if not st.session_state.is_recording:
        if st.button("Start Recording"):
            st.session_state.is_recording = True
            st.session_state.is_paused = False
            st.session_state.current_transcript = ""
            st.rerun()
    else:
        if st.button("Stop Recording"):
            st.session_state.is_recording = False
            st.session_state.is_paused = False
            if st.session_state.current_transcript:
                st.session_state.transcripts.append(st.session_state.current_transcript)
            st.rerun()

with col2:
    if st.session_state.is_recording:
        if st.button("Pause/Resume"):
            st.session_state.is_paused = not st.session_state.is_paused
            st.rerun()

# Display current transcript and status
if st.session_state.is_recording:
    st.markdown("### Current Transcript")
    st.write(st.session_state.current_transcript)
    
    if not st.session_state.is_paused:
        text = transcribe_audio(language, use_sphinx)
        if text:
            st.session_state.current_transcript += " " + text
            st.rerun()
        
    status = "🔴 Recording Paused" if st.session_state.is_paused else "🎤 Recording..."
    st.write(status)

# Save transcript options and controls
if not st.session_state.is_recording and st.session_state.current_transcript:
    st.markdown("### Save Transcript")
    
    col1, col2 = st.columns(2)
    
    with col1:
        file_format = st.selectbox(
            "File Format",
            ["txt", "json", "csv"],
            help="Select the format to save your transcript"
        )
        
    with col2:
        include_timestamp = st.checkbox(
            "Include Timestamp",
            value=True,
            help="Add timestamp to the saved file"
        )
        
    save_dir = st.text_input(
        "Save Directory",
        value="transcripts",
        help="Enter the directory path where you want to save the transcript"
    )
    
    if st.button("Save Transcript"):
        filename = save_transcript(
            st.session_state.current_transcript,
            file_format,
            include_timestamp,
            save_dir
        )
        if filename:
            st.success(f"Successfully saved transcript as: {filename}")
            # Provide download button for the saved file
            with open(filename, 'r', encoding='utf-8') as f:
                st.download_button(
                    label="Download Transcript",
                    data=f.read(),
                    file_name=os.path.basename(filename),
                    mime=f"text/{file_format}"
                )

# Display transcript history
if st.session_state.transcripts:
    st.markdown("### Transcript History")
    for i, transcript in enumerate(st.session_state.transcripts[-5:]):
        st.text_area(f"Transcript {i+1}", transcript, height=100)
        
        # Add save button for each historical transcript
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button(f"Save #{i+1}"):
                filename = save_transcript(transcript)
                if filename:
                    st.success(f"Saved transcript #{i+1} as: {filename}")