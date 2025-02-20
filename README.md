# Obsidian-Static-Web

## Overview
A static web creater, serves an obsidian vault to the web. Uses pypandoc to convert markdown to html, and django to server the site.

## Requirements
- Python 3.x
- Django
- PyPandoc
- Gunicorn

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/subtodempen/Obsidian-Static-Web.git
    cd Obsidian-Static-Web
    ```

2. Set up a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On macOS/Linux
    .\venv\Scripts\activate   # On Windows
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up the database:
    ```bash
    python manage.py migrate
    ```

5. Create a superuser (optional):
    ```bash
    python manage.py createsuperuser
    ```

6. Run the development server:
    ```bash
    python manage.py runserver
    ```

