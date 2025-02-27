from fastapi import FastAPI, File, UploadFile, HTTPException
import requests
import time
import shutil
import os

'''
Using FastAPI to Host Our APIs  
VirusTotal allows users to upload files to their cloud using [https://www.virustotal.com/api/v3/files](https://www.virustotal.com/api/v3/files)  
and fetch the results using [https://www.virustotal.com/api/v3/analyses/{file_id}](https://www.virustotal.com/api/v3/analyses/{file_id}),  
where `file_id` is generated when a file is uploaded to the `/api/v3/files` endpoint.  

Let's create two endpoints in FastAPI:  
- 1 **POST** endpoint for uploading a file.  
- 2 **GET** endpoint for retrieving the results.  
'''


app = FastAPI()

VIRUSTOTAL_API_KEY = "" # add your virus total api key here

# For quicker results, only scan the document using a select few antiviruses,  
# since VirusTotal has over 70 scanners.  
# However, it is recommended to use all scanners in production rather than just a select few.  

SAFE_ENGINES = ["Microsoft", "Bitdefender", "Kaspersky", "McAfee", "Sophos"]


# Helper function

async def scan_file_for_virus(file_path: str):
    """Uploads the file to VirusTotal and returns the scan ID (file_id)."""
    
    url = "https://www.virustotal.com/api/v3/files"
    headers = {"x-apikey": VIRUSTOTAL_API_KEY}

    with open(file_path, "rb") as file:
        files = {"file": file}
        response = requests.post(url, headers=headers, files=files)

    if response.status_code != 200:
        return {"error": f"Error scanning file: {response.text}"}

    scan_result = response.json()
    file_id = scan_result.get("data", {}).get("id")

    if not file_id:
        return {"error": "Failed to retrieve file scan ID"}

    return {"file_id": file_id}

@app.get("/get-result/{file_id}")
async def get_result(file_id: str):
    """Fetch scan results from VirusTotal using file_id."""
    
    analysis_url = f"https://www.virustotal.com/api/v3/analyses/{file_id}"
    headers = {"x-apikey": VIRUSTOTAL_API_KEY}

    while True:
        result_response = requests.get(analysis_url, headers=headers)
        result_json = result_response.json()
        attributes = result_json.get("data", {}).get("attributes", {})
        status = attributes.get("status", "")

        if status == "completed":
            scan_stats = attributes["stats"]
            scan_results = attributes["results"]

            # Extract results for selected antivirus engines
            detailed_results = {
                engine: scan_results[engine]["category"] for engine in SAFE_ENGINES if engine in scan_results
            }

            # Determine if the file is safe
            # Note: considering "timeout" value for the sake of this blog, not recommended in production
            is_safe = all(value == "undetected" or value == "timeout" for value in detailed_results.values())

            return {
                "safe": is_safe,
                "stats": scan_stats,
                "detailed_results": detailed_results
            }

        time.sleep(3)  # Wait before retrying

@app.post("/scan-file/")
async def scan_file(file: UploadFile = File(...)):
    """Uploads a file, scans it, and returns the file_id to check later."""
    
    # Save uploaded file temporarily (use any DB services for production)
    temp_filename = f"temp_{file.filename}"
    
    with open(temp_filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    scan_result = await scan_file_for_virus(temp_filename)

    if "error" in scan_result:
        raise HTTPException(status_code=500, detail=scan_result["error"])

    return {"message": "File uploaded successfully!", "file_id": scan_result["file_id"]}
