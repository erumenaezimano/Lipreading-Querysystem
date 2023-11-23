from lip import app
import json
from flask import  request, redirect,make_response, url_for, flash, jsonify,Response
from lip.model import db
from lip.model import Linguistic_Type, Video_Clips, Duration, Negative_Words, User
from lip.forms import RegisterForm, LoginForm
from lip.schemas import DurationSchema, LinguisticTypeSchema, NegativeWordsSchema, NegativeSchema,VideoClipsSchema ,HomophonesSchema,VideoClipsResultSchema, DurationResultSchema,DurationLengthResultSchema,DurationSpeedResultSchema, DurationWordResultSchema
from flask_login import login_user, logout_user, login_required
from flask_jwt_extended import (
    create_access_token,
)
from flask_bcrypt import Bcrypt
from sqlalchemy import func
from sqlalchemy.orm import aliased



from sqlalchemy import func
from sqlalchemy import or_
import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps


from flask import jsonify, request, flash, redirect, url_for


# Your secret key for JWT
app.config['SECRET_KEY'] = 'theoldmanandthesea'
bcrypt = Bcrypt(app)

@app.route('/register', methods=['POST'])
def register_page():
    data = request.json
    if 'email' not in data or 'password' not in data:
        return jsonify({"error": "Missing email or password"}), 400

    email = data['email']
    password = data['password']
    username = data['username']

        
    existing_username =User.query.filter_by(username= username).first()
    if existing_username:
        return jsonify({"error": "User with this username already exists"}), 400

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"error": "User with this email already exists"}), 400




    new_user = User(email=email, password= password,username=username)
    db.session.add(new_user)
    db.session.commit()
    accesstoken = jwt.encode({
        'user_id': new_user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Token expiration time
    }, app.config['SECRET_KEY'], algorithm='HS256')
    
    return {"message":"user_created","token": accesstoken}
   

@app.route('/login', methods=['POST'])
def login_page():
    data = request.get_json()
    email = data['email']
    password = data['password']
   

    user = User.query.filter_by(email=email).first()
    if user and bcrypt.check_password_hash(user.password, password):
        accesstoken = jwt.encode({
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Token expiration time
        }, app.config['SECRET_KEY'], algorithm='HS256')
        return {"message":"user_created","token": accesstoken}
    return jsonify({'message': 'Invalid credentials'}), 401


@app.route('/search', methods=['GET', 'POST'])
#@login_required
def search():
        if request.method == 'GET':
            criteria = request.args.get('criteria', default='', type=str)
            user_input = request.args.get('user_input', default='', type=str)
        elif request.method == 'POST':
            criteria = request.form.get('criteria', default='', type=str)
            user_input = request.form.get('user_input', default='', type=str)
    
        batch_size = 1000

        homophone_results = []
        visemes_results = []
        phonemes_results = []
        vowels_results = []
        duration_results = []
        negative_words_results = []

    
        if criteria == 'Homophone':
            homophone_results_query = db.session.query(Linguistic_Type, Video_Clips.subtitle, Video_Clips.video_id, Video_Clips.video_duration_sec, Linguistic_Type.word, Linguistic_Type.duration_sec, Linguistic_Type.homophones, Linguistic_Type.HH) \
                .join(Linguistic_Type, Video_Clips.video_id == Linguistic_Type.video_id) \
                .filter(func.lower(Linguistic_Type.word) == func.lower(user_input)) \
                .limit(batch_size).all()
            for result in homophone_results_query:
                h_result = LinguisticTypeSchema().dump(result)
                homophone_results.append(h_result)

        
        elif criteria == 'Visemes':
            visemes_results_query = db.session.query(Linguistic_Type, Video_Clips.subtitle, Video_Clips.video_id, Video_Clips.video_duration_sec, Linguistic_Type.word, Linguistic_Type.duration_sec, Linguistic_Type.visemes) \
                .join(Linguistic_Type, Video_Clips.video_id == Linguistic_Type.video_id) \
                .filter(func.lower(Linguistic_Type.word) == func.lower(user_input)) \
                .limit(batch_size).all()
            for result in visemes_results_query:
                vs_result = LinguisticTypeSchema().dump(result)
                visemes_results.append(vs_result)
        
        
        elif criteria == 'Phonemes':
            phonemes_results_query = db.session.query(Linguistic_Type, Video_Clips.subtitle, Video_Clips.video_id, Video_Clips.video_duration_sec, Linguistic_Type.word, Linguistic_Type.duration_sec, Linguistic_Type.phonemes) \
                .join(Linguistic_Type, Video_Clips.video_id == Linguistic_Type.video_id) \
                .filter(func.lower(Linguistic_Type.word) == func.lower(user_input)) \
                .limit(batch_size).all()
            for result in phonemes_results_query:
                p_result = LinguisticTypeSchema().dump(result)
                phonemes_results.append(p_result)

        
        elif criteria == 'Vowels':
            vowels_results_query = db.session.query(Duration, Video_Clips.subtitle, Video_Clips.video_id, Video_Clips.video_duration_sec, Duration.duration_sec, Duration.word, Duration.vowel) \
                .join(Duration, Video_Clips.video_id == Duration.video_id) \
                .filter(func.lower(Duration.word) == func.lower(user_input)) \
                .limit(batch_size).all()
            for result in vowels_results_query:
                v_result = DurationSchema().dump(result)
                vowels_results.append(v_result)
                

            
        elif criteria == 'Duration':
            duration_results_query = db.session.query(Duration, Video_Clips.subtitle, Video_Clips.video_id, Video_Clips.video_duration_sec, Duration.word, Duration.duration_sec, Duration.word_speed) \
                .join(Duration, Video_Clips.video_id == Duration.video_id) \
                .filter(func.lower(Duration.word) == func.lower(user_input)) | (Duration.duration_sec.is_(None)) \
                .limit(batch_size).all()
            for result in duration_results_query:
                d_result = DurationSchema().dump(result)
                duration_results.append(d_result)
                


            
        elif criteria == 'Negative Words':
            negative_words_results_query= db.session.query(Negative_Words, Video_Clips.video_id, Video_Clips.subtitle, Duration.duration_sec, Video_Clips.video_duration_sec, Negative_Words.word) \
                .join(Negative_Words, Video_Clips.video_id == Negative_Words.video_id) \
                .join(Duration, Duration.w_id == Negative_Words.w_id) \
                .filter(func.lower(Negative_Words.word) == func.lower(user_input)) \
                .limit(batch_size).all()
            for result in negative_words_results_query:
                nw_result = NegativeWordsSchema().dump(result)
                print(nw_result)
                negative_words_results.append(nw_result)
                  
        
             
           
        #print(nw_result)


        db.session.commit()
        results = {
            'Homophone': homophone_results,
            'Visemes': visemes_results,
            'Phonemes': phonemes_results,
            'Vowels': vowels_results,
            'Duration': duration_results,
            'Negative Words': negative_words_results,
            'criteria': criteria
        }

    # Serialize the results to JSON
        json_results = json.dumps(results, default=str)  # Using default=str to handle non-serializable types

       #print("API Response:", json_results)

        return json_results, 200

