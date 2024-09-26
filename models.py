# models.py

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Weather(db.Model):
    __tablename__ = 'Weather_Data'
    RECORD_ID  = db.Column(db.String, primary_key=True)
    STATION_ID = db.Column(db.String(50), nullable=False)
    DATE = db.Column(db.String(50), nullable=False)
    YEAR =db.Column(db.String(50), nullable=False)
    MONTH= db.Column(db.String(50), nullable=False)
    DAY= db.Column(db.String(50), nullable=False)
    MAX_TEMP = db.Column(db.Float, nullable=False)
    MIN_TEMP = db.Column(db.Float, nullable=False)
    PRECIPITATION = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<Weather {self.STATION_ID} {self.DATE} {self.MAX_TEMP} {self.MIN_TEMP} {self.PRECIPITATION}"

class WeatherStats(db.Model):
    __tablename__ = 'Weather_stats'
    STATION_ID = db.Column(db.String(50), primary_key=True,nullable=False)
    YEAR = db.Column(db.String(50) , nullable=False)
    AVG_MAX_TEMP = db.Column(db.Float, nullable=False)
    AVG_MIN_TEMP = db.Column(db.Float, nullable=False)
    TOTAL_PRECIPITATION = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<WeatherStats {self.STATION_ID} {self.YEAR} {self.AVG_MAX_TEMP} {self.AVG_MIN_TEMP} {self.TOTAL_PRECIPITATION}>"
