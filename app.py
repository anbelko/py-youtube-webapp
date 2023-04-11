from flask import Flask, render_template, request, jsonify, make_response
from pytube import YouTube

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/formats', methods=['POST'])
def get_formats():
    url = request.form['url']
    yt = YouTube(url)
    available_formats = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc()
    formats = [{'itag': s.itag, 'resolution': s.resolution, 'mime_type': s.mime_type} for s in available_formats]
    return jsonify(formats)

@app.route('/download', methods=['GET'])
def download():
    url = request.args.get('url')
    itag = request.args.get('format')
    yt = YouTube(url)
    stream = yt.streams.get_by_itag(itag)
    response = make_response(stream.stream_to_buffer())
    response.headers['Content-Disposition'] = 'attachment; filename="{}.mp4"'.format(yt.title)
    response.headers['Content-Type'] = stream.mime_type
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
