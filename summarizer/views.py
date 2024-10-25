from googleapiclient.discovery import build
import cohere
from django.shortcuts import render
from django.http import JsonResponse
from youtube_transcript_api import YouTubeTranscriptApi


YOUTUBE_API_KEY = 'your_YOUTUBE_API_KEY'
COHERE_API_KEY = 'your_COHERE_API_KEY'

def index(request):
    return render(request, 'index.html')

def search_videos(request):
    query = request.GET.get('query', '')
    videos = []

    if query:
        youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
        youtube_request = youtube.search().list(q=query, part='id,snippet', maxResults=3, type='video')
        response = youtube_request.execute()

        videos = [
            video for video in response.get('items', [])
            if video['id']['kind'] == 'youtube#video' 
        ]

    return render(request, 'search_results.html', {'videos': videos})

def summarize_video(request, video_id):
    transcript = get_transcript(video_id)  
    
    if not transcript:
        return JsonResponse({'error': 'Transcript not available'})

    co = cohere.Client(COHERE_API_KEY)

    
    transcript_text = ' '.join([item['text'] for item in transcript])

    prompt = (
        f"The following is a transcript of a video. Your task is to write a detailed summary of what happens in this video. "
        "Provide the summary as if you are explaining the video to someone who has not seen it, making sure to include everything essential and to maintain the meaning and context.\n\n"
        f"Transcript:\n{transcript_text}\n\n"
        "Now, summarize the content in English, making sure not to leave out anything from the video."
    )

    summary_response = co.generate(
        model='command-xlarge-nightly',
        prompt=prompt,
        max_tokens=1000,  
        temperature=0.7  
    )
    
    summary = summary_response.generations[0].text.strip()

    return render(request, 'summary.html', {'summary': summary, 'video_id': video_id})

def get_transcript(video_id):
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

       
        try:
            transcript = transcript_list.find_transcript(['en'])
            print("Fetched English transcript.")
        except Exception:
            transcript = None

            for available_transcript in transcript_list:
                
                if available_transcript.language != 'en': 
                    transcript = available_transcript
                    print(f"Fetched transcript in {transcript.language}.")
                    break 

    except Exception as e:
        return None

    if transcript:
        transcript_data = transcript.fetch() 
        return transcript_data
    else:
        print("No transcript available for the video.")
        return None

def qna(request, video_id):
    question = request.GET.get('question', '')
    transcript = get_transcript(video_id)  

    if not transcript:
        return JsonResponse({'error': 'Transcript not available'})

    co = cohere.Client(COHERE_API_KEY)

    
    transcript_text = ' '.join([item['text'] for item in transcript])
    
    prompt = (
        f"Here is the transcript of the video:\n\n{transcript_text}\n\n"
        f"Based on the transcript above, answer the following question:\n"
        f"Question: {question}\n"
        "Answer the question in English based solely on the transcript. If the question is unrelated to the transcript, respond with 'I can't answer that as it is outside the scope of the content.'"
    )

    qna_response = co.generate(
        model='command-xlarge-nightly',
        prompt=prompt,
        max_tokens=400,
        temperature=0.4
    )

    answer = qna_response.generations[0].text.strip()

    return JsonResponse({'answer': answer})
