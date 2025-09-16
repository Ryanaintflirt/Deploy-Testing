from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_cors import CORS
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import requests
import os
from dotenv import load_dotenv
import json
from datetime import datetime
from models import db, User, MedicalInfofuser, Doctor
import numpy as np
import pickle

# Load environment variables
load_dotenv('SECRET.env')

app = Flask(__name__)

# Load models at startup
app.secret_key = 'tytawthutithokthantohtktktrtrtwrti'

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///healthcare_users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
CORS(app)

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#Load ML Models
def load_models():
    try:
        working_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Load heart disease model
        heart_model_path = os.path.join(working_dir, 'saved_models', 'heart_disease_model.pkl')
        if os.path.exists(heart_model_path):
            heart_model = pickle.load(open(heart_model_path, 'rb'))
            print("Heart model loaded successfully")
        else:
            heart_model = None
            print("Heart model not found")
        
        # Load diabetes model
        diabetes_model_path = os.path.join(working_dir, 'saved_models', 'diabetes_model.pkl')
        if os.path.exists(diabetes_model_path):
            diabetes_model = pickle.load(open(diabetes_model_path, 'rb'))
            print("Diabetes model loaded successfully")

        else:
            diabetes_model = None
            print("Diabetes model not found")
            
        # Load Parkinson's model
        parkinsons_model_path = os.path.join(working_dir, 'saved_models', 'parkinsons_model.pkl')
        if os.path.exists(parkinsons_model_path):
            parkinsons_model = pickle.load(open(parkinsons_model_path, 'rb'))
            print("Parkinsons model loaded successfully")
        else:
            print("Parkinsons model not found")
            parkinsons_model = None
        
        return {
            'heart': heart_model,
            'diabetes': diabetes_model,
            'parkinsons': parkinsons_model
        }
    except Exception as e:
        print(f"Error loading models: {str(e)}")
        return {
            'heart': None,
            'diabetes': None,
            'parkinsons': None
        }

# Firebase Configuration
FIREBASE_CONFIG = {
    "apiKey": "AIzaSyDBJt1k0mgiEiC3CT27GbUwoQrKId4dXm0",
    "authDomain": "healthcare-620a8.firebaseapp.com",
    "projectId": "healthcare-620a8",
    "storageBucket": "healthcare-620a8.firebasestorage.app",
    "messagingSenderId": "992957587185",
    "appId": "1:130404881524:web:013a99a998da81c48ead21",
    "measurementId": "G-CJXL0BMB4J",
    "databaseURL": "https://healthcare-620a8-default-rtdb.firebaseio.com/"
}

# AI Chatbot Configuration
API_KEY = "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"
CHATBOT_URL = "https://openrouter.ai/api/v1/chat/completions"
CHATBOT_HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "HTTP-Referer": "https://www.HealthCareAi.com",
    "X-Title": "HealthCare",
    "Content-Type": "application/json"
}



@app.route('/')
def index():
    username = current_user.username if current_user.is_authenticated else None
    return render_template("index.html", username=username)

@app.route('/init-db')
def init_db():
    """Initialize the database with tables"""
    try:
        with app.app_context():
            db.create_all()
        return jsonify({'message': 'Database initialized successfully!'})
    except Exception as e:
        return jsonify({'error': f'Database initialization failed: {str(e)}'}), 500

