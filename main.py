import cv2
import mediapipe as mp
import numpy as np
import math
import subprocess
import threading
import os

# =====================================================
# CONFIGURATION
# =====================================================
VIDEO_PATH = r"C:\Users\sakth\Videos\alarm.mp4"
VLC_PATH = r"C:\Program Files\VideoLAN\VLC\vlc.exe"

FRAMES_TO_PLAY = 2
FRAMES_TO_STOP = 35

# =====================================================
# MEDIAPIPE SETUP
# =====================================================

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

video_process = None

def start_video():
    global video_process

    if video_process is not None:
        return

    if not os.path.exists(VIDEO_PATH):
        print(f"Video not found: {VIDEO_PATH}")
        return

    try:
        video_process = subprocess.Popen([
            VLC_PATH,
            "--fullscreen",
            "--play-and-exit",
            VIDEO_PATH
        ])
    except Exception as e:
        print("Failed to launch VLC:", e)

def stop_video():
    global video_process

    if video_process is not None:
        try:
            video_process.terminate()
        except Exception:
            pass
        video_process = None

def dist3d(a, b):
    return math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2 + (a.z - b.z) ** 2)

MODEL_POINTS = np.array([
    (0.0, 0.0, 0.0),
    (0.0, -330.0, -65.0),
    (-225.0, 170.0, -135.0),
    (225.0, 170.0, -135.0),
    (-150.0, -150.0, -125.0),
    (150.0, -150.0, -125.0)
], dtype=np.float64)

LANDMARK_IDS = [1, 152, 33, 263, 61, 291]

def get_head_pitch(landmarks, img_w, img_h):
    image_points = np.array([
        (landmarks[i].x * img_w, landmarks[i].y * img_h)
        for i in LANDMARK_IDS
    ], dtype=np.float64)

    focal_length = img_w
    center = (img_w / 2, img_h / 2)

    camera_matrix = np.array([
        [focal_length, 0, center[0]],
        [0, focal_length, center[1]],
        [0, 0, 1]
    ], dtype=np.float64)

    dist_coeffs = np.zeros((4, 1))

    success, rotation_vec, _ = cv2.solvePnP(
        MODEL_POINTS,
        image_points,
        camera_matrix,
        dist_coeffs,
        flags=cv2.SOLVEPNP_ITERATIVE
    )

    if not success:
        return 0.0

    rot_mat, _ = cv2.Rodrigues(rotation_vec)
    return math.degrees(math.asin(-rot_mat[2][1]))

def eye_looking_down(landmarks):
    try:
        results = []

        for top_idx, bottom_idx, iris_idx in [
            (159, 145, 468),
            (386, 374, 473)
        ]:
            top = landmarks[top_idx]
            bottom = landmarks[bottom_idx]
            iris = landmarks[iris_idx]

            eye_h = dist3d(top, bottom)

            if eye_h < 0.005:
                return None

            iris_rel = (iris.y - top.y) / (bottom.y - top.y + 1e-6)
            results.append(iris_rel)

        avg = sum(results) / len(results)
        return avg > 0.52, avg

    except Exception:
        return None

def draw_eye_boxes(image, landmarks, img_w, img_h):
    for ids in [(33, 133, 159, 145), (263, 362, 386, 374)]:
        xs = [int(landmarks[i].x * img_w) for i in ids]
        ys = [int(landmarks[i].y * img_h) for i in ids]

        pad = 8

        cv2.rectangle(
            image,
            (min(xs) - pad, min(ys) - pad),
            (max(xs) + pad, max(ys) + pad),
            (0, 255, 0),
            2
        )

cap = cv2.VideoCapture(0)
cv2.namedWindow("Doomscroller Ctrl", cv2.WINDOW_NORMAL)

at_screen_frames = 0
away_frames = 0
no_face_frames = 0
video_playing = False

while cap.isOpened():
    ok, frame = cap.read()

    if not ok:
        continue

    frame = cv2.flip(frame, 1)

    img_h, img_w = frame.shape[:2]

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    rgb.flags.writeable = False
    results = face_mesh.process(rgb)
    rgb.flags.writeable = True

    display = frame.copy()
    looking_at_screen = not video_playing

    if results.multi_face_landmarks:
        no_face_frames = 0
        lms = results.multi_face_landmarks[0].landmark

        draw_eye_boxes(display, lms, img_w, img_h)

        pitch = get_head_pitch(lms, img_w, img_h)
        eye_result = eye_looking_down(lms)

        if eye_result is not None:
            _, iris_val = eye_result

            head_straight = -10 < pitch < 20
            eyes_centered = 0.20 < iris_val < 0.68

            looking_at_screen = head_straight and eyes_centered

            cv2.putText(display, f"Pitch: {pitch:+.1f}", (15, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            cv2.putText(display, f"Eye: {iris_val:.2f}", (15, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        state_label = "AT SCREEN" if looking_at_screen else "AWAY"
        color = (0, 255, 0) if looking_at_screen else (0, 0, 255)

        cv2.putText(display, state_label, (15, 90),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

    else:
        no_face_frames += 1
        looking_at_screen = True if no_face_frames >= 30 else False

    if looking_at_screen:
        at_screen_frames += 1
        away_frames = 0
    else:
        away_frames += 1
        at_screen_frames = 0

    if not video_playing and away_frames >= FRAMES_TO_PLAY:
        video_playing = True
        threading.Thread(target=start_video, daemon=True).start()

    elif video_playing and at_screen_frames >= FRAMES_TO_STOP:
        video_playing = False
        threading.Thread(target=stop_video, daemon=True).start()

    cv2.imshow("Doomscroller Ctrl", display)

    if cv2.waitKey(1) & 0xFF == 27:
        break

stop_video()
cap.release()
cv2.destroyAllWindows()
