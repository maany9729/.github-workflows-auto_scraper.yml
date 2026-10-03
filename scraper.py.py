import os
import json
import requests
from supabase import create_client

# 1. Configuration
SUPABASE_URL = "https://pmqjomnfalmqmdpwytgq.supabase.co"

# 👇 In dono me apni keys double quotes ("") ke andar paste kar lein:
SUPABASE_SERVICE_KEY = "sb_secret_pHcXpkPQkmqdiYVJOJTWeg_WUHOtUFO"
GEMINI_API_KEY = "AQ.Ab8RN6JPIFuAHIHIUpeFWuPYRSa-9VStlk7s5pURONM_YlumJw"

supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

def generate_and_insert_trends():
    prompt = """
    Generate 2 fresh, highly engaging, and viral content ideas/hooks for creators in JSON format.
    One should be for 'tech' niche and one for 'finance' niche.
    
    Return ONLY a JSON array with this exact structure:
    [
      {
        "title": "Short Catchy Title",
        "description": "Detailed description/hook structure for the creator",
        "niche": "tech",
        "content_type": "Trend",
        "icon": "fa-robot",
        "status": "pending"
      }
    ]
    """

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"response_mime_type": "application/json"}
    }

    print("🤖 Generating trends using Gemini AI...")
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        generated_text = result['candidates'][0]['content']['parts'][0]['text']
        items = json.loads(generated_text)
        
        # Database me Insert
        data, count = supabase.table('creator_content').insert(items).execute()
        print(f"✅ Successfully inserted {len(items)} AI-generated items into Supabase Pending queue!")
    else:
        print(f"❌ Error from Gemini API: {response.text}")

if __name__ == "__main__":
    generate_and_insert_trends()