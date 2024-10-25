# YOUTUBE_VIDEO_SUMMARIZER  
A Django-based application that takes a YouTube link as input, generates a summary of the video content, and offers an interactive Q&A based on that content.   It uses the Cohere API for natural language processing and YouTube API to fetch video details.  
  
# Features    
Video Content Summarization: Summarizes the main points of a video.  
Interactive Q&A: Enables users to ask questions based on the video content.  
Video Player: Embeds the YouTube video on the page for easy access.  
# Prerequisites  
Python (3.7 or higher)  
Django  
Access to Cohere and YouTube Data APIs  
pip (Python package manager)    

# Setup Guide  
1. Clone the Repository  
   git clone https://github.com/yourusername/YOUTUBE_VIDEO_SUMMARIZER.git  
cd YOUTUBE_VIDEO_SUMMARIZER   
  
2. Create and Activate a Virtual Environment  
To avoid package conflicts, set up a virtual environment:

 # Create virtual environment  
python3 -m venv venv  

# Activate virtual environment  
# On macOS/Linux  
source venv/bin/activate  
# On Windows  
venv\Scripts\activate  

  
3. Install Dependencies  
Install required packages from requirements.txt:    
 pip install -r requirements.txt  

  
4. Set Up API Keys  
You will need both the Cohere API key and the YouTube Data API key. Follow these steps:   

Cohere API:  
Go to Cohere's API documentation.  
Sign up and get your API key. 
  
YouTube Data API:  
Go to the Google Cloud Console.  
Enable the YouTube Data API v3.  
Create an API key.  

# Add both API in the views.py file of the project  

5. Run the Development Server  
Start the Django development server:  
  python manage.py runserver  

