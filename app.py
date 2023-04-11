import os
import pytube
from flask import Flask, render_template, request, redirect, url_for, send_file, Response

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# @app.route('/download', methods=['POST'])
# def download():
#     url = request.form['url']
#     video = pytube.YouTube(url)
#     stream = video.streams.get_highest_resolution()
#     filename = stream.default_filename
#     stream.download()
#     path = os.path.join(os.getcwd(), filename)
#     return send_file(path, as_attachment=True)

class Stream:
    def __init__(self, video):
        self.video = video

    def stream_to_buffer(self, buffer):
        for chunk in self.video.iter_content(chunk_size=1024):
            if chunk:
                buffer.write(chunk)
                yield buffer.getvalue()
                buffer.truncate(0)

@app.route('/download', methods=['GET', 'POST'])
def download():
    video_url = request.form['url']
    yt = pytube.YouTube(url)
    stream = yt.streams.get_highest_resolution()
    response = Response(stream.stream_to_buffer(), mimetype='video/mp4')
    response.headers['Content-Disposition'] = f'attachment; filename={yt.title}.mp4'
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
