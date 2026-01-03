import math

def distance(p1, p2):
    return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

def detect_confusion(face_landmarks):
    """
    Custom confusion logic:
    - Eyebrows closer (brow furrow)
    - No smile
    """

    # Eyebrow landmarks (MediaPipe)
    left_brow = face_landmarks.landmark[65]
    right_brow = face_landmarks.landmark[295]

    brow_distance = distance(left_brow, right_brow)

    # Mouth landmarks (simple smile check)
    left_mouth = face_landmarks.landmark[61]
    right_mouth = face_landmarks.landmark[291]
    mouth_distance = distance(left_mouth, right_mouth)

    if brow_distance < 0.25 and mouth_distance < 0.40:
        return "CONFUSED"

    return "NOT_CONFUSED"