@app.route('/populate-doctors')
def populate_doctors():
    """Populate the database with doctor data"""
    try:
        with app.app_context():
            # Check if doctors already exist
            if Doctor.query.first():
                return jsonify({'message': 'Doctors already exist in database!'})
            
            # Create doctor records
            doctors_data = [
                {
                    'full_name': 'Dr. Sophia Tan',
                    'gender': 'Female',
                    'date_of_birth': datetime.strptime('1982-05-10', '%Y-%m-%d').date(),
                    'specialty': 'Cardiologist',
                    'phone_number': '09123456789',
                    'email': 'sophia.tan@hospital.com',
                    'available_days': 'Monday, Wednesday, Friday',
                    'available_time': '09:00 - 12:00',
                    'years_experience': 15,
                    'qualification': 'MD, FACC',
                    'profile_photo': 'https://i.pinimg.com/736x/1b/52/fd/1b52fd81c2282b432b85dc6a8a01f13d.jpg',
                    'bio': 'Experienced cardiologist with expertise in heart disease prevention and treatment.'
                },
                {
                    'full_name': 'Dr. Michael Lee',
                    'gender': 'Male',
                    'date_of_birth': datetime.strptime('1978-08-24', '%Y-%m-%d').date(),
                    'specialty': 'Pediatrician',
                    'phone_number': '09987654321',
                    'email': 'michael.lee@hospital.com',
                    'available_days': 'Tuesday, Thursday, Saturday',
                    'available_time': '13:00 - 17:00',
                    'years_experience': 20,
                    'qualification': 'MD, FAAP',
                    'profile_photo': 'https://i.pinimg.com/736x/24/09/4f/24094f8bd75f092e7074c8b5e9d17265.jpg',
                    'bio': 'Dedicated pediatrician providing compassionate care for children of all ages.'
                },
                {
                    'full_name': 'Dr. Aye Chan',
                    'gender': 'Female',
                    'date_of_birth': datetime.strptime('1985-02-18', '%Y-%m-%d').date(),
                    'specialty': 'Dermatologist',
                    'phone_number': '09555444333',
                    'email': 'aye.chan@hospital.com',
                    'available_days': 'Monday, Thursday',
                    'available_time': '10:00 - 15:00',
                    'years_experience': 12,
                    'qualification': 'MBBS, Diploma in Dermatology',
                    'profile_photo': 'https://i.pinimg.com/736x/47/a4/44/47a4448f2df0046ee1f7bed28f87e551.jpg',
                    'bio': 'Specialist in treating skin conditions and cosmetic dermatology procedures.'
                },
                {
                    'full_name': 'Dr. John Smith',
                    'gender': 'Male',
                    'date_of_birth': datetime.strptime('1975-11-03', '%Y-%m-%d').date(),
                    'specialty': 'Orthopedic Surgeon',
                    'phone_number': '09771234567',
                    'email': 'john.smith@hospital.com',
                    'available_days': 'Wednesday, Friday',
                    'available_time': '08:00 - 12:00',
                    'years_experience': 22,
                    'qualification': 'MD, MS (Ortho)',
                    'profile_photo': 'https://i.pinimg.com/736x/e6/13/d9/e613d9a7aec9c000f2ed32756148e5e6.jpg',
                    'bio': 'Orthopedic surgeon focused on joint replacement and sports injury treatments.'
                }
            ]
            
            for doctor_data in doctors_data:
                doctor = Doctor(**doctor_data)
                db.session.add(doctor)
            
            db.session.commit()
            return jsonify({'message': f'Successfully added {len(doctors_data)} doctors to database!'})
            
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to populate doctors: {str(e)}'}), 500

@app.route('/debug')
def debug():
    """Debug route to check Firebase configuration"""
    return jsonify({
        'firebase_config': FIREBASE_CONFIG,
        'session': dict(session),
        'status': 'OK'
    })

