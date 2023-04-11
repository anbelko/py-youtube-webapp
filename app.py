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

@app.route('/download', methods=['GET', 'POST'])
def download_video():
    url = request.form.get("url")
    format_id = request.form.get("format_id")

    yt = YouTube(url)
    available_formats = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc()
    formats = [{'itag': s.itag, 'resolution': s.resolution, 'mime_type': s.mime_type, 'url': s.url} for s in available_formats]

    # Find the selected format in the list of available formats
    selected_format = next((f for f in formats if f['itag'] == format_id), None)

    # Set the response headers
    response_headers = {
        "Content-Type": selected_format['mime_type'],
        "Content-Disposition": f"attachment; filename={yt.title}.mp4",
    }

    # Send the request to the selected format URL
    r = requests.get(selected_format['url'], stream=True)

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
