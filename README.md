**MediBuddy Assistant**
MediBuddy Assistant is a Streamlit-based application designed to predict the likelihood of a user having diabetes, heart disease, or Parkinson's disease using pre-trained machine learning models. This tool leverages multiple machine learning models to analyze user inputs and provide predictive insights into various health conditions.

**Features**
Diabetes Prediction: Predicts the likelihood of diabetes based on user input.
Heart Disease Prediction: Predicts the likelihood of heart disease based on user input.
Parkinson's Disease Prediction: Predicts the likelihood of Parkinson's disease based on user input.
Interactive User Interface: Easy-to-use interface with sidebar navigation and input forms for each disease prediction.

**Installation**
1. Clone the repository:
     git clone https://github.com/your_username/MediBuddy-Assistant.git
      cd MediBuddy-Assistant
2. Install the required packages:
   pip install -r requirements.txt
3. Download and place the pre-trained models:

Ensure you have the trained models (diabetes_model.sav, heart_disease_model.sav, parkinsons_model.sav) in the saved_models directory.
Running the Application
**To run the Streamlit application, use the following command:
**
**streamlit run main.py**

This will start the application, and you can access it via your web browser at http://localhost:8501.

**Project Structure**
main.py: The main script to run the Streamlit application.
saved_models: Directory containing the pre-trained models.
requirements.txt: List of required Python packages.

**Usage**

**Navigate to the prediction page:**

Use the sidebar to select the type of prediction (Diabetes, Heart Disease, Parkinson's).

**Enter the required input values:**

Fill in the input fields with the relevant medical data.

**Get the prediction:**
Click the prediction button to get the result.
The result will be displayed below the button, indicating whether the person is likely to have the disease.