def verify_firebase_token(id_token):
    """Verify Firebase ID token using REST API"""
    try:
        # Firebase REST API endpoint for token verification
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:lookup?key={FIREBASE_CONFIG['apiKey']}"
        
        payload = {"idToken": id_token}
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            if 'users' in data and len(data['users']) > 0:
                user = data['users'][0]
                return {
                    'uid': user.get('localId'),
                    'email': user.get('email', ''),
                    'name': user.get('displayName', ''),
                    'email_verified': user.get('emailVerified', False)
                }
        return None
    except Exception as e:
        print(f"Token verification error: {e}")
        return None

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            data = request.get_json()
            auth_type = data.get('authType', 'firebase')  # 'firebase' or 'custom'
            
            if auth_type == 'firebase':
                # Firebase Google authentication
                id_token = data.get('idToken')
                
                if not id_token:
                    return jsonify({'error': 'No ID token provided'}), 400
                
                # Verify the ID token using Firebase REST API
                user_data = verify_firebase_token(id_token)
                
                if not user_data:
                    return jsonify({'error': 'Invalid token'}), 401
                
                # Check if user exists in our database
                user = User.query.filter_by(firebase_uid=user_data['uid']).first()
                
                if not user:
                    # Create new Google user
                    user = User.create_google_user(
                        firebase_uid=user_data['uid'],
                        email=user_data['email'],
                        full_name=user_data['name'],
                        profile_picture=user_data.get('photoURL')
                    )
                
                # Update last login
                user.last_login = datetime.utcnow()
                db.session.commit()
                
                # Login user with Flask-Login
                login_user(user, remember=True)
                
                return jsonify({
                    'success': True,
                    'message': 'Google login successful!',
                    'user': user.to_dict()
                })
                
            elif auth_type == 'custom':
                # Custom email/password authentication
                email = data.get('email')
                password = data.get('password')
                
                if not email or not password:
                    return jsonify({'error': 'Email and password are required'}), 400
                
                # Find user by email
                user = User.query.filter_by(email=email, auth_method='custom').first()
                
                if not user or not user.check_password(password):
                    return jsonify({'error': 'Invalid email or password'}), 401
                
                if not user.is_active:
                    return jsonify({'error': 'Account is deactivated'}), 401
                
                # Update last login
                user.last_login = datetime.utcnow()
                db.session.commit()
                
                # Login user with Flask-Login
                login_user(user, remember=True)
                
                return jsonify({
                    'success': True,
                    'message': 'Login successful!',
                    'user': user.to_dict()
                })
            
            else:
                return jsonify({'error': 'Invalid authentication type'}), 400
                
        except Exception as e:
            return jsonify({'error': f'Authentication failed: {str(e)}'}), 500
    
    return render_template("login.html", firebase_config=FIREBASE_CONFIG)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            data = request.get_json()
            print(f"🔍 Registration request received: {data}")
            auth_type = data.get('authType', 'firebase')  # 'firebase' or 'custom'
            print(f"🔍 Auth type: {auth_type}")
            
            if auth_type == 'firebase':
                # Firebase Google registration
                id_token = data.get('idToken')
                fullname = data.get('fullname', '')
                
                if not id_token:
                    return jsonify({'error': 'No ID token provided'}), 400
                
                # Verify the ID token using Firebase REST API
                user_data = verify_firebase_token(id_token)
                
                if not user_data:
                    return jsonify({'error': 'Invalid token'}), 401
                
                # Check if user already exists
                existing_user = User.query.filter_by(firebase_uid=user_data['uid']).first()
                if existing_user:
                    return jsonify({'error': 'User already exists with this Google account'}), 400
                
                # Check if email already exists with custom auth
                existing_email = User.query.filter_by(email=user_data['email']).first()
                if existing_email:
                    return jsonify({'error': 'Email already registered. Please use custom login or link your Google account.'}), 400
                
                # Create new Google user
                user = User.create_google_user(
                    firebase_uid=user_data['uid'],
                    email=user_data['email'],
                    full_name=user_data['name'] or fullname,
                    profile_picture=user_data.get('photoURL')
                )
                
                # Login user with Flask-Login
                login_user(user, remember=True)
                
                return jsonify({
                    'success': True,
                    'message': 'Google registration successful!',
                    'user': user.to_dict()
                })
                
            elif auth_type == 'custom':
                # Custom email/password registration
                username = data.get('username')
                email = data.get('email')
                password = data.get('password')
                fullname = data.get('fullname', '')
                
                print(f"🔍 Custom registration data: username={username}, email={email}, fullname={fullname}")
                
                if not all([username, email, password]):
                    print(f"❌ Missing required fields: username={bool(username)}, email={bool(email)}, password={bool(password)}")
                    return jsonify({'error': 'Username, email, and password are required'}), 400
                
                # Check if username already exists
                existing_username = User.query.filter_by(username=username).first()
                if existing_username:
                    print(f"❌ Username already exists: {username}")
                    return jsonify({'error': 'Username already exists'}), 400
                
                # Check if email already exists
                existing_email = User.query.filter_by(email=email).first()
                if existing_email:
                    print(f"❌ Email already registered: {email}")
                    return jsonify({'error': 'Email already registered'}), 400
                
                print(f"✅ Creating new user: {username}")
                
                # Create new custom user
                user = User.create_custom_user(
                    username=username,
                    email=email,
                    password=password,
                    full_name=fullname
                )
                
                print(f"✅ User created successfully: {user.username} (ID: {user.id})")
                
                # Login user with Flask-Login
                login_user(user, remember=True)
                
                print(f"✅ User logged in successfully")
                
                return jsonify({
                    'success': True,
                    'message': 'Registration successful!',
                    'user': user.to_dict()
                })
            
            else:
                return jsonify({'error': 'Invalid authentication type'}), 400
                
        except Exception as e:
            print(f"❌ Registration exception: {str(e)}")
            import traceback
            traceback.print_exc()
            return jsonify({'error': f'Registration failed: {str(e)}'}), 500
    
    return render_template("register.html", firebase_config=FIREBASE_CONFIG)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out successfully!', 'success')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template("index.html", username=current_user.username)

