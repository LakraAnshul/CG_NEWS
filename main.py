from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import mysql.connector
from mysql.connector import Error
from typing import List
from datetime import datetime
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import base64
from fastapi import File, UploadFile, Form
from dateutil import parser as dateutil_parser
from typing import Optional
from services.ocr_processor import process_base64_images
from fastapi import FastAPI, Query, Request, HTTPException
from typing import Optional
import json
from fastapi import Request
from datetime import datetime, timedelta
import os

app = FastAPI()


# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# def get_connection():
#     try:
#         conn = mysql.connector.connect(
#             host="localhost",
#             user="root",
#             password="msql1234",
#             database="cgpolice"
#         )
#         return conn
#     except Error as e:
#         print("Error:", e)
#         return None


# class FIRRecord(BaseModel):
#     FIR_REG_NUM: float
#     STATE_CD: float
#     DISTRICT_CD: float
#     PS_CD: float
#     REG_DT: datetime
#     FIR_CONTENTS: Optional[str]




# @app.get("/fir-records", response_model=List[FIRRecord])
# def get_fir_records(
#     start_date: Optional[str] = Query(None, description="Start date in YYYY-MM-DD"),
#     end_date: Optional[str] = Query(None, description="End date in YYYY-MM-DD (optional if single date)"),
#     last_24_hours: Optional[bool] = Query(False, description="Fetch records from the past 24 hours")
# ):
#     try:
#         if last_24_hours:
#             start = datetime.now() - timedelta(days=1)
#             end = datetime.now()
#         elif start_date:
#             start = datetime.strptime(start_date, "%Y-%m-%d")
#             end = datetime.strptime(end_date, "%Y-%m-%d") if end_date else start
#         else:
#             raise HTTPException(status_code=400, detail="Provide either 'last_24_hours' or 'start_date'")
#     except ValueError:
#         raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")

#     conn = get_connection()
#     if not conn:
#         raise HTTPException(status_code=500, detail="Database connection failed")

#     cursor = conn.cursor(dictionary=True)
#     query = """
#         SELECT FIR_REG_NUM, STATE_CD, DISTRICT_CD, PS_CD, REG_DT, FIR_CONTENTS
#         FROM t_fir_registration
#         WHERE REG_DT BETWEEN %s AND %s
#     """
#     cursor.execute(query, (start, end))
#     records = cursor.fetchall()

#     # ✅ Convert REG_DT to string for each record
#     for rec in records:
#         if isinstance(rec.get("REG_DT"), datetime):
#             rec["REG_DT"] = rec["REG_DT"].strftime("%Y-%m-%d %H:%M:%S")

#     cursor.close()
#     conn.close()

#     return JSONResponse(content=records)



# @app.get("/getnews")
# def get_news(
#     start_date: Optional[str] = Query(None, description="Start date in YYYY-MM-DD format"),
#     end_date: Optional[str] = Query(None, description="End date in YYYY-MM-DD format (optional)"),
#     last_24_hours: Optional[bool] = Query(False, description="Set to true to fetch past 24 hours")
# ):
#     try:
#         if last_24_hours:
#             start = datetime.now() - timedelta(days=1)
#             end = datetime.now()
#         elif start_date:
#             start = datetime.strptime(start_date, "%Y-%m-%d")
#             if end_date:
#                 end = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1) - timedelta(seconds=1)
#             else:
#                 end = start + timedelta(days=1) - timedelta(seconds=1)
#         else:
#             raise HTTPException(status_code=400, detail="Provide either 'last_24_hours' or 'start_date'")
#     except ValueError:
#         raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")

#     conn = get_connection()
#     if not conn:
#         raise HTTPException(status_code=500, detail="DB connection failed")

#     cursor = conn.cursor()
#     query = """
#         SELECT UPLOAD_ID, LANG_CD, UPLOADED_FILE, RECORD_CREATED_ON
#         FROM t_news_upload
#         WHERE RECORD_CREATED_ON BETWEEN %s AND %s
#     """
#     cursor.execute(query, (start, end))
#     rows = cursor.fetchall()

