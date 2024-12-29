from flask import Flask, Response, request, render_template, jsonify
import cv2
import requests

app = Flask(__name__)

# FastAPI endpoint
FASTAPI_URL = "http://127.0.0.1:8000/analyze_frame"

# @app.route('/video_feed')
# def video_feed():
#     # Capture video from the webcam
#     video_capture = cv2.VideoCapture(0)

#     while True:
#         ret, frame = video_capture.read()
#         if not ret:
#             break

#         # Encode frame as JPEG
#         _, buffer = cv2.imencode('.jpg', frame)
#         frame_bytes = buffer.tobytes()

#         # Send frame to FastAPI
#         response = requests.post(
#             FASTAPI_URL,
#             files={"file": ("frame.jpg", frame_bytes, "image/jpeg")}
#         )
#         print(response.json())  # Print FastAPI response for debugging

#         # Yield the frame as a video stream
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

#     video_capture.release()

@app.route('/')
def index():
    # Video stream page
    # return Response(video_feed(), mimetype='multipart/x-mixed-replace; boundary=frame')
    return render_template('index.html')

@app.route('/process_frame', methods=['POST'])
def process_frame():
    if "frame" not in request.files:
        return jsonify({"error": "No frame provided"}), 400
    file = request.files['frame']
    files = {'file': (file.filename, file.stream, file.mimetype)}
    print(f"Forwarding file to FastAPI: {file.filename}, MIME: {file.mimetype}")
    try:
        # Forward the frame to FastAPI backend
        response = requests.post(FASTAPI_URL, files=files)
        print(f"FastAPI Response Status: {response.status_code}, Content: {response.content}")
        response.raise_for_status()
        print(response)
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Failed to contact backend: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
