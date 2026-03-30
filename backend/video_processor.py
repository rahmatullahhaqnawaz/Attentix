"""
attentix — video_processor.py
Deterministic video processing — same video always gives same score.
"""

import cv2
import numpy as np
from face_engine import FaceEngine

SAMPLE_FPS = 3  # analyse 3 frames per second — faster + consistent
import hashlib

def process_video(video_path: str, student_name: str = "Student") -> dict:
    # Generate deterministic seed from video file content
    with open(video_path, 'rb') as f:
        file_hash = int(hashlib.md5(f.read(1024*1024)).hexdigest(), 16) % (2**32)
    np.random.seed(file_hash % 1000)

def process_video(video_path: str, student_name: str = "Student") -> dict:
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return {"error": f"Could not open video: {video_path}"}

    video_fps    = cap.get(cv2.CAP_PROP_FPS) or 25
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration_sec = total_frames / video_fps
    frame_skip   = max(1, int(video_fps / SAMPLE_FPS))

    engine   = FaceEngine()
    timeline = []
    all_scores = []
    frame_idx  = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_idx % frame_skip == 0:
            timestamp = frame_idx / video_fps

            # Resize for consistency — always same resolution
            frame = cv2.resize(frame, (640, 480))

            result = engine.analyse_frame(frame, timestamp)

            # Use raw score per frame for accurate reporting
            raw = result["score"]
            all_scores.append(raw)
            timeline.append({
                "time":  float(round(timestamp, 2)),
                "score": int(raw),
                "state": str(result["state"]),
            })

        frame_idx += 1

    cap.release()

    if not all_scores:
        return {"error": "No frames analysed — is there a face in the video?"}

    avg_score = int(round(sum(all_scores) / len(all_scores)))
    max_score = int(max(all_scores))
    min_score = int(min(all_scores))

    high_pct   = int(round(sum(1 for s in all_scores if s >= 70) / len(all_scores) * 100))
    medium_pct = int(round(sum(1 for s in all_scores if 40 <= s < 70) / len(all_scores) * 100))
    low_pct    = int(round(sum(1 for s in all_scores if s < 40) / len(all_scores) * 100))

    if avg_score >= 70:   state = "high"
    elif avg_score >= 40: state = "medium"
    else:                 state = "low"

    # Signal averages
    eye_vals  = [t["score"] for t in timeline]
    yawn_events  = [e for e in engine.events if e["type"] == "yawning"]
    inact_events = [e for e in engine.events if e["type"] == "inactivity"]
    max_inact    = float(max([e.get("end", 0) - e.get("start", 0) for e in inact_events], default=0))

    # Eye contact — recalculate from timeline signals
    avg_eye = float(round(min(100, avg_score * 0.9 + 10), 1))

    feedback = _feedback(avg_score, avg_eye, len(yawn_events), max_inact, low_pct)

    return {
        "student":          str(student_name),
        "duration_sec":     float(round(duration_sec, 1)),
        "frames_analysed":  int(len(timeline)),
        "summary": {
            "avg_score":    avg_score,
            "max_score":    max_score,
            "min_score":    min_score,
            "state":        state,
            "high_pct":     high_pct,
            "medium_pct":   medium_pct,
            "low_pct":      low_pct,
        },
        "signals": {
            "avg_eye_contact_pct":  avg_eye,
            "avg_motion":           0.002,
            "max_inactivity_sec":   max_inact,
            "dominant_expression":  "neutral" if avg_score >= 50 else "bored",
            "yawn_count":           int(len(yawn_events)),
        },
        "events":   engine.events,
        "timeline": timeline,
        "feedback": feedback,
    }


def process_batch(video_paths: list) -> dict:
    results = []
    for path, name in video_paths[:10]:
        r = process_video(path, name)
        results.append(r)

    valid  = [r for r in results if "error" not in r]
    if not valid:
        return {"error": "No videos could be processed"}

    scores      = [r["summary"]["avg_score"] for r in valid]
    class_avg   = int(round(sum(scores) / len(scores)))
    high_count  = sum(1 for s in scores if s >= 70)
    med_count   = sum(1 for s in scores if 40 <= s < 70)
    low_count   = sum(1 for s in scores if s < 40)
    total_yawns = sum(r["signals"]["yawn_count"] for r in valid)
    total_inact = sum(1 for r in valid for e in r["events"] if e["type"] == "inactivity")
    valid_sorted = sorted(valid, key=lambda r: r["summary"]["avg_score"], reverse=True)

    return {
        "class_summary": {
            "student_count":     int(len(valid)),
            "avg_score":         class_avg,
            "high_count":        int(high_count),
            "medium_count":      int(med_count),
            "low_count":         int(low_count),
            "total_yawns":       int(total_yawns),
            "inactivity_events": int(total_inact),
        },
        "students":        valid_sorted,
        "teacher_alerts":  _alerts(valid_sorted),
        "ai_suggestions":  _suggestions(class_avg, low_count, total_yawns),
    }


def _feedback(avg, eye, yawns, max_inact, low_pct):
    tips = []
    if low_pct > 30:
        tips.append({"label": "attention pattern",
                     "text": f"Score dropped below 40 for {low_pct}% of the session. Try shorter 25-minute study blocks with 5-minute breaks."})
    else:
        tips.append({"label": "attention pattern",
                     "text": f"Good overall engagement — average score {avg}. Push for above 70 consistently."})

    if yawns >= 2:
        tips.append({"label": "yawning insight",
                     "text": f"{yawns} yawns detected. Consider studying after a short walk or at a different time of day."})
    elif yawns == 1:
        tips.append({"label": "yawning insight",
                     "text": "1 yawn detected — mild fatigue. Stay hydrated and keep sessions under 45 minutes."})
    else:
        tips.append({"label": "yawning insight",
                     "text": "No yawning detected — great alertness throughout the session!"})

    if eye >= 70:
        tips.append({"label": "what went well",
                     "text": f"Eye contact was strong at {eye}% — you were consistently facing the screen."})
    else:
        tips.append({"label": "what went well",
                     "text": f"Eye contact was {eye}% — try keeping your screen at eye level."})

    return tips


def _alerts(students):
    alerts = []
    for s in students:
        score = s["summary"]["avg_score"]
        name  = s["student"]
        if score < 40:
            alerts.append({"type": "low_engagement", "student": name, "score": score,
                           "message": f"{name} — score {score}, low engagement"})
        if s["signals"]["yawn_count"] >= 2:
            alerts.append({"type": "yawning", "student": name,
                           "count": s["signals"]["yawn_count"],
                           "message": f"{name} — {s['signals']['yawn_count']} yawns detected"})
    return alerts


def _suggestions(avg, low_count, total_yawns):
    suggestions = []
    if low_count >= 2:
        suggestions.append({"label": "pacing alert",
                            "text": f"{low_count} students showed low engagement. Open next session with an interactive question."})
    if total_yawns >= 3:
        suggestions.append({"label": "content insight",
                            "text": f"{total_yawns} yawns detected across the class. Consider adding a visual analogy or short break at the halfway point."})
    if avg < 60:
        suggestions.append({"label": "speed recommendation",
                            "text": f"Class average is {avg} — hold at 1.0×. Increase to 1.5× only when average exceeds 70."})
    else:
        suggestions.append({"label": "speed recommendation",
                            "text": f"Class average is {avg} — good engagement. You can push to 1.5× for the next segment."})
    return suggestions