#     result = []
#     for upload_id, lang_cd, image_blob, created_on in rows:
#         image_base64 = base64.b64encode(image_blob).decode('utf-8') if image_blob else None
#         result.append({
#             "upload_id": upload_id,
#             "language_code": lang_cd,
#             "image_base64": image_base64,
#             "created_on": str(created_on)
#         })

#     cursor.close()
#     conn.close()

#     return JSONResponse(content=result)





# @app.post("/uploadnews")
# async def upload_news_image(
#     file: UploadFile = File(...),
#     language: str = Form("Hindi")
# ):
#     try:
#         contents = await file.read()
#     except Exception:
#         raise HTTPException(status_code=400, detail="Could not read file")

#     conn = get_connection()
#     if not conn:
#         raise HTTPException(status_code=500, detail="Database connection failed")

#     try:
#         cursor = conn.cursor()
#         query = "INSERT INTO news_media (language, uploaded_image) VALUES (%s, %s)"
#         cursor.execute(query, (language, contents))
#         conn.commit()
#         cursor.close()
#         conn.close()
#         return JSONResponse(content={"status": "success", "message": "Image uploaded successfully"})
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))





# class SummaryData(BaseModel):
#     date: str
#     district: str
#     police_station: str
#     fir_number: str
#     complainant: str
#     accused: str
#     weapon: str
#     crime_type: str
#     score: int
#     crime_category: str
#     heading: str
#     summary: str



# def parse_date(date_str: str) -> Optional[datetime]:
#     if not date_str or date_str.strip().upper() in ("N/A", "NA", "NONE"):
#         return None

#     known_formats = [
#         "%d.%m.%y", "%d.%m.%Y", "%d/%m/%Y", "%Y-%m-%d",
#         "%d-%m-%Y", "%d %B %Y", "%d %b %Y"
#     ]

#     for fmt in known_formats:
#         try:
#             return datetime.strptime(date_str.strip(), fmt)
#         except ValueError:
#             continue

#     # Try smart fallback
#     try:
#         return dateutil_parser.parse(date_str.strip(), dayfirst=True)
#     except Exception:
#         return None




# from fastapi import HTTPException
# from datetime import datetime
# from fastapi import Request
# from fastapi.responses import JSONResponse

# @app.post("/savesummary")
# def save_summary(data: SummaryData):
#     parsed_date = parse_date(data.date)

#     conn = get_connection()
#     if not conn:
#         raise HTTPException(status_code=500, detail="Database connection failed")

#     insert_query = """
#         INSERT INTO summary_v2 (
#             DATE, DISTRICT_NAME, POLICE_STATION_NAME, FIR_NUMBER,
#             COMPLAINANT_NAME, ACCUSED_NAME, WEAPON, CRIME_TYPE,
#             NEWS_SCORE, CRIME_CATEGORY, NEWS_HEADING, NEWS_SUMMARY,
#             RECORD_CREATED_ON, RECORD_CREATED_BY,
#             RECORD_UPDATED_ON, RECORD_UPDATED_BY,
#             RECORD_SYNC_FROM, RECORD_SYNC_TO, RECORD_SYNC_ON,
#             RECORD_UPDATED_FROM, DUMMY_COLUMN_1, DUMMY_COLUMN_2
#         ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
#     """

#     now = datetime.now()

#     values = (
#         parsed_date,
#         data.district,
#         data.police_station,
#         data.fir_number,
#         data.complainant,
#         data.accused,
#         data.weapon,
#         data.crime_type,
#         data.score,
#         data.crime_category,
#         data.heading,
#         data.summary,
#         now,             # RECORD_CREATED_ON
#         "SYSTEM",        # RECORD_CREATED_BY
#         now,             # RECORD_UPDATED_ON
#         "SYSTEM",        # RECORD_UPDATED_BY
#         "OCR",           # RECORD_SYNC_FROM
#         "DB",            # RECORD_SYNC_TO
#         now,             # RECORD_SYNC_ON
#         "FE",            # RECORD_UPDATED_FROM
#         "",              # DUMMY_COLUMN_1
#         ""               # DUMMY_COLUMN_2
#     )

#     try:
#         cursor = conn.cursor()
#         cursor.execute(insert_query, values)
#         conn.commit()
#         cursor.close()
#         conn.close()
#         return {"status": "success", "message": "Summary saved successfully"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))




