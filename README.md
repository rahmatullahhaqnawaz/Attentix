<!-- HERO -->
<h1 align="center">🚀 Attentix</h1>
<h3 align="center">🧠 Intelligent Attention Tracking System</h3>
<p align="center">
  <b>Constructor Tech Hackathon 2026</b><br/>
  Making online learning adaptive, intelligent, and human-aware.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python"/>
  <img src="https://img.shields.io/badge/FastAPI-Backend-green?style=for-the-badge&logo=fastapi"/>
  <img src="https://img.shields.io/badge/React-Frontend-61DAFB?style=for-the-badge&logo=react"/>
  <img src="https://img.shields.io/badge/OpenCV-ComputerVision-red?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/MediaPipe-AI-orange?style=for-the-badge"/>
</p>

<p align="center">
  <i>"Attentix intelligently tracks, measures, and enhances attention in real-time."</i>
</p>

---

## 🌟 Why Attentix?

Online learning struggles with one core problem:
👉 **We don't know if students are actually paying attention.**

**Attentix solves this.**

Using AI + Computer Vision, Attentix:
- Detects attention in real-time 🎯
- Adapts learning dynamically ⚡
- Re-engages distracted students 🔄

---

## 🎬 Demo Modes

### 👨‍🎓 Student — Upload Analysis
- Upload recorded sessions
- Frame-by-frame engagement breakdown
- Timeline analytics

### 🎥 Student — Live Webcam
- Real-time face tracking (every 2s)
- Live engagement scoring
- Auto playback adaptation
- Quiz on inactivity

### 👩‍🏫 Teacher Dashboard
- Upload up to **10 students at once**
- Class-wide analytics
- AI insights + alerts
- Quiz broadcasting

---

## ✨ Features

✔️ 6-signal facial analysis
✔️ Real-time engagement score (0–100)
✔️ Adaptive video playback
✔️ Inactivity detection + auto quiz
✔️ Batch video processing
✔️ AI feedback system
✔️ Live webcam streaming
✔️ Teacher analytics dashboard

---

## 🧠 How It Works

```
[ Webcam / Video ]
       ↓
[ MediaPipe FaceMesh ]
    468 Landmarks
       ↓
[ AI Engagement Engine ]
       ↓
[ FastAPI Backend ]
       ↓
[ React Dashboard ]
```

---

## 📊 Engagement Logic

```python
if ear > 0.15:                          score += 40  # eyes open
if abs(yaw) < 45 and abs(pitch) < 45:  score += 30  # face forward
if motion > 0.0003:                     score += 20  # movement
if expression in ("focused","neutral"): score += 10  # expression
```

---

## 🎯 Output Behavior

| Score | State | Action |
|-------|-------|--------|
| > 70  | HIGH  | ⚡ 1.5× speed |
| 40–70 | MED   | ▶️ Normal |
| < 40  | LOW   | ⏸ Pause + Quiz |

---

## 🛠️ Tech Stack

| Layer | Tech |
|-------|------|
| AI Vision | MediaPipe FaceMesh |
| Video | OpenCV |
| Backend | FastAPI |
| Frontend | React + Tailwind |
| Charts | Recharts |

---

## ⚙️ Installation

### 🔧 Backend

```bash
git clone https://github.com/rahmatullahhaqnawaz/New-Attentix.git
cd New-Attentix
py -3.11 -m venv .venv
.venv\Scripts\activate
pip install fastapi uvicorn opencv-python==4.10.0.84 mediapipe==0.10.14 numpy==1.26.4 python-multipart
cd backend
uvicorn main:app --reload --port 8000 --host 0.0.0.0
```

👉 API live at `http://localhost:8000`

### 🌐 Frontend

```bash
cd frontend/attentivise-insights
npm install
npm run dev
```

👉 App live at `http://localhost:8080`

---

## 🔌 API Example

```json
{
  "score": 82,
  "state": "high",
  "confidence": 0.91,
  "action": "speed_1.5x",
  "signals": {
    "eye_contact_pct": 78.0,
    "head_pose": "forward",
    "expression": "focused",
    "yawning": false,
    "inactivity_sec": 2.0
  }
}
```

---

## 📁 Project Structure

```
attentix/
├── backend/
│   ├── face_engine.py        # Core AI — 6-signal face analysis
│   ├── video_processor.py    # Video processing + batch analysis
│   ├── main.py               # FastAPI server
│   └── requirements.txt
├── frontend/
│   └── attentivise-insights/ # React app
├── samples/                  # Demo videos
└── README.md
```

---

## 🔮 Future Roadmap

- 🎭 Emotion detection AI
- 🤖 Auto-generated quizzes from lecture content
- 👥 Multi-student real-time comparison
- 📱 Mobile app
- 🎓 LMS integration (Moodle / Canvas)

---

## 🔗 Links

- 🌐 **Live Demo:** [attentivus-pulse.lovable.app](https://attentivus-pulse.lovable.app)
- 💻 **GitHub:** [New-Attentix](https://github.com/rahmatullahhaqnawaz/New-Attentix)

---

## 👨‍💻 Author

**Rehmatullah Haqnawaz**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/rehmatullah-haqnawaz-4947b0291/)

---

<p align="center">Built with ❤️ for Constructor Tech Hackathon 2026</p>
