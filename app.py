# app.py

from flask import Flask, render_template, request
from transformers import pipeline
from youtube_transcript_api import YouTubeTranscriptApi

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_video', methods=['POST'])
def process_video():
    if request.method == 'POST':
        youtube_video = request.form['youtube_video']
        video_id = youtube_video.split("=")[1]
        transcript = YouTubeTranscriptApi.get_transcript(video_id)

        result = ""
        for i in transcript:
            result += ' ' + i['text']

        summarizer = pipeline('summarization')
        num_iters = int(len(result)/1000)
        summarized_text = []

        for i in range(0, num_iters + 1):
            start = i * 1000
            end = (i + 1) * 1000
            out = summarizer(result[start:end])
            out = out[0]
            out = out['summary_text']
            summarized_text.append(out)

        return render_template('result.html', summarized_text=summarized_text)

if __name__ == '__main__':
    app.run(debug=True)
