from flask import Flask, render_template, request, jsonify, send_file
import requests
import re

app = Flask(__name__)

def extract_video_id(url):
    pattern = r"(?:v=|\/)([0-9A-Za-z_-]{11})(?:[?&#]|$)"
    match = re.search(pattern, url)
    return match.group(1) if match else None

@app.route('/', methods=['GET', 'POST'])
def index():
    video_data = None
    error = None
    if request.method == 'POST':
        url = request.form.get('url')
        video_id = extract_video_id(url)
        if not video_id:
            error = "Invalid YouTube URL"
        else:
            # Use free API to get download links
            api_url = f"https://api.vevioz.com/api/button/mp3/{video_id}"
            try:
                resp = requests.get(api_url, timeout=10)
                data = resp.json()
                if data.get('status') == 'ok':
                    video_data = {
                        'title': data.get('title'),
                        'thumbnail': data.get('thumbnail'),
                        'low_audio': data.get('audio', {}).get('low'),   # ~2MB
                        'high_audio': data.get('audio', {}).get('high'),
                        'low_video': data.get('video', {}).get('low'),
                        'high_video': data.get('video', {}).get('high')
                    }
                else:
                    error = "Could not fetch video. Try another link."
            except Exception as e:
                error = f"API error: {str(e)}"
    return render_template('index.html', video=video_data, error=error)

if __name__ == '__main__':
    app.run(debug=True)
