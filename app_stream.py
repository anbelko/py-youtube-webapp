
import os
import pytube
import io
import urllib.parse
from flask import Flask, render_template, request, redirect, url_for, send_file, Response

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['GET', 'POST'])
def download():
    url = request.form['url']
    yt = pytube.YouTube(url)
    stream = yt.streams.get_highest_resolution()
    buffer = io.BytesIO()
    stream.stream_to_buffer(buffer)
    filename = urllib.parse.quote(yt.title) + '.mp4'
    response = Response(buffer.getvalue(), mimetype='video/mp4')
    response.headers['Content-Disposition'] = f'attachment; filename={filename}; filename*=UTF-8\'\'{filename}'
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)