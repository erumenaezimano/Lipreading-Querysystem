from lip import db, login_manager
from flask_login import UserMixin
from lip import bcrypt
from sqlalchemy.orm import relationship

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    firstname = db.Column(db.String(50))
    lastname = db.Column(db.String(50))
    state = db.Column(db.String(50))
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=True)
    
    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')


    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)



class Video_Clips(db.Model):
    __tablename__ = 'video_clips'
    video_id = db.Column(db.Integer, primary_key=True)
    subtitle = db.Column(db.Text)
    video_duration_sec = db.Column(db.Float) 
    word_count = db.Column(db.Integer)
    char_count = db.Column(db.Integer)
    video_length = db.Column(db.Text)
    duration = relationship('Duration', back_populates='video_clip', foreign_keys='Duration.video_id')
    linguistic_types = relationship('Linguistic_Type', back_populates='video_clip')
    negative_words = relationship('Negative_Words', back_populates='video_clip')


class Duration(db.Model):
    __tablename__ = 'duration'
    w_id = db.Column(db.Integer, primary_key=True)
    video_id = db.Column(db.Integer, db.ForeignKey('video_clips.video_id'))
    word = db.Column(db.Text)
    duration_sec = db.Column(db.Float)
    word_speed = db.Column(db.Text)
    character_count = db.Column(db.Float)
    word_length = db.Column(db.Text)
    vowel = db.Column(db.Text)
    part_of_speech = db.Column(db.Text)
    video_clip = relationship('Video_Clips', back_populates='duration', foreign_keys=[video_id])



class Linguistic_Type(db.Model):
    __tablename__ = 'linguistic_type'
    l_id = db.Column(db.Integer, primary_key=True)
    video_id = db.Column(db.Integer, db.ForeignKey('video_clips.video_id'))
    word = db.Column(db.Text)
    duration_sec = db.Column(db.Float)
    phonemes = db.Column(db.Text)
    visemes = db.Column(db.Text)
    homophones = db.Column(db.Text)
    HH = db.Column(db.Text)
    video_clip = relationship('Video_Clips', back_populates='linguistic_types')



class Negative_Words(db.Model):
    __tablename__ = 'negative_words'
    nw_id = db.Column(db.Integer, primary_key=True)
    video_id = db.Column(db.Integer, db.ForeignKey('video_clips.video_id'))
    word = db.Column(db.Text)
    w_id = db.Column(db.Integer, db.ForeignKey('duration.w_id'))
    l_id = db.Column(db.Integer, db.ForeignKey('linguistic_type.l_id'))
    video_clip = relationship('Video_Clips', back_populates='negative_words')
