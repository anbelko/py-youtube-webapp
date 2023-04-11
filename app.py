from flask import Flask, render_template, request, jsonify
from pytube import YouTube

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/formats', methods=['POST'])
def get_formats():
    url = request.form['url']
    video = YouTube(url)
    formats = [{'itag': s.itag, 'resolution': s.resolution, 'mime_type': s.mime_type} for s in video.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc()]
    return jsonify(formats)

@app.route('/download', methods=['GET'])
def download_video():
    url = request.args.get('url')
    itag = request.args.get('format')
    video = YouTube(url)
    stream = video.streams.get_by_itag(itag)
    return stream.download()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)