@app.route('/getVideoclips', methods=['GET', 'POST'])
def queryVideoclips():
        # Query to count records in Duration table linked to each Video_Clips record
    result_array=[]
    query = (
        db.session.query(
            Video_Clips.video_length,
            func.count().label('record_count')
        )
        .group_by(Video_Clips.video_length)
    )
    video_results_query = query.all()

    for result in  video_results_query :
        nw_result = VideoClipsResultSchema().dump(result)
        result_array.append(nw_result)

    json_results = json.dumps(result_array, default=str)  # Using default=str to handle non-serializable types


    return json_results, 200




@app.route('/getHomephones', methods=['GET', 'POST'])
def queryHomophones():
        
    result_array=[]
    query = (
        db.session.query(
            Linguistic_Type.HH,
            func.count().label('record_count')
        )
        .group_by(Linguistic_Type.HH)
    )
    homophones_results_query = query.all()

    for result in homophones_results_query:
        nw_result = HomophonesSchema().dump(result)
        result_array.append(nw_result)

    json_results = json.dumps(result_array, default=str)  


    return json_results, 200

@app.route('/partofspeech', methods=['GET', 'POST'])
def getduration():
        # Query to count records in Duration table linked to each Video_Clips record
    result_array=[]
    query = (
        db.session.query(
            Duration.part_of_speech,
            func.count().label('record_count')
        )
        .group_by(Duration.part_of_speech)
    )
    homophones_results_query = query.all()

    for result in homophones_results_query[1:]:
        
        nw_result = DurationResultSchema().dump(result)
        result_array.append(nw_result)

    json_results = json.dumps(result_array, default=str)

    
    return json_results, 200

@app.route('/wordSpeed', methods=['GET', 'POST'])
def getSpeed():
        # Query to count records in Duration table linked to each Video_Clips record
    result_array=[]
    query = (
        db.session.query(
            Duration.word_speed,
            func.count().label('record_count')
        )
        .group_by(Duration.word_speed)
    )
    homophones_results_query = query.all()

  
    for result in homophones_results_query[1:]:
        nw_result = DurationSpeedResultSchema().dump(result)
        result_array.append(nw_result)

    json_results = json.dumps(result_array, default=str)

    
    return json_results, 200

@app.route('/wordLength', methods=['GET', 'POST'])
def getLength():
        # Query to count records in Duration table linked to each Video_Clips record
    result_array=[]
    query = (
        db.session.query(
            Duration.word_length,
            func.count().label('record_count')
        )
        .group_by(Duration.word_length)
    )
    homophones_results_query = query.all()


    for result in homophones_results_query[1:]:
        nw_result = DurationLengthResultSchema().dump(result)
        result_array.append(nw_result)
    


    json_results = json.dumps(result_array, default=str)

    
    return json_results, 200


@app.route('/negative', methods=['GET', 'POST'])
def getNegative():
        # Query to count records in Duration table linked to each Video_Clips record
    result_array=[]
    query = (
        db.session.query(
            Negative_Words.word,
            func.count().label('record_count')
        )
        .group_by(Negative_Words.word)
    )
    homophones_results_query = query.all()


    for result in homophones_results_query[1:]:
        nw_result = NegativeSchema().dump(result)
        result_array.append(nw_result)
    

    json_results = json.dumps(result_array, default=str)

    
    return json_results, 200


@app.route('/wordFrequency', methods=['GET', 'POST'])
def getWordFrequency():
    result_array = []
    query = (
        db.session.query(
            Duration.word,
            func.count().label('record_count')
        )
        .group_by(Duration.word)
        .having(func.length(Duration.word) > 4)  # Filter words with more than 5 letters
        .order_by(func.count().desc())  # Order by count in descending order
        .limit(15)  # Limit
    )

    word_frequency = query.all()
    logging.info("Word Frequency Results:")
    for result in word_frequency[1:]:
        nw_result = DurationWordResultSchema().dump(result)
        result_array.append(nw_result)
        logging.info(f"Word: {nw_result['word']}, Count: {nw_result['record_count']}")
    json_results = json.dumps(result_array, default=str)

    
    return json_results, 200


    



#@app.route('/check_connection', methods=['GET'])
#def check_connection():
    #return jsonify(message="Backend connection is working")