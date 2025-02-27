from flask import render_template, request, url_for, current_app, jsonify
from flask_login import login_required, current_user
import requests
from app.utils.permissions import role_required
from app.models.user import Company
from . import job_posting_bp

# should take from config
job_service_url = "http://job-service:80"
db_api_url = "http://db-service:80"


# needs refactoring
@job_posting_bp.route("/jobs/submit", methods=["GET", "POST"])
@login_required
@role_required(allowed_roles=[Company])
def submit_job():
    db_api_url = current_app.config.get("DB_API_URL", "http://db-service:80")
    jobs = []
    try:
        response = requests.get(f"{db_api_url}/jobs/{current_user.uid}")
        if response.status_code == 200:
            jobs = response.json().get("jobs", [])
    except requests.exceptions.RequestException:
        jobs = []

    if request.method == "POST":
        job_url = request.form.get("job_url")
        site = request.form.get("site")
        if not job_url or not site:
            return (
                jsonify(
                    {
                        "status": "error",
                        "message": "Please provide both Job URL and Site.",
                    }
                ),
                400,
            )

        tmp_job_payload = {"company_id": current_user.uid}
        scraper_payload = {"url": job_url, "site": site}
        try:
            # Create a temporary job in the database
            response = requests.post(
                f"{db_api_url}/jobs/create_tmp", json=tmp_job_payload
            )
            if response.status_code != 201:
                error_msg = response.json().get("message", "Unknown error")
                return (
                    jsonify(
                        {
                            "status": "error",
                            "message": f"Job posting failed: {error_msg}",
                        }
                    ),
                    response.status_code,
                )
            tmp_job_id = response.json().get("job_id")
            scraper_payload["id"] = tmp_job_id

            # Submit the job scraping request to the job service
            response = requests.post(
                f"{job_service_url}/jobs/scrape", json=scraper_payload
            )
            if response.status_code == 201:
                return jsonify(
                    {
                        "status": "success",
                        "message": "Job submitted successfully! It is being processed.",
                    }
                )
            else:
                error_msg = response.json().get("message", "Unknown error")
                return (
                    jsonify(
                        {
                            "status": "error",
                            "message": f"Job posting failed: {error_msg}",
                        }
                    ),
                    response.status_code,
                )
        except requests.exceptions.RequestException as e:
            return (
                jsonify(
                    {
                        "status": "error",
                        "message": f"Error connecting to job service: {str(e)}",
                    }
                ),
                500,
            )

    return render_template("job_posting.html", jobs=jobs)
