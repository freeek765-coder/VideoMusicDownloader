from flask import Flask, render_template, send_file
import os

app = Flask(__name__)

# Sample video file (replace with your own or use a public URL)
# For demonstration, we use a small placeholder video from the web.
SAMPLE_VIDEO_URL = "https://www.w3schools.com/html/mov_bbb.mp4"

@app.route('/')
def index():
    return render_template('index.html', video_url=SAMPLE_VIDEO_URL)

# Dummy download endpoints – in a real app you would generate/retrieve the file
@app.route('/download/low')
def download_low():
    # Simulate a low-quality 2MB video (here we just redirect to a sample)
    # In reality, you would serve a compressed version.
    return send_file('static/sample_low.mp4', as_attachment=True)

@app.route('/download/high')
def download_high():
    return send_file('static/sample_high.mp4', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)