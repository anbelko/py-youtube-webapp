from flask import Flask, render_template, request, jsonify
from pytube import YouTube

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/formats', methods=['POST'])
def formats():
    url = request.form['url']
    yt = YouTube(url)
    available_formats = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc()
    formats_list = []
    for stream in available_formats:
        formats_list.append({'itag': stream.itag, 'resolution': stream.resolution, 'mime_type': stream.mime_type})
    return jsonify({'formats': formats_list})

@app.route('/download', methods=['GET'])
def download_video():
    url = request.args.get('url')
    itag = request.args.get('format')
    video = YouTube(url)
    stream = video.streams.get_by_itag(itag)
    return stream.download()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)