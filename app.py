import os
import pytube
import subprocess
import io
import urllib.parse
from flask import Flask, render_template, request, redirect, url_for, send_file, Response

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    yt = pytube.YouTube(url)
    stream = yt.streams.get_highest_resolution()
    audio_path = yt.streams.filter(only_audio=True).first().download(output_path='.', filename_prefix='audio_')
    video_path = yt.streams.filter(only_video=True).first().download(output_path='.', filename_prefix='video_')
    output_path = f'{yt.title}.mp4'
    ffmpeg_concat_cmd = f'ffmpeg -i "{video_path}" -i "{audio_path}" -c:v copy -c:a copy "{output_path}"'
    os.system(ffmpeg_concat_cmd)
    filename = urllib.parse.quote(yt.title) + '.mp4'
    response = send_file(output_path, mimetype='video/mp4')
    response.headers['Content-Disposition'] = f'attachment; filename={filename}; filename*=UTF-8\'\'{filename}'
    os.remove(audio_path)
    os.remove(video_path)
    os.remove(output_path)
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
