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
    return jsonify([{'itag': s.itag, 'resolution': s.resolution, 'mime_type': s.mime_type} for s in available_formats])

@app.route('/download', methods=['GET'])
def download():
    url = request.args.get('url')
    itag = request.args.get('format')
    yt = YouTube(url)
    stream = yt.streams.get_by_itag(itag)
    return stream.download()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)