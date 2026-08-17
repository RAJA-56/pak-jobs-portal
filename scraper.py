import requests
import json

def categorize_job(title):
    t = title.lower()
    if any(k in t for k in ['python', 'backend', 'django', 'fastapi', 'sql', 'node']):
        return "Python / Backend"
    elif any(k in t for k in ['react', 'vue', 'frontend', 'web', 'html', 'css', 'javascript']):
        return "Web Development"
    elif any(k in t for k in ['design', 'ui', 'ux', 'graphic', 'figma']):
        return "Design & Creative"
    else:
        return "Software & Tech"

def detect_city(location_str):
    loc = location_str.lower()
    if 'lahore' in loc: return "Lahore"
    elif 'karachi' in loc: return "Karachi"
    elif 'islamabad' in loc: return "Islamabad"
    else: return "Remote / Global"

def fetch_jobs():
    cleaned_jobs = []
    
    try:
        res = requests.get("https://jobicy.com/api/v2/remote-jobs?count=30&industry=dev", timeout=15)
        if res.status_code == 200:
            data = res.json().get('jobs', [])
            for job in data:
                title = job.get('jobTitle', 'Software Position')
                location = job.get('jobGeo', 'Remote')
                
                cleaned_jobs.append({
                    "id": str(job.get('id')),
                    "title": title,
                    "company": job.get('companyName', 'Tech Company'),
                    "city": detect_city(location),
                    "category": categorize_job(title),
                    "url": job.get('url', '#'),
                    "date": str(job.get('pubDate', ''))[:10],
                    "is_featured": False
                })
    except Exception as e:
        print(f"Error: {e}")

    # Example featured job slot
    featured_spot = {
        "id": "feat-101",
        "title": "Senior Python & Automation Developer",
        "company": "PakTech Solutions",
        "city": "Lahore",
        "category": "Python / Backend",
        "url": "https://wa.me/923000000000",
        "date": "2026-08-17",
        "is_featured": True
    }
    cleaned_jobs.insert(0, featured_spot)

    with open("jobs.json", "w", encoding="utf-8") as f:
        json.dump(cleaned_jobs, f, indent=2)

if __name__ == "__main__":
    fetch_jobs()
