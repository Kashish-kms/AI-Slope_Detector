from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class AnalysisHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    content_type = db.Column(db.String(20)) # 'text' or 'url'
    input_data = db.Column(db.Text)
    ai_score = db.Column(db.Float)
    human_score = db.Column(db.Float)
    slop_probability = db.Column(db.Float)
    summary = db.Column(db.Text)

    def to_dict(self):
        return {
            "id": self.id,
            "timestamp": self.timestamp.strftime("%Y-%m-%d %H:%M"),
            "ai_score": round(self.ai_score * 100, 2),
            "slop_probability": round(self.slop_probability * 100, 2)
        }