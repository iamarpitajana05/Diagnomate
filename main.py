import streamlit as st
import mysql.connector
import hashlib
import os
import time
from PIL import Image
import pickle
from streamlit_option_menu import option_menu
import subprocess

st.set_page_config(page_title="DiagnoMate Assistant",
                    layout="wide",
                    page_icon="🧑‍⚕")

# Initialize session state variable to check if image has already been shown
if "image_shown" not in st.session_state:
    st.session_state.image_shown = False
placeholder = st.empty()
col1, col2, col3 = st.columns([1, 3, 1])
if not st.session_state.image_shown:
    with col2:
        image = Image.open("mdp.jpg")
        image = image.resize((950, 500))
        placeholder.image(image, use_container_width=False)
    time.sleep(3)
    # Mark the image as shown and clear it
    st.session_state.image_shown = True
    placeholder.empty()
st.markdown(
    """
    <style>
    .stRadio > div {flex-direction: row; justify-content: center;}
    .css-1v0mbdj {visibility: hidden;}
    .error-message {color: red; margin-top: 5px;}
    .success-message {color: green; margin-top: 5px;}
    .stApp {
        background-color: #f0f4f8;
    }
    .stSidebar { 
        background-color: #2f3e46;
    }
    h1, h2, h3 {
        color: #2f3e46;
        font-weight: bold;
    }
    .stButton>button {
        background-color: #f0ad4e;
        color: white;
        border-radius: 8px;
        height: 40px;
        width: 160px;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
    }
    .stInfo, .stWarning {
        padding: 10px;
        background-color: #f1f3f5;
        border-radius: 5px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# MySQL Database Connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Arpita@9128",
        database="disease_prediction"
    )

# Function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Registration Function
def registration():
    st.title("Register for DiagnoMate")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')
    confirm_password = st.text_input("Confirm Password", type='password')
    
    if st.button("Register"):
        if password != confirm_password:
            st.error("Passwords do not match!")
        else:
            try:
                conn = get_db_connection()
                cursor = conn.cursor()
                
                # Check if username already exists
                cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
                user = cursor.fetchone()
                
                if user:
                    st.error("Username already exists! Please choose a different one.")
                else:
                    hashed_password = hash_password(password)
                    cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
                    conn.commit()
                    st.success("Registration successful! Please login.")
                
            except mysql.connector.Error as err:
                st.error(f"Error: {err}")
            finally:
                cursor.close()
                conn.close()

# Login Function
def login():
    st.title("Login to DiagnoMate")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')

    if st.button("Login"):
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Check if user exists and verify password
            cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
            result = cursor.fetchone()
            
            if result:
                stored_password = result[0]
                if hash_password(password) == stored_password:
                    st.success("Login successful!")
                    st.session_state['logged_in'] = True
                    st.session_state['username'] = username
                    st.rerun()
                else:
                    st.error("Incorrect password!")
            else:
                st.error("User does not exist! Please register.")
                
        except mysql.connector.Error as err:
            st.error(f"Error: {err}")
        finally:
            cursor.close()
            conn.close()

# Main logic
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if st.session_state['logged_in']:
    if 'loading_cleared' not in st.session_state:
        loading_message = st.empty()
        loading_message.success("Wait, DiagnoMate is loading...")
        time.sleep(8)
        loading_message.empty()
        st.session_state['loading_cleared'] = True
        
    # Getting the working directory of the main.py
    working_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Loading the saved models
    diabetes_model = pickle.load(open(f'{working_dir}/saved_models/diabetes_model.sav', 'rb'))
    heart_disease_model = pickle.load(open(f'{working_dir}/saved_models/heart_disease_model.sav', 'rb'))
    corona_model = pickle.load(open(f'{working_dir}/saved_models/corona.sav', 'rb'))
    parkinsons_model = pickle.load(open(f'{working_dir}/saved_models/parkinsons_model.sav', 'rb'))
    brain_tumor_model = pickle.load(open(f'{working_dir}/saved_models/brains.sav', 'rb'))


    # Sidebar for navigation
    with st.sidebar:
        selected = option_menu('DiagnoMate Welcome To Multiple Disease Prediction System',
                            ['Dashboard',
                                'Diabetes Prediction',
                                'Heart Disease Prediction',
                                'Parkinsons Prediction',
                                'Corona Prediction',
                                'Brain Tumor Prediction','Logout'],
                            menu_icon='hospital-fill',
                            icons=['bar-chart-line','activity', 'heart', 'eye', 'virus', 'emoji-dizzy',''],
                            default_index=0)

    # Safe conversion function to handle empty or invalid values
    def safe_convert_to_float(value):
        try:
            return float(value) if value.strip() else None  
        except ValueError:
            return None 
        
    if selected == 'Logout':
        st.session_state.clear()
        loading_message = st.empty()
        loading_message.success("Sure Want to Logout....")
        time.sleep(3)
        loading_message.success("Once Again Click Logout Button")
        st.stop()

    # Dashboard Page
    if selected == 'Dashboard':
        image_width = 600
        image_height = 400
        def resize_image(image_path, width, height):
            if os.path.exists(image_path):
                img = Image.open(image_path)
                img = img.resize((width, height))
                return img
            else:
                return None
        st.title('Insights Dashboard')
        # COVID-19 Visualizations
        st.header("COVID-19 Insights")
        col1, col2 = st.columns(2)
        with col1:
            covid_image_path = 'visualizations/corona1.png'
            if os.path.exists(covid_image_path):
                covid_image = resize_image(covid_image_path, image_width, image_height)
                st.image(covid_image, caption='COVID-19 Cases Over Time', use_container_width=True)
            else:
                st.warning('COVID-19 visualization not found.')

        with col2:
            covid_deaths_image_path = 'visualizations/covid2.png'
            if os.path.exists(covid_deaths_image_path):
                covid_deaths_image = resize_image(covid_deaths_image_path, image_width, image_height)
                st.image(covid_deaths_image, caption='Common Symptoms in COVID Positive Cases', use_container_width=True)
            else:
                st.warning('COVID-19 deaths visualization not found.')
        st.info("The insights shows that COVID-19 positive cases made up 39.8% of tests, with the most common symptoms being cough, sore throat, chest pain, loss of taste, and fever.")

        # Brain Tumor Visualizations
        st.header("Brain Tumor Insights")
        col3, col4 = st.columns(2)
        with col3:
            brain_image_path = 'visualizations/brain1.png'
            if os.path.exists(brain_image_path):
                brain_image = resize_image(brain_image_path, image_width, image_height)
                st.image(brain_image, caption='Brain Tumor Type Distribution', use_container_width=True)
            else:
                st.warning('Brain Tumor visualization not found.')

        with col4:
            brain_tumor_size_image_path = 'visualizations/brain3.png'
            if os.path.exists(brain_tumor_size_image_path):
               brain_tumor_size_image = resize_image(brain_tumor_size_image_path, image_width, image_height)
               st.image(brain_tumor_size_image, caption='Brain Tumor Size Distribution',use_container_width=True)
            else:
                st.warning('Brain Tumor Size visualization not found.')

        st.info("Brain tumor patient outcomes were nearly evenly split between deceased, complications, and recovered, with the accompanying box plot showing the distribution of tumor sizes across those three groups.")
        # Diabetes Visualizations
        st.header("Diabetes Insights")
        col5, col6 = st.columns(2)
        with col5:
            diabetes_image_path = 'visualizations/diabetes1.png'
            if os.path.exists(diabetes_image_path):
                diabetes_image = resize_image(diabetes_image_path, image_width, image_height)
                st.image(diabetes_image, caption='Age Distribution of Diabetic Patients', use_container_width=True)
            else:
                st.warning('Diabetes visualization not found.')

        with col6:
            diabetes_bmi_image_path = 'visualizations/diabetes2.png'
            if os.path.exists(diabetes_bmi_image_path):
                diabetes_bmi_image = resize_image(diabetes_bmi_image_path, image_width, image_height)
                st.image(diabetes_bmi_image, caption='Diabetes Cases Over Time', use_container_width=True)
            else:
                st.warning('Diabetes BMI visualization not found.')

        st.info("This insights shows the age distribution of diabetic patients with a peak around the 50s, and a diabetes prevalence rate where 34.9% of the observed group is diabetic while 65.1% is not.")
        # Parkinson's Disease Visualizations
        st.header("Parkinson's Disease Insights")
        col7, col8 = st.columns(2)
        with col7:
            parkinsons_age_image_path = 'visualizations/head1.png'
            if os.path.exists(parkinsons_age_image_path):
                parkinsons_age_image = resize_image(parkinsons_age_image_path, image_width, image_height)
                st.image(parkinsons_age_image, caption="Parkinson's Cases Over Time", use_container_width=True)
            else:
                st.warning("Parkinson's age distribution visualization not found.")

        with col8:
            parkinsons_speech_image_path = 'visualizations/head2.png'
            if os.path.exists(parkinsons_speech_image_path):
                parkinsons_speech_image = resize_image(parkinsons_speech_image_path, image_width, image_height)
                st.image(parkinsons_speech_image, caption="Mean Fundamental Frequency by Status", use_container_width=True)
            else:
                st.warning("Parkinson's speech analysis visualization not found.")
        st.info("This insights shows that Parkinson's disease affects 24.6% of the observed group, and those with the disease have a lower mean fundamental frequency of speech compared to healthy individuals.")
        # Heart Disease Visualizations
        st.header("Heart Disease Insights")
        col9, col10 = st.columns(2)
        with col9:
            heart_age_chol_image_path = 'visualizations/heart1.png'
            if os.path.exists(heart_age_chol_image_path):
                heart_age_chol_image = resize_image(heart_age_chol_image_path, image_width, image_height)
                st.image(heart_age_chol_image, caption='Heart Disease Cases Over Time', use_container_width=True)
            else:
                st.warning('Heart Disease Age vs Cholesterol visualization not found.')

        with col10:
            heart_blood_pressure_image_path = 'visualizations/heart2.png'
            if os.path.exists(heart_blood_pressure_image_path):
                heart_blood_pressure_image = resize_image(heart_blood_pressure_image_path, image_width, image_height)
                st.image(heart_blood_pressure_image, caption='Chest Pain Type Distribution', use_container_width=True)
            else:
                st.warning('Heart Disease Blood Pressure visualization not found.')
        st.info("This insights shows that 45.5% of the observed group has heart disease, and it explores the relationship between heart disease and chest pain type, suggesting a possible link between the two.")
    # Diabetes Prediction Page
    if selected == 'Diabetes Prediction':
        st.title('Diabetes Prediction using ML')
        col1, col2, col3 = st.columns(3)

        with col1:
            Pregnancies = st.text_input('Number of Pregnancies')

        with col2:
            Glucose = st.text_input('Glucose Level')

        with col3:
            BloodPressure = st.text_input('Blood Pressure value')

        with col1:
            SkinThickness = st.text_input('Skin Thickness value')

        with col2:
            Insulin = st.text_input('Insulin Level')

        with col3:
            BMI = st.text_input('BMI value')

        with col1:
            DiabetesPedigreeFunction = st.text_input('Diabetes Pedigree Function value')

        with col2:
            Age = st.text_input('Age of the Person')

        diab_diagnosis = ''
        if st.button('Diabetes Test Result'):
            user_input = [Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age]
            user_input = [safe_convert_to_float(x) for x in user_input]

            if None in user_input:
                st.error("Please fill all fields correctly with valid numbers.")
            else:
                diab_prediction = diabetes_model.predict([user_input])
                if diab_prediction[0] == 1:
                    diab_diagnosis = 'The person is diabetic'
                else:
                    diab_diagnosis = 'The person is not diabetic'
                st.success(diab_diagnosis)

    # Heart Disease Prediction Page
    if selected == 'Heart Disease Prediction':
       
        st.title('Heart Disease Prediction using ML')
        col1, col2, col3 = st.columns(3)
        with col1:
            age = st.text_input('Age')
        with col2:
            sex = st.text_input('Sex(Female-0 or Male-1)')
        with col3:
            cp = st.text_input('Chest Pain types')

        with col1:
            trestbps = st.text_input('Resting Blood Pressure')
        with col2:
            chol = st.text_input('Serum Cholestoral in mg/dl')
        with col3:
            fbs = st.text_input('Fasting Blood Sugar > 120 mg/dl')

        with col1:
            restecg = st.text_input('Resting Electrocardiographic results')
        with col2:
            thalach = st.text_input('Maximum Heart Rate achieved')
        with col3:
            exang = st.text_input('Exercise Induced Angina')

        with col1:
            oldpeak = st.text_input('ST depression induced by exercise')
        with col2:
            slope = st.text_input('Slope of the peak exercise ST segment')
        with col3:
            ca = st.text_input('Major vessels colored by flourosopy')

        with col1:
            thal = st.text_input('thal: 0 = normal; 1 = fixed defect; 2 = reversable defect')

        heart_diagnosis = ''
        if st.button('Heart Disease Test Result'):
            user_input = [age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]
            user_input = [safe_convert_to_float(x) for x in user_input]

            if None in user_input:
                st.error("Please fill all fields correctly with valid numbers.")
            else:
                heart_prediction = heart_disease_model.predict([user_input])
                if heart_prediction[0] == 1:
                    heart_diagnosis = 'The person is having heart disease'
                else:
                    heart_diagnosis = 'The person does not have any heart disease'
                st.success(heart_diagnosis)

    # Parkinson's Prediction Page
    if selected == "Parkinsons Prediction":
       
        # page title
        st.title("Parkinson's Disease Prediction using ML")

        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            fo = st.text_input('MDVP:Fo(Hz)')

        with col2:
            fhi = st.text_input('MDVP:Fhi(Hz)')

        with col3:
            flo = st.text_input('MDVP:Flo(Hz)')

        with col4:
            Jitter_percent = st.text_input('MDVP:Jitter(%)')

        with col5:
            Jitter_Abs = st.text_input('MDVP:Jitter(Abs)')

        with col1:
            RAP = st.text_input('MDVP:RAP')

        with col2:
            PPQ = st.text_input('MDVP:PPQ')

        with col3:
            DDP = st.text_input('Jitter:DDP')

        with col4:
            Shimmer = st.text_input('MDVP:Shimmer')

        with col5:
            Shimmer_dB = st.text_input('MDVP:Shimmer(dB)')

        with col1:
            APQ3 = st.text_input('Shimmer:APQ3')

        with col2:
            APQ5 = st.text_input('Shimmer:APQ5')

        with col3:
            APQ = st.text_input('MDVP:APQ')

        with col4:
            DDA = st.text_input('Shimmer:DDA')

        with col5:
            NHR = st.text_input('NHR')

        with col1:
            HNR = st.text_input('HNR')

        with col2:
            RPDE = st.text_input('RPDE')

        with col3:
            DFA = st.text_input('DFA')

        with col4:
            spread1 = st.text_input('spread1')

        with col5:
            spread2 = st.text_input('spread2')

        with col1:
            D2 = st.text_input('D2')

        with col2:
            PPE = st.text_input('PPE')

        # code for Prediction
        parkinsons_diagnosis = ''

        # creating a button for Prediction    
        if st.button("Parkinson's Test Result"):

            user_input = [fo, fhi, flo, Jitter_percent, Jitter_Abs,
                        RAP, PPQ, DDP,Shimmer, Shimmer_dB, APQ3, APQ5,
                        APQ, DDA, NHR, HNR, RPDE, DFA, spread1, spread2, D2, PPE]

            user_input = [float(x) for x in user_input]

            parkinsons_prediction = parkinsons_model.predict([user_input])

            if parkinsons_prediction[0] == 1:
                parkinsons_diagnosis = "The person has Parkinson's disease"
            else:
                parkinsons_diagnosis = "The person does not have Parkinson's disease"

        st.success(parkinsons_diagnosis)



    # Corona Prediction Page
    if selected == "Corona Prediction":
     
        st.title("Corona Virus Prediction using ML")
        col1, col2 = st.columns(2)

        with col1:
            age = st.text_input('Age')
            gender = st.text_input('Gender (Female-0 or Male-1)')
            fever = st.text_input('Fever')
            cough = st.text_input('Cough ( Yes-1 or No-0)')
            sore_throat = st.text_input('Sore Throat ( Yes-1 or No-0)')
            chest_pain = st.text_input('Chest Pain ( Yes-1 or No-0)')

        with col2:
            oxygen_level = st.text_input('Oxygen Level (%)')
            taste_loss = st.text_input('Taste Loss ( Yes-1 or No-0)')
            fatigue_level = st.text_input('Fatigue Level (Low-0, Moderate-1 or Severe-2)')
            diabetes = st.text_input('Diabetes ( Yes-1 or No-0)')
            hypertension = st.text_input('Hypertension ( Yes-1 or No-0)')
            asthma = st.text_input('Asthma ( Yes-1 or No-0)')
            immunocompromised = st.text_input('Immunocompromised ( Yes-1 or No-0)')
            cardiovascular_disease = st.text_input('Cardiovascular Disease ( Yes-1 or No-0)')

        corona_diagnosis = ''
        if st.button("Corona Test Result"):
            user_input = [age, gender, fever, cough, sore_throat, chest_pain, oxygen_level, taste_loss, fatigue_level,
                        diabetes, hypertension, asthma, immunocompromised, cardiovascular_disease]
            
            # Convert string fields to binary (Yes/No -> 1/0)
            user_input = [1 if x.strip().lower() == 'yes' else 0 if x.strip().lower() == 'no' else safe_convert_to_float(x) for x in user_input]

            if None in user_input:
                st.error("Please fill all fields correctly with valid numbers.")
            else:
                corona_prediction = corona_model.predict([user_input])
                if corona_prediction[0] == 1:
                    corona_diagnosis = 'The person is infected with Corona'
                else:
                    corona_diagnosis = 'The person is not infected with Corona'

                st.success(corona_diagnosis)



    # Brain Tumor Prediction Page
    if selected == "Brain Tumor Prediction":
       
        st.title("Brain Tumor Prediction using ML")
        col1, col2, col3 = st.columns(3)

        with col1:
            age = st.text_input('Age')
            gender = st.text_input('Gender (Female-0 or Male-1)')
            tumor_type = st.text_input('Tumor Type (Benign-0 Malignant-1 Malig-2)')
            tumor_size = st.text_input('Tumor Size (cm)')

        with col2:
            tumor_location = st.text_input('Tumor Location (Parietal-2  Occipital-1  Temporal-3  Frontal-0)')
            mri_findings = st.text_input('MRI Findings (Clear-0  or Present-1)')
            wbc_count = st.text_input('WBC Count (x10^3/uL)')
            lymphocyte_percent = st.text_input('Lymphocyte (%)')

        with col3:
            pcr_test = st.text_input('PCR Test (Positive-1 Negative-0)')
            covid_severity = st.text_input('COVID Severity (Moderate-1, Mild-0 or Severe-2)')
            oxygen_sat = st.text_input('Oxygen Sat (%)')
            symptoms_headache = st.text_input('Symptoms (Headache) (Yes/No)')
            symptoms_seizures = st.text_input('Symptoms (Seizures) (Yes/No)')
            treatment_type = st.text_input('Treatment Type')

        brain_tumor_diagnosis = ''
        if st.button("Brain Tumor Test Result"):
            user_input = [age, gender, tumor_type, tumor_size, tumor_location, mri_findings, wbc_count,
                        lymphocyte_percent, pcr_test, covid_severity, oxygen_sat, symptoms_headache, symptoms_seizures,
                        treatment_type]
            
            # Convert inputs to float or None for invalid inputs
            user_input = [safe_convert_to_float(x) if isinstance(x, str) and x.replace('.', '', 1).isdigit() else None for x in user_input]

            # Check for any None values (empty or invalid inputs)
            if None in user_input:
                st.error("Please fill all fields correctly with valid numbers.")
            else:
                brain_tumor_prediction = brain_tumor_model.predict([user_input])
                if brain_tumor_prediction[0] == 1:
                    brain_tumor_diagnosis = 'The person has a Brain Tumor'
                else:
                    brain_tumor_diagnosis = 'The person does not have a Brain Tumor'

                st.success(brain_tumor_diagnosis)
else:
    st.markdown("<h2 style='text-align: center;'>DiagnoMate</h2>", unsafe_allow_html=True)
    
    option = st.select_slider(
        "Choose Option",
        options=["Login", "Register"],
        value="Login",
        label_visibility="collapsed"
    )

    # Display the appropriate form
    if option == "Login":
        login()
    else:
        registration()
