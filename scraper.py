import requests
import json
import re

def clean_html(text):
    """Strip raw HTML tags so clean plain text descriptions show up on the web page"""
    if not text:
        return "Click 'Apply Direct' to view complete details on the hiring site."
    clean = re.sub(r'<[^>]+>', ' ', str(text))
    clean = ' '.join(clean.split())
    return clean[:450] + "..." if len(clean) > 450 else clean

def categorize_job(title):
    t = str(title).lower()
    if any(k in t for k in ['python', 'backend', 'django', 'fastapi', 'node', 'java', 'c++', 'php', 'golang']):
        return "Python / Backend"
    elif any(k in t for k in ['react', 'vue', 'frontend', 'web', 'html', 'css', 'javascript', 'typescript', 'wordpress']):
        return "Web Development"
    elif any(k in t for k in ['android', 'ios', 'flutter', 'react native', 'mobile']):
        return "Mobile Development"
    elif any(k in t for k in ['ai', 'data', 'machine learning', 'nlp', 'analyst', 'python']):
        return "Data & AI"
    elif any(k in t for k in ['design', 'ui', 'ux', 'graphic', 'figma', 'video']):
        return "Design & Creative"
    elif any(k in t for k in ['sales', 'marketing', 'seo', 'content', 'social media', 'copywriter']):
        return "Marketing & Sales"
    elif any(k in t for k in ['support', 'customer', 'chat', 'service']):
        return "Customer Support"
    elif any(k in t for k in ['admin', 'hr', 'manager', 'accountant', 'operations', 'assistant']):
        return "Admin & Operations"
    else:
        return "Web Development"

def detect_city(location_str):
    loc = str(location_str).lower()
    if 'lahore' in loc: return "Lahore"
    elif 'karachi' in loc: return "Karachi"
    elif 'islamabad' in loc: return "Islamabad"
    elif 'rawalpindi' in loc: return "Rawalpindi"
    elif 'faisalabad' in loc: return "Faisalabad"
    elif 'pakistan' in loc: return "Pakistan (Physical)"
    else: return "Remote / Global"

def fetch_jobicy():
    jobs = []
    try:
        res = requests.get("https://jobicy.com/api/v2/remote-jobs?count=40", timeout=10)
        if res.status_code == 200:
            for item in res.json().get('jobs', []):
                jobs.append({
                    "id": f"jobicy-{item.get('id')}",
                    "title": item.get('jobTitle', 'Position'),
                    "company": item.get('companyName', 'Tech Company'),
                    "city": detect_city(item.get('jobGeo', 'Remote')),
                    "category": categorize_job(item.get('jobTitle', '')),
                    "url": item.get('url', '#'),
                    "description": clean_html(item.get('jobDescription', '')),
                    "source": "Jobicy Network",
                    "is_featured": False
                })
    except Exception as e: print(f"Jobicy Error: {e}")
    return jobs

def fetch_remotive():
    jobs = []
    try:
        res = requests.get("https://remotive.com/api/remote-jobs?limit=40", timeout=10)
        if res.status_code == 200:
            for item in res.json().get('jobs', []):
                jobs.append({
                    "id": f"remotive-{item.get('id')}",
                    "title": item.get('title', 'Position'),
                    "company": item.get('company_name', 'Company'),
                    "city": detect_city(item.get('candidate_required_location', 'Remote')),
                    "category": categorize_job(item.get('title', '')),
                    "url": item.get('url', '#'),
                    "description": clean_html(item.get('description', '')),
                    "source": "Remotive",
                    "is_featured": False
                })
    except Exception as e: print(f"Remotive Error: {e}")
    return jobs

def fetch_arbeitnow():
    jobs = []
    try:
        res = requests.get("https://www.arbeitnow.com/api/job-board-api", timeout=10)
        if res.status_code == 200:
            for item in res.json().get('data', []):
                jobs.append({
                    "id": f"arbeit-{item.get('slug')}",
                    "title": item.get('title', 'Position'),
                    "company": item.get('company_name', 'Company'),
                    "city": detect_city(item.get('location', 'Remote')),
                    "category": categorize_job(item.get('title', '')),
                    "url": item.get('url', '#'),
                    "description": clean_html(item.get('description', '')),
                    "source": "Arbeitnow",
                    "is_featured": False
                })
    except Exception as e: print(f"Arbeitnow Error: {e}")
    return jobs

def main():
    all_jobs = []
    
    # 1. Scrape from all 3 API networks
    all_jobs.extend(fetch_jobicy())
    all_jobs.extend(fetch_remotive())
    all_jobs.extend(fetch_arbeitnow())

    # 2. Add pinned sponsor spot
    featured_spot = {
        "id": "feat-101",
        "title": "Featured Job Slot: Promote Your Vacancy Here",
        "company": "PakJobs Hub Sponsorship",
        "city": "Lahore / Remote",
        "category": "Admin & Operations",
        "url": "https://wa.me/923000000000?text=Hi,%20I%20want%20to%20feature%20a%20job",
        "description": "Get your job posting pinned at the top of PakJobs Hub for max exposure across developers in Pakistan. Instant WhatsApp application delivery.",
        "source": "PakJobs Direct",
        "is_featured": True
    }
    all_jobs.insert(0, featured_spot)

    # Save to JSON
    with open("jobs.json", "w", encoding="utf-8") as f:
        json.dump(all_jobs, f, indent=2)

    print(f"Updated jobs.json with {len(all_jobs)} rich job entries.")

if __name__ == "__main__":
    main()