# @app.get("/police-station/name")
# def get_police_station_name(ps_cd: float, district_cd: float, state_cd: float):
#     conn = get_connection()
#     if not conn:
#         raise HTTPException(status_code=500, detail="Database connection failed")

#     try:
#         cursor = conn.cursor()
#         query = """
#             SELECT PS FROM m_police_station
#             WHERE PS_CD = %s AND DISTRICT_CD = %s AND STATE_CD = %s
#         """
#         cursor.execute(query, (ps_cd, district_cd, state_cd))
#         result = cursor.fetchone()

#         if result:
#             return {"police_station": result[0]}
#         else:
#             raise HTTPException(status_code=404, detail="Police station not found")

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

#     finally:
#         try:
#             cursor.fetchall()  # Consume any remaining results
#         except:
#             pass
#         cursor.close()
#         conn.close()




# @app.get("/district/name")
# def get_district_name(district_cd: float, state_cd: float):
#     conn = get_connection()
#     if not conn:
#         raise HTTPException(status_code=500, detail="Database connection failed")

#     try:
#         cursor = conn.cursor()
#         query = """
#             SELECT DISTRICT FROM m_district
#             WHERE DISTRICT_CD = %s AND STATE_CD = %s
#         """
#         cursor.execute(query, (district_cd, state_cd))
#         result = cursor.fetchone()

#         if result:
#             return {"district_name": result[0]}
#         else:
#             raise HTTPException(status_code=404, detail="District not found")

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

#     finally:
#         try:
#             cursor.fetchall()  # Consume any remaining unread results
#         except:
#             pass
#         cursor.close()
#         conn.close()





# @app.get("/extract-articles")
# def extract_news_articles(
#     request: Request,
#     start_date: Optional[str] = Query(None),
#     end_date: Optional[str] = Query(None),
#     last_24_hours: Optional[bool] = Query(False)
# ):
#     # 1. Reuse get_news to fetch image records
#     news_response = get_news(
#         start_date=start_date,
#         end_date=end_date,
#         last_24_hours=last_24_hours
#     )

#     # 2. Extract only base64 images
#     news_items = news_response.body
#     import json
#     decoded = json.loads(news_items.decode())
#     base64_images = [item["image_base64"] for item in decoded if item["image_base64"]]

#     if not base64_images:
#         return {"articles": [], "message": "No images found for this date range."}

#     # 3. OCR processing
#     structured_articles = process_base64_images(base64_images)
#     return {"articles": structured_articles}



# from fastapi import APIRouter, Request, Query, HTTPException
# from typing import Optional
# from services.keyword_extractor import analyze_articles



# @app.get("/extract-keywords")
# def auto_extract_keywords(
#     request: Request,
#     start_date: Optional[str] = Query(None),
#     end_date: Optional[str] = Query(None),
#     last_24_hours: Optional[bool] = Query(False)
# ):
#     import json

#     try:
#         if last_24_hours:
#             end = datetime.now()
#             start = end - timedelta(days=1)
#         elif start_date:
#             start = datetime.strptime(start_date, "%Y-%m-%d")
#             end = datetime.strptime(end_date, "%Y-%m-%d") if end_date else start
#         else:
#             raise HTTPException(status_code=400, detail="Provide either 'last_24_hours' or 'start_date'")
#     except ValueError:
#         raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")

#     fir_start = start - timedelta(days=7)
#     fir_end = end

#     # --- Step 1: Get News Articles ---
#     article_response = extract_news_articles(
#         request=request,
#         start_date=start.strftime("%Y-%m-%d"),
#         end_date=end.strftime("%Y-%m-%d"),
#         last_24_hours=last_24_hours
#     )
#     articles = article_response.get("articles", [])

#     # --- Step 2: Get FIR Records ---
#     fir_response = get_fir_records(
#         start_date=fir_start.strftime("%Y-%m-%d"),
#         end_date=fir_end.strftime("%Y-%m-%d"),
#         last_24_hours=False
#     )

#     # If get_fir_records returns JSONResponse, decode the body:
#     if hasattr(fir_response, "body"):
#         try:
#             fir_list = json.loads(fir_response.body.decode("utf-8"))
#         except Exception as e:
#             raise HTTPException(status_code=500, detail=f"Failed to decode FIR records: {str(e)}")
#     else:
#         fir_list = fir_response  # If it directly returns the list

