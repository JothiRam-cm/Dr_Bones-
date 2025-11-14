# 🦴 **Bone Guard – AI-Powered Osteoporosis Detection App**

Early Detection • AI Diagnosis • Medical Report Generation

Bone Guard is an AI-driven healthcare application designed to **detect osteoporosis from X-ray images** using deep learning (MobileNet) and provide real-time insights into bone health.
The system offers a **fast, cost-effective, radiation-free alternative** to traditional DEXA scans and generates **downloadable medical reports** for clinicians and patients.

---

## 🚀 **Features**

### 🔬 **AI-Based Osteoporosis Detection**

* Uses **MobileNet** deep learning architecture
* 94.5% accuracy on X-ray image classification
* Identifies early-stage osteoporosis faster than traditional methods

### 📱 **Streamlit Web Application**

* Upload X-ray images for instant diagnosis
* Clean, user-friendly interface
* Download diagnosis in **PDF report format**

### ⌚ **(Optional Extension)** Real-Time Bone Health Monitoring

* Wearable vibrational sensors to track bone strength
* Continuous monitoring + AI insights

### 📊 **Data Visualization**

* Model accuracy graphs
* Predicted class distribution
* Bone density trend interpretations

---

## 🏗️ **Tech Stack**

| Component           | Technology                     |
| ------------------- | ------------------------------ |
| AI Model            | TensorFlow / Keras (MobileNet) |
| Image Processing    | OpenCV, NumPy                  |
| Web App             | Streamlit                      |
| Backend APIs        | FastAPI / Flask                |
| Database            | SQLite / Cloud Firestore       |
| Report Generation   | Python FPDF                    |
| Version Control     | Git + GitHub                   |
| Optional IoT Module | Wearable vibrational sensors   |

---

## 📂 **Project Folder Structure**

```
Osteo-Finder/
│── app.py                # Streamlit interface
│── models/               # MobileNet model (LFS tracked)
│── utils/                # Helper scripts
│── reports/              # Generated PDF reports
│── data/                 # Datasets (optional)
│── requirements.txt      # Dependencies
│── README.md             # Project documentation
```

---

## 🛠️ **Installation & Setup**

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/Osteo-Finder.git
cd Osteo-Finder
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ (Important) Install Git LFS

If you're downloading model files:

```bash
git lfs install
git lfs pull
```

### 4️⃣ Run App Locally

```bash
streamlit run app.py
```

---

## 🧠 **How It Works**

1. **Upload X-ray image**
2. Image is resized, normalized, and fed into the MobileNet model
3. AI predicts osteoporosis / normal bone
4. The system generates:

   * Diagnosis
   * Confidence score
   * Medical PDF report
5. (If sensors enabled) Real-time bone vibration data is added

---

## 📜 **Model Accuracy**

* **Accuracy:** 94.5%
* **Architecture:** MobileNet (Transfer Learning)
* **Dataset:** X-ray bone images
* **Validation:** Confusion matrix, classification report

---

## 📄 **PDF Report Includes**

✔ Patient details
✔ Uploaded X-ray image
✔ AI prediction & confidence
✔ Notes for clinicians
✔ Preventive recommendations

---

## 📌 **Use Cases**

* Hospitals & clinics
* Rural health camps
* Telemedicine platforms
* Personal health monitoring
* Research in AI for Medical Imaging

---

## 📈 **Future Enhancements**

* Integrate vibrational IoT bone sensors
* Add fracture risk prediction
* Deploy on cloud (AWS / GCP)
* Expand dataset for multi-bone predictions

---

## 👨‍💻 **Contributors**

* **C.M. Jothi Ram**
* K.S. Gajendran
* Thiruvishva K
* Gopika R
* Nandavarma T
* Abinaya J

---

## 📚 **References**

Research papers on AI diagnosis, MobileNet, wearable sensors, and osteoporotic fracture detection.
(Complete list available in the project report.)

---

## ⭐ **Support**

If you like this project, consider giving the repository a **star ⭐** to support the work.
