\# attentix — Intelligent Attention Tracking System



> \*\*Constructor Tech Hackathon 2026\*\*  

> \*"Attentix is a system that intelligently tracks and responds to user attention."\*



\---



\## What is Attentix?



Attentix is a real-time student engagement tracking system for online education. It analyses student webcam feeds using computer vision, calculates a live engagement score from 6 facial signals, and automatically adapts the lecture experience — pausing videos, triggering quizzes, adjusting playback speed, and alerting the teacher when attention drops.



\---



\## Demo



\### Student View — Upload Mode

Upload a recorded lecture session. Attentix analyses every frame and returns a full engagement report with second-level breakdown.



\### Student View — Live Webcam

Real-time face analysis every 2 seconds. Score updates live, video speed adapts automatically, quiz triggers on inactivity.



\### Teacher Dashboard

Upload up to 10 student recordings at once. Get class-wide analytics, AI suggestions, live alerts, and broadcast quiz controls.



\---



\## Features



\- \*\*6-signal face analysis\*\* — eye contact, head pose, yawning, facial expression, motion, inactivity

\- \*\*Real-time engagement score\*\* (0–100) updated every 4 seconds

\- \*\*Adaptive playback\*\* — 1.5× speed when HIGH, 1.0× when MEDIUM, pause + quiz when LOW

\- \*\*Inactivity detection\*\* — quiz triggered after 20 seconds of no movement

\- \*\*Batch video analysis\*\* — teacher uploads up to 10 student recordings at once

\- \*\*AI feedback\*\* — personalised suggestions for students and teachers

\- \*\*Live webcam mode\*\* — streams frames to backend every 2 seconds

\- \*\*Teacher dashboard\*\* — class-wide metrics, alerts, speed control, quiz broadcast



\---



\## Architecture



```

\[ Webcam / MP4 Upload ]

&#x20;        |

\[ OpenCV + MediaPipe FaceMesh ]

&#x20;  468 facial landmarks

&#x20;        |

\[ Python Engagement Engine ]

&#x20;  Eye · Head · Lips · Expression · Motion · Inactivity

&#x20;        |

\[ FastAPI  →  GET/POST /engagement  /upload  /students ]

&#x20;        |

\[ React Frontend (Lovable) ]

&#x20;  Student View  |  Teacher Dashboard

&#x20;  Graph · Timeline · Quiz · Rewards

```



\---



\## Engagement Score Formula



```python

score = 0

if ear > 0.15:                    score += 40   # eyes open

if abs(yaw) < 45:                 score += 30   # face forward

if motion > 0.0003:               score += 20   # slight movement

if expression in ("focused", "neutral"):  score += 10



if abs(yaw) > 55:                 score -= 30   # looking away

if lip\_ratio > 0.07:              score -= 15   # yawning

if expression == "drowsy":        score -= 10

if inactivity\_sec > 30:           score -= 10



score = max(0, min(100, score))

```



| Score | State | Action |

|-------|-------|--------|

| > 70 | HIGH | Speed → 1.5× |

| 40–70 | MEDIUM | Speed → 1.0× |

| < 40 | LOW | Pause + quiz |



\---



\## Tech Stack



| Layer | Technology |

|-------|-----------|

| Face detection | MediaPipe FaceMesh (468 landmarks) |

| Video processing | OpenCV 4.10 |

| Math | NumPy 1.26 |

| API | FastAPI + Uvicorn |

| Frontend | React + Tailwind (Lovable) |

| Charts | Recharts |



\---



\## Installation



\### Requirements

\- Python 3.11

\- Node.js 18+



\### Backend Setup



```bash

\# Clone the repo

git clone https://github.com/rahmatullahhaqnawaz/New-Attentix.git

cd New-Attentix



\# Create virtual environment with Python 3.11

py -3.11 -m venv .venv

.venv\\Scripts\\activate        # Windows

\# source .venv/bin/activate   # Mac/Linux



\# Install dependencies

pip install fastapi uvicorn opencv-python==4.10.0.84 mediapipe==0.10.14 numpy==1.26.4 python-multipart



\# Start the API server

cd backend

uvicorn main:app --reload --port 8000 --host 0.0.0.0

```



