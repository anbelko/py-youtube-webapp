from flask import Flask, render_template, request
from pytube import YouTube

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    yt = YouTube(url)
    itag = request.form['itag']
    video = yt.streams.get_by_itag(itag)
    download_url = video.url
    return redirect(download_url)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)