#     fir_texts = [
#         item["FIR_CONTENTS"].strip()
#         for item in fir_list
#         if item.get("FIR_CONTENTS") and len(item["FIR_CONTENTS"].strip()) > 30
#     ]

#     if not articles and not fir_texts:
#         raise HTTPException(status_code=404, detail="No valid news or FIR text to extract.")

#     # --- Step 3: Keyword Extraction ---
#     news_keywords = analyze_articles(articles) if articles else []
#     fir_keywords = analyze_articles(fir_texts) if fir_texts else []

#     return {
#         "news_keywords": news_keywords,
#         "fir_keywords": fir_keywords
#     }



# from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline

# from fastapi import APIRouter, HTTPException
# from typing import List
# from fastapi.responses import JSONResponse

# @app.get("/law-hi", response_model=List[str])
# def get_law_hi():
#     conn = get_connection()
#     if not conn:
#         raise HTTPException(status_code=500, detail="Database connection failed")

#     try:
#         cursor = conn.cursor()
#         query = "SELECT relevant_law_section_hindi FROM crime_data"
#         cursor.execute(query)
#         rows = cursor.fetchall()
#         cursor.close()
#         conn.close()

#         # Return plain list
#         return [row[0] for row in rows if row[0]]

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))



# # from services.scoring_engine import run_scoring_and_save
# from services.keyword_extractor import analyze_articles


# @app.get("/generate-report")
# def generate_final_summary(
#     request: Request,
#     start_date: Optional[str] = Query(None),
#     end_date: Optional[str] = Query(None),
#     last_24_hours: Optional[bool] = Query(False)
# ):
#     import json

#     # Step 1: Extract News Articles
#     article_response = extract_news_articles(request, start_date, end_date, last_24_hours)
#     articles = article_response.get("articles", [])
#     if not articles:
#         raise HTTPException(status_code=404, detail="No news articles found.")
#     all_info_2d_list = analyze_articles(articles)

#     # Step 2: Compute FIR time range (7 days back from start)
#     try:
#         if last_24_hours:
#             end_dt = datetime.now()
#             start_dt = end_dt - timedelta(days=1)
#         elif start_date:
#             start_dt = datetime.strptime(start_date, "%Y-%m-%d")
#             end_dt = datetime.strptime(end_date, "%Y-%m-%d") if end_date else start_dt
#         else:
#             raise HTTPException(status_code=400, detail="Provide either 'last_24_hours' or 'start_date'")
#     except ValueError:
#         raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")

#     fir_start = start_dt - timedelta(days=7)
#     fir_end = end_dt

#     # Step 3: Fetch FIR records
#     fir_response = get_fir_records(
#         start_date=fir_start.strftime("%Y-%m-%d"),
#         end_date=fir_end.strftime("%Y-%m-%d"),
#         last_24_hours=False
#     )
#     fir_list = json.loads(fir_response.body.decode("utf-8")) if hasattr(fir_response, "body") else fir_response

#     # Step 4: Extract keywords from FIR contents
#     fir_texts = [
#         item["FIR_CONTENTS"].strip()
#         for item in fir_list
#         if item.get("FIR_CONTENTS") and len(item["FIR_CONTENTS"].strip()) > 30
#     ]
#     fir_info_2d_list = analyze_articles(fir_texts) if fir_texts else []

#     # Step 5: Load law_hi
#     law_hi = get_law_hi()

