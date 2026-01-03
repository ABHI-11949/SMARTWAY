from fastapi import WebSocket
import cv2
import mediapipe as mp
from engagement_logic import detect_confusion
import asyncio
from starlette.websockets import WebSocketDisconnect

mp_face = mp.solutions.face_mesh
face_mesh = mp_face.FaceMesh()

async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    cap = cv2.VideoCapture(0)
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                await websocket.send_json({"status": "NO_CAMERA"})
                await asyncio.sleep(1)
                continue

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = face_mesh.process(rgb)

            if not result.multi_face_landmarks:
                await websocket.send_json({"status": "PROCTOR_ALERT"})
                await asyncio.sleep(1)
                continue

            if len(result.multi_face_landmarks) > 1:
                await websocket.send_json({"status": "MULTIPLE_FACES"})
                await asyncio.sleep(1)
                continue

            face_landmarks = result.multi_face_landmarks[0]
            status = detect_confusion(face_landmarks)

            if status == "CONFUSED":
                await websocket.send_json({"status": "CONFUSED"})
            else:
                await websocket.send_json({"status": "FOCUSED"})

            await asyncio.sleep(0.5)

    except WebSocketDisconnect:
        print("WebSocket disconnected. Closing camera.")
    finally:
        cap.release()
