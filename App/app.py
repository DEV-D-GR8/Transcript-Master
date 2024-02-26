import streamlit as st
from utils import convert_to_video_address_link, extract_transcript_details, generate_gemini_content, generate_pdf

prompt="""
You are a highly advanced AI language model, and you have been provided with the transcriptions of a YouTube video. Your task is to generate a detailed summary of the video contents, ensuring that no crucial information is omitted. After the summary, you are required to identify and explain important technical terms and/or concepts discussed in the video. Use your extensive knowledge to provide an in-depth understanding of the content covered.
#INSTRUCTIONS:
1. Provide a comprehensive summary of the video content, covering key points and details.
2. Identify and explain any technical terms or concepts introduced in the video.
3. Use your own knowledge to elaborate on the video content and provide additional insights or context.
#NOTE: If the video covers a specific field or topic, make sure to draw on relevant knowledge to enhance the summary and explanations.
Here is the YouTube video transcription: 
"""

st.title("Transcript Master")

youtube_link = st.text_input("Enter YouTube Video Link:")

if st.button("Get Summary"):
    
    if youtube_link:
        
        generalised_link = convert_to_video_address_link(youtube_link)
        video_id = generalised_link.split("=")[1]
        st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)
        
    try:
        
        transcript_text = extract_transcript_details(generalised_link)
        
        if transcript_text:
            
            try:
                
                summary = generate_gemini_content(transcript_text, prompt)
                st.write(summary)
                pdf_data = generate_pdf(summary)
                st.download_button("Download PDF", pdf_data, key='download_button', file_name='output.pdf', mime='application/pdf')
                
            except Exception as err:
                st.markdown("Gemini Pro API not responding. Try later.")
                
    except Exception as e:
        st.markdown("Transcripts unavailable for the provided video.")