#     # Step 6: Define crime mappings
#     crime_severity_sorted = {
#         'शराब तस्करी': 6, 'जुआ': 2, 'गौ हत्या': 6, 'गौ तस्करी': 5, 'नशीली दवाओं की तस्करी': 9, 'हथियारों की तस्करी': 9,
#         'मादक पदार्थ तस्करी': 9, 'अवैध हथियार रखना': 8, 'एनडीपीएस': 8, 'मादक पदार्थ': 7, 'वन्यजीव तस्करी': 7,
#         'अवैध उत्पादों की तस्करी': 7, 'फेंटेनिल': 4, 'एमडी ड्रग': 4, 'मेफेड्रोन': 4, 'कोकीन': 4, 'ब्राउन शुगर': 4,
#         'हेरोइन': 4, 'गांजा': 4, 'धार्मिक उन्माद': 7, 'नकली नोट': 7, 'आतंकवाद': 10, 'देशद्रोह': 10, 'माओवाद': 9,
#         'नक्सली': 9, 'नक्सलवाद': 9, 'पुनर्वास नीति': 2, 'साइबर अपराध': 6, 'डिजिटल गिरफ्तारी': 2, 'साइबर धोखाधड़ी': 6,
#         'डकैती': 9, 'लूट': 8, 'गृहभेदन': 6, 'धोखाधड़ी': 6, 'चोरी': 5, 'ठगी': 5, 'सांप्रदायिक हत्या': 6, 'हत्या': 10,
#         'बलात्कार': 10, 'दुष्कर्म': 10, 'मानव तस्करी': 10, 'नाबालिग से दुष्कर्म': 10, 'हत्या का प्रयास': 9,
#         'बलात्कार का प्रयास': 9, 'अपहरण': 8, 'घरेलू हिंसा': 4, 'आत्महत्या के लिए उकसाना': 4, 'छेड़छाड़': 6,
#         'मारपीट': 6, 'पत्नि पर अत्याचार': 7, 'धमकी देना': 5, 'ईनामी': 0, 'अवैध परिवहन': 0, 'बिक्री': 0, 'आत्मसमर्पण': 0
#     }
#     crime_type_hi = [
#         "हत्या", "हत्या का प्रयास", "बलात्कार", "बलात्कार का प्रयास", "छेड़छाड़", "दुष्कर्म", "अपहरण", "डकैती", "लूट", "चोरी",
#         "गृहभेदन", "मारपीट", "धोखाधड़ी", "ठगी", "घूसखोरी", "साइबर अपराध", "नकली नोट", "नशीली दवाओं की तस्करी", "शराब तस्करी",
#         "मानव तस्करी", "घरेलू हिंसा", "आतंकवाद", "देशद्रोह", "धार्मिक उन्माद", "नाबालिग से दुष्कर्म", "पत्नि पर अत्याचार",
#         "आत्महत्या के लिए उकसाना", "धमकी देना", "अवैध हथियार रखना", "हथियारों की तस्करी", "जुआ", "मादक पदार्थ तस्करी",
#         "नशीली दवाओं की तस्करी", "तस्करी", "नक्सली", "आत्मसमर्पण", "ईनामी", "पुनर्वास नीति", "माओवाद", "गांजा", "मादक पदार्थ",
#         "एनडीपीएस", "बिक्री", "अवैध परिवहन", "नक्सलवाद", "देशद्रोह", "गौ हत्या", "गौ तस्करी"
#     ]

#     # Step 7: Final scoring using FIR extracted keywords
#     from services.scoring_engine import run_scoring_and_save_keywords

#     report_data = run_scoring_and_save_keywords(
#         fir_info_2d_list,             # FIR keywords 2D
#         all_info_2d_list,             # News keywords 2D
#         law_hi,
#         crime_type_hi,
#         crime_severity_sorted
#     )


#     return {
#         "message": "Report generation complete",
#         "total": len(report_data)
#     }



# from fastapi import Query, HTTPException
# from fastapi.responses import JSONResponse
# import base64

# @app.get("/getnews/by-id")
# def get_news_by_upload_id(upload_id: int = Query(..., description="Unique Upload ID")):
#     conn = get_connection()
#     if not conn:
#         raise HTTPException(status_code=500, detail="Database connection failed")

#     cursor = conn.cursor()
#     query = """
#         SELECT UPLOAD_ID, LANG_CD, UPLOADED_FILE, RECORD_CREATED_ON
#         FROM t_news_upload
#         WHERE UPLOAD_ID = %s
#     """
#     cursor.execute(query, (upload_id,))
#     row = cursor.fetchone()

#     if not row:
#         return JSONResponse(content={"message": "No record found with the given Upload ID."}, status_code=404)

#     upload_id, lang_cd, image_blob, created_on = row
#     image_base64 = base64.b64encode(image_blob).decode('utf-8') if image_blob else None

#     result = {
#         "upload_id": upload_id,
#         "language_code": lang_cd,
#         "image_base64": image_base64,
#         "created_on": str(created_on)
#     }

