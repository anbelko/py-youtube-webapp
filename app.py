import os
import pytube
from flask import Flask, render_template, request, redirect, url_for, send_file

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    video = pytube.YouTube(url)
    stream = video.streams.filter(progressive=True).first()
    filename = stream.default_filename
    stream.download()
    path = os.path.join(os.getcwd(), filename)
    return send_file(path, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
