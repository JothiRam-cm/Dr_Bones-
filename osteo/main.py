import streamlit as st
import numpy as np
import cv2
import tensorflow as tf
from fpdf import FPDF
import tempfile
from pathlib import Path

# Resolve project base directory (two levels up from this file -> DrBones)
BASE_DIR = Path(__file__).resolve().parents[2]

# Prefer the model shipped inside `DrBones_app/models`, fall back to top-level `models`
MODEL_PATH = '/mount/src/dr_bones-/osteo/models/DrBones.h5'


# Load the trained MobileNet model using a relative path
model = tf.keras.models.load_model(str(MODEL_PATH))


# Function to preprocess the image for prediction
def preprocess_image(image):
    image = cv2.resize(image, (224, 224))
    image = image.astype(np.float32) / 255.0
    image = np.expand_dims(image, axis=0)
    return image


# Function to predict the result using the model
def predict(image):
    processed_image = preprocess_image(image)
    predictions = model.predict(processed_image)
    return np.argmax(predictions, axis=1)


# Function to calculate BMI
def calculate_bmi(weight, height):
    if height > 0:
        bmi = weight / (height ** 2)
        return round(bmi, 2)
    else:
        return None


# Function to interpret BMI
def interpret_bmi(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 24.9:
        return "Normal weight"
    elif 25 <= bmi < 29.9:
        return "Overweight"
    else:
        return "Obesity"


# Function to create a PDF report
def create_pdf_report(name, gender, age, joint_pain, menopause_age, height, weight, bmi, bmi_category, smoker, alcoholic, diabetic, hypothyroidism, pregnancies, seizures, estrogen_use, occupation, fracture_history, dialysis, osteoporosis_family_history, walking_distance, eating_habits, medical_history, prediction):
    pdf = FPDF()
    pdf.add_page()

    # Title
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(200, 10, "Bone Health Report", ln=True, align="C")

    # Patient Information Table
    pdf.set_font("Arial", '', 10)
    pdf.ln(10)
    
    # Table header
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(80, 10, "Field", border=1)
    pdf.cell(100, 10, "Details", border=1)
    pdf.ln()

    # Table content
    pdf.set_font("Arial", '', 10)
    details = [
        ("Name", name),
        ("Gender", gender),
        ("Age", age),
        ("Menopause Age", menopause_age),
        ("Joint Pain", joint_pain),
        ("Height (meters)", height),
        ("Weight (KG)", weight),
        ("BMI", bmi),
        ("BMI Category", bmi_category),
        ("Smoker", smoker),
        ("Alcoholic", alcoholic),
        ("Diabetic", diabetic),
        ("Hypothyroidism", hypothyroidism),
        ("Number of Pregnancies", pregnancies),
        ("Seizure Disorder", seizures),
        ("Estrogen Use", estrogen_use),
        ("Occupation", occupation),
        ("History of Fracture", fracture_history),
        ("Dialysis", dialysis),
        ("Family History of Osteoporosis", osteoporosis_family_history),
        ("Maximum Walking Distance (km)", walking_distance),
        ("Daily Eating Habits", eating_habits),
        ("Medical History", medical_history),
    ]

    for field, value in details:
        pdf.cell(80, 10, field, border=1)
        pdf.cell(100, 10, str(value), border=1)
        pdf.ln()

    # Prediction result
    pdf.cell(80, 10, "Prediction", border=1)
    pdf.cell(100, 10, 'Osteoporosis' if prediction == 1 else 'No Osteoporosis', border=1)
    pdf.ln()

    # Save the PDF
    pdf_output_path = 'Bone_Health_Report.pdf'
    pdf.output(pdf_output_path)

    return pdf_output_path


# Main function
def main():
    # Custom CSS for styling
    st.markdown("""
        <style>
            body {
                background-color: #FFFafb;
                color: #2B2C28;
            }
            .header {
                background-color: #131515;
                padding: 10px;
                color: #FFFafb;
                text-align: center;
            }
            .button {
                background-color: #339989;
                color: #FFFafb;
                padding: 10px 20px;
                border: None;
                cursor: pointer;
                border-radius: 5px;
            }
            .button:hover {
                background-color: #7DE2D1;
            }
            .footer {
                background-color: #131515;
                color: #FFFafb;
                text-align: center;
                padding: 10px;
                position: fixed;
                bottom: 0;
                width: 100%;
            }
        </style>
    """, unsafe_allow_html=True)

    # Sidebar for navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Select a page", ("Landing Page", "Upload Data", "Processing", "Results", "View Reports", "Help/FAQ"))

    if page == "Landing Page":
        st.title("Bone Health Detection By Dr.Bones")
        # Set the image path for the logo (use project-relative paths)
        logo_url = '/mount/src/dr_bones-/osteo/Asserts/bone-logo.png'
        image_url = '/mount/src/dr_bones-/osteo/Asserts/health-quotes.jpg'
        st.logo(logo_url, link=None, icon_image=logo_url)
        st.image(image_url, width=670)
        st.write("Welcome to the Bone Health Detection app. Please navigate to the Upload Data page to begin.")
    
    elif page == "Upload Data":
        st.header("Upload Patient Data")
        # Patient Details Input
        name = st.text_input("Name")
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        age = st.number_input("Age", min_value=0, max_value=120, step=1)
        menopause_age = st.number_input("Menopause Age", min_value=0, max_value=120, step=1)
        joint_pain = st.selectbox("Joint Pain", ["Yes", "No"])
        height = st.number_input("Height (meters)", min_value=0.0, step=0.01)
        weight = st.number_input("Weight (KG)", min_value=0.0, step=0.1)
        smoker = st.selectbox("Smoker", ["Yes", "No"])
        alcoholic = st.selectbox("Alcoholic", ["Yes", "No"])
        diabetic = st.selectbox("Diabetic", ["Yes", "No"])
        hypothyroidism = st.selectbox("Hypothyroidism", ["Yes", "No"])
        pregnancies = st.number_input("Number of Pregnancies", min_value=0, max_value=20, step=1)
        seizures = st.selectbox("Seizure Disorder", ["Yes", "No"])
        estrogen_use = st.selectbox("Estrogen Use", ["Yes", "No"])
        occupation = st.text_input("Occupation")
        fracture_history = st.selectbox("History of Fracture", ["Yes", "No"])
        dialysis = st.selectbox("Dialysis", ["Yes", "No"])
        osteoporosis_family_history = st.selectbox("Family History of Osteoporosis", ["Yes", "No"])
        walking_distance = st.number_input("Maximum Walking Distance (km)", min_value=0.0, step=0.1)
        eating_habits = st.text_input("Daily Eating Habits")
        medical_history = st.text_input("Medical History")

        # File upload for X-ray image
        uploaded_file = st.file_uploader("Upload an X-ray Image", type=["jpg", "jpeg", "png"])

        if st.button("Next to Processing"):
            st.session_state.name = name
            st.session_state.gender = gender
            st.session_state.age = age
            st.session_state.menopause_age = menopause_age
            st.session_state.joint_pain = joint_pain
            st.session_state.height = height
            st.session_state.weight = weight
            st.session_state.smoker = smoker
            st.session_state.alcoholic = alcoholic
            st.session_state.diabetic = diabetic
            st.session_state.hypothyroidism = hypothyroidism
            st.session_state.pregnancies = pregnancies
            st.session_state.seizures = seizures
            st.session_state.estrogen_use = estrogen_use
            st.session_state.occupation = occupation
            st.session_state.fracture_history = fracture_history
            st.session_state.dialysis = dialysis
            st.session_state.osteoporosis_family_history = osteoporosis_family_history
            st.session_state.walking_distance = walking_distance
            st.session_state.eating_habits = eating_habits
            st.session_state.medical_history = medical_history
            st.session_state.uploaded_file = uploaded_file
            
            st.success("Data saved! Proceeding to Processing page...")

    elif page == "Processing":
        st.header("Processing Data by Dr_Bones")
        if 'uploaded_file' in st.session_state and st.session_state.uploaded_file is not None:
            # Reset the file pointer to the beginning of the uploaded file
            st.session_state.uploaded_file.seek(0)

            # Load and preprocess image for prediction
            file_bytes = np.asarray(bytearray(st.session_state.uploaded_file.read()), dtype=np.uint8)
            image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

            if image is not None:
                st.image(image, caption='Uploaded X-ray Image', use_column_width=True)

                if st.button("Predict"):
                    prediction = predict(image)

                    # Calculate BMI
                    bmi = calculate_bmi(st.session_state.weight, st.session_state.height)
                    bmi_category = interpret_bmi(bmi) if bmi else "N/A"

                    st.session_state.bmi = bmi
                    st.session_state.bmi_category = bmi_category
                    st.session_state.prediction = prediction

                    st.success("Prediction completed! Proceeding to Results page...")
            else:
                st.error("Error loading image. Please upload a valid image file.")

        else:
            st.warning("Please upload an image on the Upload Data page before proceeding.")

    elif page == "Results":
        st.header("Prediction Results by Dr_Bones")
        if 'prediction' in st.session_state:
            st.write("## Prediction Result:")
            st.write('Osteoporosis' if st.session_state.prediction == 1 else 'No Osteoporosis')
            st.write(f"### BMI: {st.session_state.bmi} ({st.session_state.bmi_category})")

            # Create and display PDF report
            if st.button("Generate PDF Report"):
                pdf_path = create_pdf_report(
                    st.session_state.name,
                    st.session_state.gender,
                    st.session_state.age,
                    st.session_state.joint_pain,
                    st.session_state.menopause_age,
                    st.session_state.height,
                    st.session_state.weight,
                    st.session_state.bmi,
                    st.session_state.bmi_category,
                    st.session_state.smoker,
                    st.session_state.alcoholic,
                    st.session_state.diabetic,
                    st.session_state.hypothyroidism,
                    st.session_state.pregnancies,
                    st.session_state.seizures,
                    st.session_state.estrogen_use,
                    st.session_state.occupation,
                    st.session_state.fracture_history,
                    st.session_state.dialysis,
                    st.session_state.osteoporosis_family_history,
                    st.session_state.walking_distance,
                    st.session_state.eating_habits,
                    st.session_state.medical_history,
                    st.session_state.prediction
                )
                with open(pdf_path, "rb") as pdf_file:
                    st.download_button("Download PDF Report", pdf_file, "Bone_Health_Report.pdf")
        else:
            st.warning("Please complete the prediction first.")

    elif page == "View Reports":
        st.header("View Past Reports by Dr_Bones")
        st.write("Feature coming soon!")

    elif page == "Help/FAQ":
        st.header("Help and FAQ")
        
        # Help Topics
        st.header("Help Topics")

        help1 = """
        **1. Getting Started**  
        - Overview of the app features  
        - Instructions on how to navigate through the app
        """

        help2 = """
        **2. Data Entry Guidelines**  
        - Detailed explanation of each input field  
        - Tips for providing accurate data
        """

        help3 = """
        **3. Uploading Images**  
        - Accepted file formats and size limits  
        - Best practices for uploading clear and relevant images
        """

        help4 = """
        **4. Interpreting Results**  
        - How to understand the analysis and output provided by the app  
        - Common terminologies and what they mean
        """

        help5 = """
        **5. Technical Support**  
        - Troubleshooting common issues  
        - Contact information for further assistance
        """

        help6 = """
        **6. Feedback and Suggestions**  
        - How users can provide feedback to improve the app  
        - Encouraging users to report bugs or suggest new features
        """

        st.markdown(help1)
        st.markdown(help2)
        st.markdown(help3)
        st.markdown(help4)
        st.markdown(help5)
        st.markdown(help6)

        # Frequently Asked Questions
        st.header("Frequently Asked Questions (FAQs)")

        faq1 = """
        **1. What is the Bone Health Detection app?**  
        The Bone Health Detection app uses machine learning algorithms to assess your bone health based on the symptoms and lifestyle factors you provide. It aims to help users detect potential bone-related issues early.
        """

        faq2 = """
        **2. How do I use the app?**  
        To use the app:
        - Navigate to the Upload Data page.
        - Enter your patient details in the provided fields.
        - Upload a photo for analysis (if applicable).
        - Click on Submit to process your data and receive results.
        """

        faq3 = """
        **3. What type of data do I need to provide?**  
        You will need to provide details such as:
        - Joint Pain
        - Gender
        - Smoking and Alcohol consumption status
        - Diabetes and Hypothyroidism history
        - Family history of osteoporosis
        - Daily eating habits
        - Any other relevant health information.
        """

        faq4 = """
        **4. What should I do if I encounter an error while uploading data?**  
        - Ensure that all required fields are filled out correctly.
        - Check that the uploaded file is in an accepted format (e.g., JPEG, PNG).
        - If the problem persists, refresh the page or try again later.
        """

        faq5 = """
        **5. How long does it take to get results?**  
        The processing time typically ranges from a few seconds to a couple of minutes, depending on the complexity of the analysis and server load.
        """

        faq6 = """
        **6. Can I save my results?**  
        Yes! Once you receive your results, you can download them as a PDF report from the View Reports page.
        """

        faq7 = """
        **7. Is my data safe?**  
        We take data privacy seriously. Your personal information is stored securely and is not shared with third parties without your consent. Please refer to our Privacy Policy for more details.
        """

        faq8 = """
        **8. What should I do if I have questions about my results?**  
        For any medical inquiries or concerns regarding your results, please consult a qualified healthcare professional. This app is intended for informational purposes only and should not replace professional medical advice.
        """

        st.markdown(faq1)
        st.markdown(faq2)
        st.markdown(faq3)
        st.markdown(faq4)
        st.markdown(faq5)
        st.markdown(faq6)
        st.markdown(faq7)
        st.markdown(faq8)

    # Footer
    st.markdown("""
        <div class="footer">
            <p>© 2024 Dr.Bones. All rights reserved.</p>
        </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
