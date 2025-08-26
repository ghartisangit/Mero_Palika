MeroPalika

MeroPalika is a Django-based municipal management system designed to streamline citizen services within Nepali local government contexts.

Features

Complaint Submission – Citizens can file grievances or complaints.

Vacancy Postings – Municipal authorities can post and manage job opportunities.

Notices & Announcements – Publish important updates for citizens.

Training Programs – Create and manage training events.

Role-Based Apps –

accounts → User authentication and profile management

complaints → Handling complaint submissions and statuses

dashboard → Municipality/admin dashboards

notices → Notice publication and management

Tech Stack
Component	Technology
Framework	Django (Python)
Frontend	HTML, CSS, JavaScript
File Handling	Media uploads (media/)
Templates	Django Templates (templates/)
Configurations	.env file for secrets/env
Database	SQLite/PostgreSQL/MySQL
Dependencies	requirements.txt
Version Control	Git + GitHub
Installation
Prerequisites

Python 3.8+

Virtual environment (venv or virtualenv)

Steps
# Clone the repository
git clone https://github.com/samir-28/MeroPalika.git
cd MeroPalika

# Create & activate virtual environment
python -m venv venv
source venv/bin/activate     # On Windows: .\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Run the server
python manage.py runserver

Usage

Open http://127.0.0.1:8000/
 in your browser.

Register/login through the Accounts module.

Explore available features:

Submit/view complaints

View notices

Apply for vacancies

Access admin dashboard (for municipalities)

Project Structure
MeroPalika/
│── accounts/        # User accounts & authentication
│── complaints/      # Complaint management
│── core/            # Core settings & utilities
│── dashboard/       # Municipality/admin dashboards
│── notices/         # Notices & announcements
│── static/          # CSS, JS, Images
│── templates/       # HTML templates
│── media/complaints # Uploaded complaint files
│── env/             # Environment config
│── manage.py        # Django management script
│── requirements.txt # Python dependencies
└── .gitignore       # Ignored files for Git

Contribution

Fork the repository

Create a branch (git checkout -b feature-xyz)

Commit changes (git commit -m "Add feature xyz")

Push branch (git push origin feature-xyz)

Create a Pull Request
