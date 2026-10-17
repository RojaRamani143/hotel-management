# RoyalStay — Hotel Booking Demo

Responsive Flask hotel-booking website with Docker, Jenkins, and SQLite persistence.

## Files

```text
royalstay-hotel/
├── app.py
├── requirements.txt
├── Dockerfile
├── Jenkinsfile
├── .dockerignore
├── .gitignore
├── README.md
├── templates/
│   ├── index.html
│   ├── confirmation.html
│   └── not_found.html
└── static/
    ├── style.css
    └── script.js
```

## Docker (on EC2)

```bash
docker build -t royalstay-hotel:local .
docker volume create royalstay-data
docker run -d --name royalstay-container -p 5000:5000 \
  -v royalstay-data:/app/data -e SECRET_KEY='change-this-for-practice' \
  royalstay-hotel:local
curl http://localhost:5000/health
```

Visit `http://EC2-PUBLIC-IP:5000` (allow TCP 5000 from your IP in the EC2 security group).

## Jenkins

1. Push this directory to a GitHub repository.
2. Install Jenkins, Docker, Git, and curl on the Jenkins build agent. Ensure the agent can run Docker.
3. Create a Jenkins **Pipeline** job.
4. Select **Pipeline script from SCM**, Git repository URL, branch `*/main`, and script path `Jenkinsfile`.
5. Click **Build Now**. Jenkins checks out, builds, deploys, and health-checks the app.
6. For push-triggered builds, configure an appropriate GitHub webhook and Jenkins trigger.

Jenkins and the Docker deployment host are assumed to be the same machine. The `royalstay-data` volume persists bookings across container replacements. Jenkins builds interrupt the app briefly. Docker group access is root-equivalent; use an isolated, trusted practice agent.

## Notes

This is a learning demo, **not a real hotel reservation service**. It does not check room availability or process payments. The confirmation URL uses a booking ID and email in the URL; do not enter real guest information. Use authentication, CSRF protection, a proper database, and secret management before production use. Photos and Google Fonts load from external services.
