import streamlit as st
import requests
import time

# We will connect to the API hosted on the FastAPI server through a frontend created using Streamlit.  

# User Flow:  
# 1. The user uploads a file via the UI.  
# 2. The file is sent using a **POST** request to the '/scan-file/' endpoint.  
# 3. The resulting 'file_id' is captured.  
# 4. The 'file_id' is passed in a **GET** request.  
# 5. The scan result is displayed on the UI. 

FASTAPI_URL = "http://127.0.0.1:8000"

st.title("PDF Malware Scanner 🛡️")

uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

# Store file_id from FastAPI response
file_id = None

if uploaded_file:
    with st.spinner("Uploading file and scanning..."):
        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
        response = requests.post(f"{FASTAPI_URL}/scan-file/", files=files)

        if response.status_code == 200:
            file_id = response.json().get("file_id")
            st.success("File uploaded successfully! Click 'Get Scan Result' to check.")
            # print(file_id)
        else:
            st.error("Error scanning file! Please try again.")

# Button to fetch scan results
if file_id and st.button("Get Scan Result"):
    with st.spinner("Fetching scan results..."):

        # Loop to make sure scan is carried out only for select few services mentioned inside GET request

        while True:
            result_response = requests.get(f"{FASTAPI_URL}/get-result/{file_id}")
            
            if result_response.status_code == 200:
                result_data = result_response.json()
                is_safe = result_data["safe"]
                scan_stats = result_data["stats"]
                detailed_results = result_data["detailed_results"]

                st.write("### Scan Summary")
                st.write(scan_stats)

                st.write("### Safe Engines Analysis")
                for engine, category in detailed_results.items():
                    st.write(f"**{engine}:** {category}")

                if is_safe:
                    st.success("✅ The file is safe!")
                else:
                    st.error("🚨 The file might be infected!")

                break
            time.sleep(3)
