# **File Scanner with FastAPI, Streamlit, and VirusTotal API**  

![blog 4 gif](https://github.com/user-attachments/assets/21060cbd-734e-4eec-a858-df8f8f5ae987)

## **Overview** 
This project demonstrates how to build a **file scanning service** using **FastAPI**, **Streamlit**, and **VirusTotal’s API**. 
The backend handles **file uploads and scan requests**, while the frontend provides a simple UI for users to upload files and view scan results.  

## **Features**  
- Upload a **PDF file** via the UI.  
- Scan the file using **VirusTotal's API**.  
- Retrieve and display scan results in real-time.  
- Uses a subset of antivirus engines for demonstration purposes.  

## **Tech Stack**  
- **Backend**: FastAPI  
- **Frontend**: Streamlit  
- **API Integration**: VirusTotal API  
- **Environment Management**: Python & Virtual Environment  

## **Project Setup**  

### **1. Clone the Repository**  
```bash
git clone https://github.com/your-username/repository-name.git
cd repository-name
```

### **2. Create a Virtual Environment**  
```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate     # On Windows
```

### **3. Install Dependencies**  
```bash
pip install streamlit fastapi uvicorn requests
```

### **4. Set Up Environment Variables**  
```bash
VIRUSTOTAL_API_KEY=your_api_key_here
```

### **5. Start the FastAPI Backend**  
```bash
uvicorn backend.app:app --reload
```

### **6. Start the Streamlit Frontend**  
```bash
streamlit run app.py
```

## **Usage**  
- Open the Streamlit UI in your browser.
- Upload a PDF file for scanning.  
- Click "Scan File" to submit the file to the FastAPI backend.
- Click "Get Scan Result" to retrieve the results.

## Contributing
Feel free to fork this repository, submit issues, or contribute enhancements via pull requests.

## License
This project is open-source and available under the MIT License.



