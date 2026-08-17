import requests
import json

def categorize_job(title):
    t = str(title).lower()
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
        return "Software & Tech"

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
        res = requests.get("https://jobicy.com/api/v2/remote-jobs?count=30", timeout=10)
        if res.status_code == 200:
            for job in res.json().get('jobs', []):
                jobs.append({
                    "id": f"jobicy-{job.get('id', '')}",
                    "title": job.get('jobTitle', 'Software Position'),
                    "company": job.get('companyName', 'Company'),
                    "city": detect_city(job.get('jobGeo', 'Remote')),
                    "category": categorize_job(job.get('jobTitle', '')),
                    "url": job.get('url', '#'),
                    "date": "Recent",
                    "is_featured": False
                })
    except Exception as e:
        print(f"Jobicy Error: {e}")
    return jobs

def fetch_arbeitnow():
    jobs = []
    try:
        res = requests.get("https://www.arbeitnow.com/api/job-board-api", timeout=10)
        if res.status_code == 200:
            for job in res.json().get('data', [])[:30]:
                jobs.append({
                    "id": f"arbeit-{job.get('slug', '')}",
                    "title": job.get('title', 'Position'),
                    "company": job.get('company_name', 'Company'),
                    "city": detect_city(job.get('location', 'Remote')),
                    "category": categorize_job(job.get('title', '')),
                    "url": job.get('url', '#'),
                    "date": "Recent",
                    "is_featured": False
                })
    except Exception as e:
        print(f"Arbeitnow Error: {e}")
    return jobs

def fetch_remotive():
    jobs = []
    try:
        res = requests.get("https://remotive.com/api/remote-jobs?limit=30", timeout=10)
        if res.status_code == 200:
            for job in res.json().get('jobs', [])[:30]:
                jobs.append({
                    "id": f"remotive-{job.get('id', '')}",
                    "title": job.get('title', 'Position'),
                    "company": job.get('company_name', 'Company'),
                    "city": detect_city(job.get('candidate_required_location', 'Remote')),
                    "category": categorize_job(job.get('title', '')),
                    "url": job.get('url', '#'),
                    "date": "Recent",
                    "is_featured": False
                })
    except Exception as e:
        print(f"Remotive Error: {e}")
    return jobs

def main():
    all_jobs = []
    
    # Gather jobs from live web APIs
    all_jobs.extend(fetch_jobicy())
    all_jobs.extend(fetch_arbeitnow())
    all_jobs.extend(fetch_remotive())

    # Optional: Featured banner slot for direct monetization (points to WhatsApp)
    featured_spot = {
        "id": "feat-101",
        "title": "Promote Your Company Job Here (Paid Listing)",
        "company": "PakJobs Hub Sponsorship",
        "city": "Lahore / Remote",
        "category": "Admin & Management",
        "url": "https://wa.me/923000000000?text=Hi,%20I%20want%20to%20feature%20a%20job",
        "date": "Pinned",
        "is_featured": True
    }
    
    all_jobs.insert(0, featured_spot)

    # Overwrite jobs.json with clean data
    with open("jobs.json", "w", encoding="utf-8") as f:
        json.dump(all_jobs, f, indent=2)

    print(f"Successfully saved {len(all_jobs)} live jobs to jobs.json.")

if __name__ == "__main__":
    main()
