from flask import Flask, render_template, request, jsonify, make_response
from pytube import YouTube

app = Flask(__name__)

def stream_to_buffer(self, buffer):
    chunk_size = 4096
    for chunk in self.iter_content(chunk_size=chunk_size):
        buffer.write(chunk)
    buffer.flush()

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

@app.route("/download", methods=["POST"])
def download_video():
    url = request.form.get("url")
    format_id = request.form.get("format_id")

    # Get the selected format URL
    format_url = video_formats[int(format_id)]["url"]

    # Set the response headers
    response_headers = {
        "Content-Type": "video/mp4",
        "Content-Disposition": "attachment; filename=video.mp4",
    }

    # Send the request to the format URL
    r = requests.get(format_url, stream=True)

    # Create a buffer to store the contents of the response stream
    buffer = io.BytesIO()

    # Stream the contents of the response to the buffer
    r.raw.decode_content = True
    stream = Stream(r.raw)
    stream.stream_to_buffer(buffer)

    # Create the response object with the contents of the buffer
    response = make_response(buffer.getvalue())

    # Set the response headers
    for key, value in response_headers.items():
        response.headers[key] = value

    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
