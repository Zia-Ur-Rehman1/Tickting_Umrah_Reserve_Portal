# 🎫 Tickting Umrah Reserve Portal

*Empowering Seamless Umrah Ticketing and Travel Experience*

![last-commit](https://img.shields.io/github/last-commit/Zia-Ur-Rehman1/Tickting_Umrah_Reserve_Portal?style=flat&logo=git&logoColor=white&color=0080ff)
![repo-top-language](https://img.shields.io/github/languages/top/Zia-Ur-Rehman1/Tickting_Umrah_Reserve_Portal?style=flat&color=0080ff)
![repo-language-count](https://img.shields.io/github/languages/count/Zia-Ur-Rehman1/Tickting_Umrah_Reserve_Portal?style=flat&color=0080ff)

---

## 🧰 Built With the tools and technologies:
---
![JSON](https://img.shields.io/badge/JSON-000000.svg?style=flat&logo=JSON&logoColor=white)
![Markdown](https://img.shields.io/badge/Markdown-000000.svg?style=flat&logo=Markdown&logoColor=white)
![Sphinx](https://img.shields.io/badge/Sphinx-000000.svg?style=flat&logo=Sphinx&logoColor=white)
![npm](https://img.shields.io/badge/npm-CB3837.svg?style=flat&logo=npm&logoColor=white)
![Autoprefixer](https://img.shields.io/badge/Autoprefixer-DD3735.svg?style=flat&logo=Autoprefixer&logoColor=white)
![PostCSS](https://img.shields.io/badge/PostCSS-DD3A0A.svg?style=flat&logo=PostCSS&logoColor=white)
![Cookiecutter](https://img.shields.io/badge/Cookiecutter-D4AA00.svg?style=flat&logo=Cookiecutter&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E.svg?style=flat&logo=JavaScript&logoColor=black)
![Rich](https://img.shields.io/badge/Rich-FAE742.svg?style=flat&logo=Rich&logoColor=black)
![GNU Bash](https://img.shields.io/badge/GNU%20Bash-4EAA25.svg?style=flat&logo=GNU-Bash&logoColor=white)
![Gunicorn](https://img.shields.io/badge/Gunicorn-499848.svg?style=flat&logo=Gunicorn&logoColor=white)
![NGINX](https://img.shields.io/badge/NGINX-009639.svg?style=flat&logo=NGINX&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20.svg?style=flat&logo=Django&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243.svg?style=flat&logo=NumPy&logoColor=white)
![jQuery](https://img.shields.io/badge/jQuery-0769AD.svg?style=flat&logo=jQuery&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED.svg?style=flat&logo=Docker&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB.svg?style=flat&logo=Python&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-2088FF.svg?style=flat&logo=GitHub-Actions&logoColor=white)
![pandas](https://img.shields.io/badge/pandas-150458.svg?style=flat&logo=pandas&logoColor=white)
---

## 📚 Table of Contents

- [📌 Overview](#-overview)
- [⚙️ Features](#️-features)
- [🧰 Tech Stack](#-tech-stack)
- [🚀 Getting Started](#-getting-started)
- [🛠 Useful Commands](#-useful-commands)
- [📂 Project Structure](#-project-structure)
- [📄 License](#-license)
- [🙋‍♂️ Author](#-author)
- [🤝 Contributing](#-contributing)

---

## 📌 Overview

**Tickting Umrah Reserve Portal** is a web-based system designed to manage Umrah travel bookings efficiently. It helps agencies handle ticket reservations, service requests, and customer interactions, all in one streamlined platform.

---

## ⚙️ Features

- 🧾 Umrah ticket booking and management
- 👥 Agent and admin role-based access
- 🔄 Service request matching system
- 📊 Dashboard for flight and booking summaries
- 🧠 **AI-powered image parsing** for payment confirmations
- 📄 **AI-powered PDF parsing** for auto-filling ticket forms
- 🔌 RESTful API support
- 🛰 Dockerized environment
- 📦 Integrated CI/CD with GitHub Actions

---

## 🧰 Tech Stack

- **Backend:** Django, Python, PostgreSQL
- **Frontend:** HTML, CSS, JavaScript, jQuery
- **DevOps:** Docker, GitHub Actions, NGINX, Gunicorn
- **Tools & Libraries:** NumPy, pandas, Sphinx, Markdown, Cookiecutter, Rich

---

## 🚀 Getting Started

### Clone & Run with Docker

```bash
git clone https://github.com/Zia-Ur-Rehman1/Tickting_Umrah_Reserve_Portal.git
cd Tickting_Umrah_Reserve_Portal
docker-compose up --build
````

Visit: [http://localhost:8000](http://localhost:8000)

### Manual Setup

```bash
# Create and activate virtualenv
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run database migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

---

## 🛠 Useful Commands

```bash
# Collect static files
python manage.py collectstatic

# Run tests
python manage.py test
```

---

## 📂 Project Structure

```
Tickting_Umrah_Reserve_Portal/
├── apps/
│   ├── tickets/
│   ├── agents/
│   └── dashboard/
├── templates/
├── static/
├── manage.py
├── docker-compose.yml
└── requirements.txt
```

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 🙋‍♂️ Author

**Zia Ur Rehman**
GitHub: [Zia-Ur-Rehman1](https://github.com/Zia-Ur-Rehman1)

---

## 🤝 Contributing

Contributions are welcome!
Feel free to fork the repo, open issues, or submit pull requests.

---