@app.route('/home')
@login_required
def home():
    return render_template("home.html", username=current_user.username)

@app.route('/test-ai')
@login_required
def test_ai():
    """Test route to check AI API connection"""
    
    try:
        payload = {
            "model": "deepseek/deepseek-r1:free",
            "messages": [
                {
                    "role": "user", 
                    "content": "Hello, are you working?"
                }
            ]
        }
        
        print("Testing AI API connection...")
        response = requests.post(CHATBOT_URL, headers=CHATBOT_HEADERS, json=payload, timeout=10)
        
        return jsonify({
            'status': response.status_code,
            'response': response.text[:500] if response.text else 'No response text',
            'headers': dict(response.headers)
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'type': type(e).__name__
        })

@app.route('/ask', methods=['POST'])
@login_required
def ask():
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
            
        prompt = data.get('prompt', '')
        
        if not prompt:
            return jsonify({'error': 'No prompt provided'}), 400
        
        print(f"User {current_user.username} asked: {prompt}")
        
        # Prepare the payload for the AI API
        payload = {
            "model": "deepseek/deepseek-r1:free",
            "messages": [
                {
                    "role": "system", 
                    "content": "You are a helpful AI Health Assistant. Provide accurate, helpful health information and advice. Always remind users to consult with healthcare professionals for serious medical concerns.If user ask other question except medical question, say that you don't know.  Use five sentences maximum and keep the answer concise."
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ]
        }
        
        print(f"Sending request to AI API...")
        
        response = requests.post(CHATBOT_URL, headers=CHATBOT_HEADERS, json=payload, timeout=30)
        
        print(f"API Response Status: {response.status_code}")
        
        if response.status_code != 200:
            print(f"API Error Response: {response.text}")
            return jsonify({'error': f'AI service error: {response.status_code}'}), 503
        
        ai_data = response.json()
        print(f"API Response Data: {ai_data}")
        
        # Check if response has expected structure
        if "choices" not in ai_data or not ai_data["choices"]:
            print(f"Unexpected API response structure: {ai_data}")
            return jsonify({'error': 'AI service returned unexpected response format'}), 500
        
        reply = ai_data["choices"][0]["message"]["content"]
        print(f"AI Reply: {reply[:100]}...")
        
        return jsonify({"reply": reply})
        
    except requests.exceptions.Timeout:
        print("API request timed out")
        return jsonify({'error': 'AI service request timed out. Please try again.'}), 503
    except requests.exceptions.ConnectionError:
        print("API connection error")
        return jsonify({'error': 'Cannot connect to AI service. Please check your internet connection.'}), 503
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        return jsonify({'error': f'AI service error: {str(e)}'}), 503
    except KeyError as e:
        print(f"Unexpected API response format: {e}")
        return jsonify({'error': 'AI service returned unexpected response format'}), 500
    except Exception as e:
        print(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500

@app.route('/predict-diseases')
@login_required
def predict_diseases():
    """Route to display the disease prediction page"""
    return render_template("predit.html", username=current_user.username)

@app.route('/predict-heart')
@login_required
def predict_heart():
    """Route for heart disease prediction"""
    return render_template("preditHeart.html", username=current_user.username)

@app.route('/predict-diabetes')
@login_required
def predict_diabetes():
    """Route for diabetes prediction"""
    return render_template("preditDiabetes.html", username=current_user.username)

@app.route('/predict-parkinsons')
@login_required
def predict_parkinsons():
    """Route for Parkinson's disease prediction"""
    return render_template("preditParkinsons.html", username=current_user.username)

@app.route('/symptoms-check')
@login_required
def symptoms_check():
    """Route for symptom check page"""
    return render_template("symptomsCheck.html", username=current_user.username)

@app.route('/check-symptoms', methods=['POST'])
@login_required
def check_symptoms():
    """Route to handle symptom checking using external API"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Extract form data
        age = data.get('age')
        gender = data.get('gender')
        main_symptoms = data.get('mainSymptoms')
        onset_time = data.get('onsetTime')
        severity = data.get('severity')
        medical_history = data.get('medicalHistory', '')
        additional_info = data.get('additionalInfo', '')
        
        # Validate required fields
        if not all([age, gender, main_symptoms, onset_time, severity]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Build comprehensive description for the API
        description_parts = [
            f"Patient: {age}-year-old {gender}",
            f"Main symptoms: {main_symptoms}",
            f"Symptoms started: {onset_time}",
            f"Severity: {severity}"
        ]
        
        if medical_history:
            description_parts.append(f"Medical history: {medical_history}")
        
        if additional_info:
            description_parts.append(f"Additional information: {additional_info}")
        
        # Create comprehensive description (200-2000 characters as recommended)
        description = ". ".join(description_parts) + "."
        
        # Ensure description is within recommended length
        if len(description) > 2000:
            description = description[:1997] + "..."
        
        # Prepare API request payload (using the same structure as symptomCheck.py)
        import uuid
        myuuid = str(uuid.uuid4())
        
        api_url = "https://dxgpt-apim.azure-api.net/api/diagnose"
        headers = {
            "Ocp-Apim-Subscription-Key": "aeb1f678b16e40cdb828bd14c0838488",
            "Content-Type": "application/json"
        }
        
        payload = {
            "description": description,
            "lang": "en",
            "myuuid": myuuid,
            "model": "gpt4o",
            "response_mode": "direct",
            "timezone": "America/New_York"
        }
        
        # Make API request
        import requests
        response = requests.post(api_url, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            api_data = response.json()
            
            if "data" in api_data and api_data["data"]:
                # Format the response for the frontend
                diagnoses = []
                for item in api_data["data"]:
                    diagnoses.append({
                        "diagnosis": item.get('diagnosis', 'Unknown'),
                        "description": item.get('description', 'No description available'),
                    })
                
                return jsonify({
                    "success": True,
                    "diagnoses": diagnoses,
                    "total_found": len(diagnoses)
                })
            else:
                return jsonify({
                    "success": True,
                    "diagnoses": [],
                    "message": "No specific diagnoses found based on the provided symptoms."
                })
        else:
            print(f"Symptom check API error: {response.status_code} - {response.text}")
            return jsonify({'error': 'External symptom analysis service is currently unavailable'}), 503
            
    except requests.exceptions.Timeout:
        return jsonify({'error': 'Symptom analysis request timed out. Please try again.'}), 503
    except requests.exceptions.ConnectionError:
        return jsonify({'error': 'Cannot connect to symptom analysis service. Please check your internet connection.'}), 503
    except Exception as e:
        print(f"Error in symptom checking: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'An error occurred during symptom analysis. Please try again.'}), 500

@app.route('/doctors')
@login_required
def doctors():
    """Route for doctors page"""
    # Fetch all doctors from database
    doctors = Doctor.query.all()
    return render_template("Doctors.html", username=current_user.username, doctors=doctors)

@app.route('/predict-heart-disease', methods=['POST'])
@login_required
def predict_heart_disease():
    """Route to handle heart disease prediction"""
    try:
        if not ML_MODELS['heart']:
            return jsonify({'error': 'Heart disease prediction model is not available'}), 503
        
        # Get form data
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Extract and validate input parameters
        required_fields = ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 
                          'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal']
        
        # Check if all required fields are present
        missing_fields = [field for field in required_fields if field not in data or data[field] is None]
        if missing_fields:
            return jsonify({'error': f'Missing required fields: {", ".join(missing_fields)}'}), 400
        
        # Convert to numpy array in the correct order
        try:
            input_data = np.array([
                float(data['age']),
                float(data['sex']),
                float(data['cp']),
                float(data['trestbps']),
                float(data['chol']),
                float(data['fbs']),
                float(data['restecg']),
                float(data['thalach']),
                float(data['exang']),
                float(data['oldpeak']),
                float(data['slope']),
                float(data['ca']),
                float(data['thal'])
            ]).reshape(1, -1)
        except (ValueError, TypeError) as e:
            return jsonify({'error': f'Invalid input data: {str(e)}'}), 400
        
        # Make prediction
        prediction = ML_MODELS['heart'].predict(input_data)[0]
        
        # Get prediction probability if available
        confidence = None
        try:
            if hasattr(ML_MODELS['heart'], 'predict_proba'):
                probabilities = ML_MODELS['heart'].predict_proba(input_data)[0]
                confidence = round(max(probabilities) * 100, 2)
        except:
            pass
        
        # Prepare response
        result = {
            'prediction': int(prediction),
            'confidence': confidence,
            'message': 'Heart disease risk detected' if prediction == 1 else 'Low heart disease risk'
        }
        
        print(f"Heart disease prediction for user {current_user.username}: {result}")
        
        return jsonify(result)
        
    except Exception as e:
        print(f"Error in heart disease prediction: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'An error occurred during prediction. Please try again.'}), 500

@app.route('/predict-diabetes-disease', methods=['POST'])
@login_required
def predict_diabetes_disease():
    """Route to handle diabetes prediction"""
    try:
        if not ML_MODELS['diabetes']:
            return jsonify({'error': 'Diabetes prediction model is not available'}), 503
        
        # Get form data
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Extract and validate input parameters for diabetes
        required_fields = ['pregnancies', 'glucose', 'bloodpressure', 'skinthickness', 
                          'insulin', 'bmi', 'diabetespedigreefunction', 'age']
        
        # Check if all required fields are present
        missing_fields = [field for field in required_fields if field not in data or data[field] is None]
        if missing_fields:
            return jsonify({'error': f'Missing required fields: {", ".join(missing_fields)}'}), 400
        
        # Convert to numpy array in the correct order (matching the diabetes dataset)
        try:
            input_data = np.array([
                float(data['pregnancies']),
                float(data['glucose']),
                float(data['bloodpressure']),
                float(data['skinthickness']),
                float(data['insulin']),
                float(data['bmi']),
                float(data['diabetespedigreefunction']),
                float(data['age'])
            ]).reshape(1, -1)
        except (ValueError, TypeError) as e:
            return jsonify({'error': f'Invalid input data: {str(e)}'}), 400
        
        # Make prediction
        prediction = ML_MODELS['diabetes'].predict(input_data)[0]
        
        # Get prediction probability if available
        confidence = None
        try:
            if hasattr(ML_MODELS['diabetes'], 'predict_proba'):
                probabilities = ML_MODELS['diabetes'].predict_proba(input_data)[0]
                confidence = round(max(probabilities) * 100, 2)
        except:
            pass
        
        # Prepare response
        result = {
            'prediction': int(prediction),
            'confidence': confidence,
            'message': 'Diabetes risk detected' if prediction == 1 else 'Low diabetes risk'
        }
        
        print(f"Diabetes prediction for user {current_user.username}: {result}")
        
        return jsonify(result)
        
    except Exception as e:
        print(f"Error in diabetes prediction: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'An error occurred during prediction. Please try again.'}), 500

@app.route('/predict-parkinsons-disease', methods=['POST'])
@login_required
def predict_parkinsons_disease():
    """Route to handle Parkinson's disease prediction"""
    try:
        if not ML_MODELS['parkinsons']:
            return jsonify({'error': 'Parkinson\'s disease prediction model is not available'}), 503
        
        # Get form data
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Extract and validate input parameters for Parkinson's (matching preditEg.py)
        required_fields = ['fo', 'fhi', 'flo', 'Jitter_percent', 'Jitter_Abs', 
                          'RAP', 'PPQ', 'DDP', 'Shimmer', 'Shimmer_dB', 'APQ3', 'APQ5', 
                          'APQ', 'DDA', 'NHR', 'HNR', 'RPDE', 'DFA', 
                          'spread1', 'spread2', 'D2', 'PPE']
        
        # Check if all required fields are present
        missing_fields = [field for field in required_fields if field not in data or data[field] is None]
        if missing_fields:
            return jsonify({'error': f'Missing required fields: {", ".join(missing_fields)}'}), 400
        
        # Convert to numpy array in the correct order (matching preditEg.py)
        try:
            input_data = np.array([
                float(data['fo']),
                float(data['fhi']),
                float(data['flo']),
                float(data['Jitter_percent']),
                float(data['Jitter_Abs']),
                float(data['RAP']),
                float(data['PPQ']),
                float(data['DDP']),
                float(data['Shimmer']),
                float(data['Shimmer_dB']),
                float(data['APQ3']),
                float(data['APQ5']),
                float(data['APQ']),
                float(data['DDA']),
                float(data['NHR']),
                float(data['HNR']),
                float(data['RPDE']),
                float(data['DFA']),
                float(data['spread1']),
                float(data['spread2']),
                float(data['D2']),
                float(data['PPE'])
            ]).reshape(1, -1)
        except (ValueError, TypeError) as e:
            return jsonify({'error': f'Invalid input data: {str(e)}'}), 400
        
        # Make prediction
        prediction = ML_MODELS['parkinsons'].predict(input_data)[0]
        
        # Get prediction probability if available
        confidence = None
        try:
            if hasattr(ML_MODELS['parkinsons'], 'predict_proba'):
                probabilities = ML_MODELS['parkinsons'].predict_proba(input_data)[0]
                confidence = round(max(probabilities) * 100, 2)
        except:
            pass
        
        # Prepare response
        result = {
            'prediction': int(prediction),
            'confidence': confidence,
            'message': 'Parkinson\'s disease risk detected' if prediction == 1 else 'Low Parkinson\'s disease risk'
        }
        
        print(f"Parkinson's disease prediction for user {current_user.username}: {result}")
        
        return jsonify(result)
        
    except Exception as e:
        print(f"Error in Parkinson's disease prediction: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'An error occurred during prediction. Please try again.'}), 500

@app.route('/view-profile')
@login_required
def view_profile():
    """Route to display user profile page"""
    # Load user's medical info if available
    medical = MedicalInfofuser.query.filter_by(user_id=current_user.id).first()
    print(f"🔍 Medical data for user {current_user.id} (ID: {current_user.id}): {medical}")
    print(f"🔍 All medical records: {MedicalInfofuser.query.all()}")
    if medical:
        print(f"🔍 Medical fields: full_name={medical.full_name}, gender={medical.gender}, symptoms={medical.symptoms}")
    return render_template("viewProfile.html", user=current_user, medical=medical, username=current_user.username)

@app.route('/update-profile', methods=['POST'])
@login_required
def update_profile():
    """Route to handle profile updates"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Get current user
        user = current_user
        
        # Validate and update username
        if 'username' in data and data['username']:
            new_username = data['username'].strip()
            if len(new_username) < 3:
                return jsonify({'error': 'Username must be at least 3 characters'}), 400
            
            # Check if username is already taken by another user
            existing_user = User.query.filter_by(username=new_username).first()
            if existing_user and existing_user.id != user.id:
                return jsonify({'error': 'Username already taken'}), 400
            
            user.username = new_username
        
        # Update email (only for custom accounts)
        if 'email' in data and user.auth_method == 'custom':
            new_email = data['email'].strip()
            if not new_email or '@' not in new_email:
                return jsonify({'error': 'Invalid email address'}), 400
            
            # Check if email is already taken by another user
            existing_user = User.query.filter_by(email=new_email).first()
            if existing_user and existing_user.id != user.id:
                return jsonify({'error': 'Email already registered'}), 400
            
            user.email = new_email
        
        # Update other profile fields
        if 'full_name' in data:
            user.full_name = data['full_name'].strip() if data['full_name'] else None
        
        if 'phone_number' in data:
            user.phone_number = data['phone_number'].strip() if data['phone_number'] else None
        
        if 'date_of_birth' in data and data['date_of_birth']:
            try:
                from datetime import datetime
                user.date_of_birth = datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'error': 'Invalid date format'}), 400
        
        # Update password (only for custom accounts)
        if 'password' in data and data['password'] and user.auth_method == 'custom':
            password = data['password']
            confirm_password = data.get('confirm_password', '')
            
            if len(password) < 8:
                return jsonify({'error': 'Password must be at least 8 characters'}), 400
            
            if password != confirm_password:
                return jsonify({'error': 'Passwords do not match'}), 400
            
            # Check password strength
            has_upper = any(c.isupper() for c in password)
            has_lower = any(c.islower() for c in password)
            has_digit = any(c.isdigit() for c in password)
            
            if not (has_upper and has_lower and has_digit):
                return jsonify({'error': 'Password must contain uppercase, lowercase, and number'}), 400
            
            user.set_password(password)
        
        # Save changes to database
        db.session.commit()
        
        print(f"Profile updated for user {user.username}")
        
        return jsonify({
            'success': True,
            'message': 'Profile updated successfully',
            'user': user.to_dict()
        })
        
    except Exception as e:
        print(f"Error updating profile: {str(e)}")
        import traceback
        traceback.print_exc()
        db.session.rollback()
        return jsonify({'error': 'An error occurred while updating profile'}), 500

@app.route('/update-medical-info', methods=['POST'])
@login_required
def update_medical_info():
    """Route to handle medical info update"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Get current user
        user = current_user
        
        # Update medical info in database
        medical = MedicalInfofuser.query.filter_by(user_id=user.id).first()
        print(f"🔍 Looking for medical record for user_id: {user.id}")
    
        if not medical:
            print(f"🔍 Creating new medical record for user_id: {user.id}")
            medical = MedicalInfofuser(user_id=user.id)
            db.session.add(medical)
            db.session.flush()  # Flush to get the ID
        else:
            print(f"🔍 Found existing medical record: {medical.id}")
            # Don't add existing record to session - it's already tracked
        # Update fields
        if 'full_name' in data:
            medical.full_name = data['full_name'].strip() if data['full_name'] else None
        if 'date_of_birth' in data:
            dob_str = (data['date_of_birth'] or '').strip()
            if dob_str:
                try:
                    from datetime import datetime
                    # Expecting YYYY-MM-DD from <input type="date">
                    medical.date_of_birth = datetime.strptime(dob_str, '%Y-%m-%d').date()
                except ValueError:
                    return jsonify({'error': 'Invalid date_of_birth format. Use YYYY-MM-DD'}), 400
            else:
                medical.date_of_birth = None
        if 'gender' in data:
            medical.gender = data['gender'].strip() if data['gender'] else None
        if 'phone_number' in data:
            medical.phone_number = data['phone_number'].strip() if data['phone_number'] else None
        if 'symptoms' in data:
            medical.symptoms = data['symptoms'].strip() if data['symptoms'] else None
        if 'started_time' in data:
            started_str = (data['started_time'] or '').strip()
            if started_str:
                try:
                    from datetime import datetime
                    # Expecting YYYY-MM-DDTHH:MM from <input type="datetime-local">
                    medical.started_time = datetime.strptime(started_str, '%Y-%m-%dT%H:%M')
                except ValueError:
                    # Try fallback without minutes/with seconds
                    try:
                        medical.started_time = datetime.fromisoformat(started_str)
                    except Exception:
                        return jsonify({'error': 'Invalid started_time format. Use YYYY-MM-DDTHH:MM'}), 400
            else:
                medical.started_time = None
        if 'current_medication' in data:
            medical.current_medication = data['current_medication'].strip() if data['current_medication'] else None
        if 'allergies' in data:
            medical.allergies = data['allergies'].strip() if data['allergies'] else None
            
        db.session.commit()     
        
        print(f"Medical info updated for user {user.username}")
        
        return jsonify({
            'success': True,
            'message': 'Medical info updated successfully',
            'medical': medical.to_dict()
        })
        
    except Exception as e:
        print(f"Error updating medical info: {str(e)}")
        import traceback
        traceback.print_exc()
        db.session.rollback()
        # Return detailed error to help with debugging on frontend
        return jsonify({'error': f'Update failed: {str(e)}'}), 500
@app.route('/delete-profile', methods=['DELETE'])
@login_required
def delete_profile():
    """Route to handle profile deletion"""
    try:
        user = current_user
        username = user.username
        
        # Logout user first
        logout_user()
        
        # Delete user from database
        db.session.delete(user)
        db.session.commit()
        
        print(f"Profile deleted for user {username}")
        
        return jsonify({
            'success': True,
            'message': 'Account deleted successfully'
        })
        
    except Exception as e:
        print(f"Error deleting profile: {str(e)}")
        import traceback
        traceback.print_exc()
        db.session.rollback()
        return jsonify({'error': 'An error occurred while deleting account'}), 500

@app.route('/appointment')
@login_required
def appointment():
    return render_template("appointment.html",username=current_user.username)




if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
