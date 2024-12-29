from fastapi import FastAPI, APIRouter, File, UploadFile
import numpy as np
import cv2
from fastapi.responses import JSONResponse

from eye_tracker import track_eye
from head_pose_estimation import detect_head_pose
from mouth_opening_detector import mouth_opening_detector
from person_and_phone import detect_phone_and_person


app = FastAPI()


# @app.post("/analyze_video")
# def read_root(video_url: str=None):
#     track_eye(video_url)
#     detect_head_pose(video_url)
#     mouth_opening_detector(video_url)
#     detect_phone_and_person(video_url)


#     return {"message": "Success"}
@app.post("/analyze_frame")
async def analyze_frame(file: UploadFile = File(...)):
    # Save the frame temporarily
    contents = await file.read()
    np_frame = np.frombuffer(contents, np.uint8)
    frame = cv2.imdecode(np_frame, cv2.IMREAD_COLOR)
    
    # Pass the frame to your analysis functions
    # eyes = track_eye(frame)
    # head = detect_head_pose(frame)
    # mouth = mouth_opening_detector(frame)
    # phone_person = detect_phone_and_person(frame)
    # if not eyes:
    #     eyes = ""
    # if not head:
    #     head = ""
    # if not mouth:
    #     mouth = ""
    # if not phone_person:
    #     phone_person = ""
    
    # messages = {
    #     "phone_message": phone_person,
    #     "eye_message": eyes,
    #     "head_message": head,
    #     "mouth_message": mouth,
    # }
    result = (
        track_eye(frame) or
        detect_head_pose(frame) or
        mouth_opening_detector(frame) or
        detect_phone_and_person(frame)
    )
    return {"result": result or "No significant activity detected"}