API will be live at `http://localhost:8000`



\### Frontend Setup



```bash

cd frontend/attentivise-insights

npm install

npm run dev

```



Frontend will be live at `http://localhost:8080`



\---



\## API Endpoints



| Method | Endpoint | Description |

|--------|----------|-------------|

| GET | `/` | Health check |

| POST | `/engagement` | Send webcam frame, get live score |

| GET | `/engagement` | Poll current speed + quiz state |

| POST | `/upload` | Upload video file for analysis |

| POST | `/upload/batch` | Upload up to 10 videos at once |

| GET | `/students` | Get all student results |

| POST | `/speed` | Set playback speed (0.75/1.0/1.5/2.0) |

| POST | `/quiz` | Broadcast quiz to students |

| GET | `/quiz` | Poll for pending quiz |

| POST | `/quiz/answer` | Submit quiz answer |



\### Example Response — POST /engagement



```json

{

&#x20; "score": 82,

&#x20; "state": "high",

&#x20; "confidence": 0.91,

&#x20; "timestamp": 14.2,

&#x20; "signals": {

&#x20;   "eye\_contact\_pct": 78.0,

&#x20;   "eyes\_open": true,

&#x20;   "head\_pose": "forward",

&#x20;   "yaw\_deg": -8.3,

&#x20;   "pitch\_deg": 4.1,

&#x20;   "yawning": false,

&#x20;   "lip\_ratio": 0.032,

&#x20;   "motion": 0.0014,

&#x20;   "inactivity\_sec": 2.0,

&#x20;   "expression": "focused"

&#x20; },

&#x20; "events": \[],

&#x20; "action": "speed\_1.5x",

&#x20; "teacher\_alert": {

&#x20;   "triggered": false,

&#x20;   "message": ""

&#x20; }

}

```



\---



\## Project Structure



```

attentix/

├── backend/

│   ├── face\_engine.py        # Core AI — 6-signal face analysis

│   ├── video\_processor.py    # Video file processing + batch analysis

│   ├── main.py               # FastAPI server — all endpoints

│   ├── test\_engine.py        # Webcam test with face mesh overlay

│   └── requirements.txt

├── frontend/

│   └── attentivise-insights/ # React app (Lovable)

│       ├── src/

│       │   ├── pages/

│       │   │   ├── StudentPage.tsx

│       │   │   └── TeacherPage.tsx

│       │   └── lib/

│       │       └── api.ts    # All API calls

│       └── package.json

├── samples/

│   ├── sample\_engaged.mp4    # Demo video — high engagement

│   └── sample\_distracted.mp4 # Demo video — low engagement

└── README.md

```



\---



\## Inactivity Definition



> \*"Prolonged inactivity is defined as the absence of significant head or facial movement (motion < 0.0003 across all 468 MediaPipe landmarks) sustained for more than 30 seconds. When detected, the system pauses video playback and triggers a quiz to re-engage the student."\*



\---



\## Evaluation Metrics



> \*"The system was evaluated based on accuracy of event detection compared against ground-truth labels, robustness across varying lighting conditions and webcam qualities, and real-time usability measured by end-to-end latency from frame capture to score display."\*



\- \*\*Accuracy\*\* — precision/recall of yawn and inactivity detection vs manual labels

\- \*\*Robustness\*\* — tested across bright, dim, and backlit conditions; 480p–1080p webcams

\- \*\*Latency\*\* — < 500ms end-to-end from frame capture to score update



\---



\## Future Work



\- Emotion detection using full expression classification

\- AI-generated quiz questions from lecture transcript

\- Multi-student real-time comparison dashboard

\- Voice alerts for prolonged inactivity

\- LMS integration (Moodle / Canvas)

\- Mobile app with front-facing camera



\---



\## Authors



Built for Constructor Tech Hackathon 2026.



\---



\## License



MIT