#     cursor.close()
#     conn.close()

#     return JSONResponse(content=result)


# @app.get("/extract-single-news")
# def extract_single_news(upload_id: int = Query(..., description="Upload ID for the news image")):
#     # Step 1: Fetch the image using existing DB logic
#     conn = get_connection()
#     if not conn:
#         raise HTTPException(status_code=500, detail="Database connection failed")

#     cursor = conn.cursor()
#     query = """
#         SELECT UPLOAD_ID, LANG_CD, UPLOADED_FILE, RECORD_CREATED_ON
#         FROM t_news_upload
#         WHERE UPLOAD_ID = %s
#     """
#     cursor.execute(query, (upload_id,))
#     row = cursor.fetchone()

#     if not row:
#         raise HTTPException(status_code=404, detail="No record found with the given Upload ID.")

#     upload_id, lang_cd, image_blob, created_on = row
#     image_base64 = base64.b64encode(image_blob).decode('utf-8') if image_blob else None

#     cursor.close()
#     conn.close()

#     if not image_base64:
#         return {"message": "No image found for the given Upload ID."}

#     # Step 2: Run OCR using process_base64_images (already defined in your project)
#     articles = process_base64_images([image_base64])

#     return {"upload_id": upload_id, "extracted_articles": articles}


# import requests
# from fastapi import Query, HTTPException
# from fastapi.responses import JSONResponse
# import services.keyword_extractor

# @app.get("/news_keywords")
# def news_keywords(upload_id: int = Query(..., description="Upload ID of the news image")):
#     try:
#         # 🔁 Call the local /extract-single-news endpoint using requests
#         response = requests.get(f"http://localhost:8000/extract-single-news?upload_id={upload_id}")
#         if response.status_code != 200:
#             raise HTTPException(status_code=response.status_code, detail=response.json().get("detail", "Error in OCR extraction"))

#         extracted_data = response.json()
#         extracted_texts = extracted_data.get("extracted_articles", [])
#         if not extracted_texts:
#             raise HTTPException(status_code=404, detail="No OCR text found.")

#         text = extracted_texts[0]

#         # 🔍 Use keyword_extractor functions
#         heading, summary = services.keyword_extractor.extract_summary_string(text)

#         response_json = {
#             "incidentNo": str(upload_id),
#             "districtName": services.keyword_extractor.extract_district(text),
#             "psName": services.keyword_extractor.extract_police_station(text),
#             "complaintantName": services.keyword_extractor.extract_complainant(text),
#             "accusedName": services.keyword_extractor.extract_accused(text),
#             "weapon": services.keyword_extractor.extract_weapons(text),
#             "crimeType": services.keyword_extractor.extract_crime_type(text),
#             "summary": summary,
#             "newsHeading": heading
#         }

#         return JSONResponse(content=response_json)

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Keyword extraction failed: {str(e)}")


from fastapi import File, UploadFile, HTTPException
import base64
import services.keyword_extractor

@app.post("/extract_keywords_from_image")
async def extract_keywords_from_image(file: UploadFile = File(...)):
    try:
        # 1. Read the uploaded image file and encode to base64
        image_bytes = await file.read()
        image_base64 = base64.b64encode(image_bytes).decode("utf-8")

        # 2. Run OCR
        articles = process_base64_images([image_base64])
        if not articles:
            raise HTTPException(status_code=400, detail="OCR failed or empty result.")
        text = articles[0]

        # 3. Run keyword extraction
        heading, summary = services.keyword_extractor.extract_summary_string(text)
        response_json = {
            "incidentNo": "N/A",  # No upload_id since this is direct upload
            "districtName": services.keyword_extractor.extract_district(text),
            "psName": services.keyword_extractor.extract_police_station(text),
            "complaintantName": services.keyword_extractor.extract_complainant(text),
            "accusedName": services.keyword_extractor.extract_accused(text),
            "weapon": services.keyword_extractor.extract_weapons(text),
            "crimeType": services.keyword_extractor.extract_crime_type(text),
            "summary": summary,
            "newsHeading": heading
        }

        return JSONResponse(content=response_json)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image keyword extraction failed: {str(e)}")

# code as per google cloud deployment

if __name__ == "__main__":
    import os
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
    

