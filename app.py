import streamlit as st
import google.generativeai as genai
import re
from youtube_transcript_api import YouTubeTranscriptApi
from googletrans import Translator


genai.configure(api_key="AIzaSyB34O3DUQGvAV_XI7cf0zNCvmO0DkFA8T4")
prompt="""You are a specialized YouTube video summarizer. Your task is to take the provided transcript text and generate a comprehensive, accurate, and detailed summary that fully captures the essence of the video. The summary should be well-organized, leaving no significant content out, and should be consistent in quality and detail each time.

Instructions:
Generate a comprehensive summary of the provided YouTube video transcript. Follow these guidelines:
Title: Start with the video title for context.
Intro Summary: Offer a brief overview of the video's purpose, key themes, and background its summary in 200 words.
Detailed Summary: Break down the content into bullet points, covering all significant details and transitions. Include tone, intent, and emphasis where relevant.
Subtopics: If the video has sections, summarize each under clear subheadings, highlighting connections to the overall theme and any important arguments or examples.
Implementation Steps: For practical demonstrations, provide a detailed, step-by-step guide including tools, methods, and outcomes.
Key Takeaways: Summarize key lessons, insights, and conclusions, focusing on actionable points and overarching themes.
Special Cases:
Review Videos: Summarize the reviewer’s recommendation, any ratings, pros and cons, and tone.
Learning Videos: Focus on key concepts, learning objectives, and tips or best practices.
Consistency & Engagement: Ensure a consistent, professional tone, and note any particularly compelling sections or interactive elements.
Generate a comprehensive summary based on the given instruction  for the following youtube video transcript in english language:"""


#for extractin video id from youtube url
def extract_video_code(youtube_url):
    # Regular expression pattern to match the video code
    pattern = r'(?:v=|\/)([0-9A-Za-z_-]{11}).*'
    match = re.search(pattern, youtube_url)
    
    if match:
        return match.group(1)
    else:
        return None
    

#translating summary 
def translate_summary(summary, target_language):
    translator = Translator()
    translated = translator.translate(summary, dest=target_language)
    return translated.text.replace("**", "")


#for extracting transcription from youtube video
def extract_transcript_details(youtube_video_url):
    try:
        video_id= extract_video_code(youtube_video_url)
        #for knowing in what languages the transcripts are available
        #available_transcripts = YouTubeTranscriptApi.list_transcripts(video_id)
        #print(available_transcripts)
        
        if video_id:
            transcript=YouTubeTranscriptApi.get_transcript(video_id,languages=[
                "en","hi","bn","ta","te","kn","ml","as","or","gu","mr","ne","pa","sd","si",
                "ab", "aa", "af", "ak", "sq", "am", "ar", "hy", "ay", "az", "ba", "eu", "be", "bho",
                "bs", "br", "bg", "my", "ca", "ceb", "zh-Hans", "zh-Hant", "co", "hr", "cs", "da",
                "dv", "nl", "dz", "eo", "et", "ee", "fo", "fj", "fil", "fi", "fr", "gaa", "gl", "lg",
                "ka", "de", "el", "gn", "ht", "ha", "haw", "iw", "hmn", "hu", "is", "ig", "id",
                "ga", "it", "ja", "jv", "kl", "kk", "kha", "km", "rw", "ko", "kri", "ku", "ky", "lo",
                "la", "lv", "ln", "lt", "luo", "lb", "mk", "mg", "ms", "mt", "gv", "mi", "mr", "mn",
                "mfe", "new", "nso", "no", "ny", "oc", "om", "os", "pam", "ps", "fa", "pl", "pt",
                "pt-PT", "qu", "ro", "rn", "ru", "sm", "sg", "sa", "gd", "sr", "crs", "sn", "sd",
                "si", "sk", "sl", "so", "st", "es", "su", "sw", "ss", "sv", "tg", "tt", "th",
                "bo", "ti", "to", "ts", "tn", "tum", "tr", "tk", "uk", "ur", "ug", "uz", "ve", "vi",
                "war", "cy", "fy", "wo", "xh", "yi", "yo", "zu"
]
)
            transcript_text=""
            for i in transcript:
                transcript_text += " " + i["text"]
            return transcript_text
        else:
            return "No transcripts available for this video."
            
    except Exception as e:
        raise e


#for extracting summary from transcription using gemini api
def generate_gemini_content(transcript_text,prompt):
    model=genai.GenerativeModel("gemini-pro")
    response=model.generate_content(prompt+transcript_text+"in english language")
    print(response.text)
    return response.text


#frontend interface using streamlit
st.markdown("<h1 style='text-align: center; color: #FF6347;'> YouTube Video Notes Taker</h1>", unsafe_allow_html=True)
st.markdown("<h5 style='text-align: center; color: white;'>This will work well only if the youtube video has a good transcription</h5>", unsafe_allow_html=True)

youtube_link = st.text_input("Paste or enter YouTube video link:")
target_language=st.text_input("Enter you prefered language code(e.g. 'hi' for hindi, 'te' for telugu, 'es' for spanish, search in google if you don't know) ")

if youtube_link:
    video_id = extract_video_code(youtube_link)
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

if st.button("Get Detailed Notes"):
    transcript_text = extract_transcript_details(youtube_link)
    
    if transcript_text:
        if target_language:
            if target_language!='en':
                 summary = generate_gemini_content(transcript_text, prompt)
                 summary=translate_summary(summary, target_language)
            else:
                summary = generate_gemini_content(transcript_text, prompt)
       
        st.markdown("<h2 style='color: #FF6347;'>Detailed Notes:</h2>", unsafe_allow_html=True)
        st.write(summary)

#applying basic styles
st.markdown(
    """
    <style>
    input {
        padding: 10px;
        font-size: 18px;
    }

    button {
        padding: 10px;
        font-size: 18px;
        background-color: #FF6347;
        color: white;
        border: none;
        border-radius: 5px;
        align:center;
    }

    button:hover {
        background-color: white;
        transition: background-color 0.3s ease;
    }

    h2 {
        color: #FF6347;
    }

    p {
        line-height: 1.6;
    }
    </style>
    """,
    unsafe_allow_html=True
)

