import requests
import json
import re

def categorize_job(title):
    t = title.lower()
    if any(k in t for k in ['python', 'backend', 'django', 'fastapi', 'sql', 'node', 'java', 'c++', 'php']):
        return "Python / Backend"
    elif any(k in t for k in ['react', 'vue', 'frontend', 'web', 'html', 'css', 'javascript', 'wordpress']):
        return "Web Development"
    elif any(k in t for k in ['design', 'ui', 'ux', 'graphic', 'figma', 'video', 'animator']):
        return "Design & Creative"
    elif any(k in t for k in ['sales', 'marketing', 'seo', 'content', 'social media', 'copywriter']):
        return "Marketing & Sales"
    elif any(k in t for k in ['admin', 'hr', 'manager', 'accountant', 'customer support', 'assistant']):
        return "Admin & Management"
    else:
        return "General / Other"

def detect_city(location_str):
    loc = location_str.lower()
    if 'lahore' in loc: return "Lahore"
    elif 'karachi' in loc: return "Karachi"
    elif 'islamabad' in loc: return "Islamabad"
    elif 'rawalpindi' in loc: return "Rawalpindi"
    elif 'faisalabad' in loc: return "Faisalabad"
    elif 'pakistan' in loc: return "Pakistan (Physical)"
    else: return "Remote / Global"

def fetch_jobicy():
    """Fetch global remote jobs"""
    jobs = []
    try:
        res = requests.get("https://jobicy.com/api/v2/remote-jobs?count=20", timeout=10)
        if res.status_code == 200:
            for job in res.json().get('jobs', []):
                title = job.get('jobTitle', 'Position')
                location = job.get('jobGeo', 'Remote')
                jobs.append({
                    "id": f"jobicy-{job.get('id')}",
                    "title": title,
                    "company": job.get('companyName', 'Company'),
                    "city": detect_city(location),
                    "category": categorize_job(title),
                    "url": job.get('url', '#'),
                    "date": str(job.get('pubDate', ''))[:10],
                    "is_featured": False
                })
    except Exception as e:
        print(f"Error Jobicy: {e}")
    return jobs

def fetch_arbeitnow():
    """Fetch physical and remote jobs from global job network"""
    jobs = []
    try:
        res = requests.get("https://www.arbeitnow.com/api/job-board-api", timeout=10)
        if res.status_code == 200:
            for job in res.json().get('data', [])[:20]:
                title = job.get('title', 'Position')
                location = job.get('location', 'Remote')
                jobs.append({
                    "id": f"arbeit-{job.get('slug')}",
                    "title": title,
                    "company": job.get('company_name', 'Company'),
                    "city": detect_city(location),
                    "category": categorize_job(title),
                    "url": job.get('url', '#'),
                    "date": "2026-08-17",
                    "is_featured": False
                })
    except Exception as e:
        print(f"Error Arbeitnow: {e}")
    return jobs

def fetch_remotive():
    """Fetch tech and non-tech global remote positions"""
    jobs = []
    try:
        res = requests.get("https://remotive.com/api/remote-jobs?limit=20", timeout=10)
        if res.status_code == 200:
            for job in res.json().get('jobs', [])[:20]:
                title = job.get('title', 'Position')
                location = job.get('candidate_required_location', 'Remote')
                jobs.append({
                    "id": f"remotive-{job.get('id')}",
                    "title": title,
                    "company": job.get('company_name', 'Company'),
                    "city": detect_city(location),
                    "category": categorize_job(title),
                    "url": job.get('url', '#'),
                    "date": str(job.get('publication_date', ''))[:10],
                    "is_featured": False
                })
    except Exception as e:
        print(f"Error Remotive: {e}")
    return jobs

def main():
    all_jobs = []
    
    # 1. Gather jobs from all networks
    all_jobs.extend(fetch_jobicy())
    all_jobs.extend(fetch_arbeitnow())
    all_jobs.extend(fetch_remotive())

    # 2. Add manual physical local Pakistani openings & sponsored jobs
    local_physical_sample = {
        "id": "pk-loc-101",
        "title": "Office Admin & Operations Executive (Physical)",
        "company": "Apex Logistics Pakistan",
        "city": "Lahore",
        "category": "Admin & Management",
        "url": "https://wa.me/923000000000",
        "date": "2026-08-17",
        "is_featured": True
    }
    
    # Place featured/paid spot at the very top
    all_jobs.insert(0, local_physical_sample)

    # Save aggregated jobs to JSON
    with open("jobs.json", "w", encoding="utf-8") as f:
        json.dump(all_jobs, f, indent=2)

    print(f"Success! Saved {len(all_jobs)} jobs across physical & remote categories.")

if __name__ == "__main__":
    main()
