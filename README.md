# Professional Personal Website

A modern, responsive personal website built with Flask, featuring a newsletter subscription system and responsive design.

## Project Structure
```
├── app.py                 # Main Flask application
├── database.py           # Database configuration
├── models.py            # Database models
├── static/              # Static assets
│   ├── css/
│   │   └── styles.css   # Main stylesheet
│   ├── js/
│   │   └── main.js     # JavaScript functionality
│   └── images/         # Image assets
└── templates/          # HTML templates
    └── index.html      # Main template file
```

## Requirements
- Python 3.11
- PostgreSQL database
- Mailgun account for email notifications

## Environment Variables
Create a `.env` file with the following variables:
```
DATABASE_URL=postgresql://username:password@host:port/database
MAILGUN_API_KEY=your_mailgun_api_key
MAILGUN_DOMAIN=your_mailgun_domain
```

## Installation
1. Clone the repository
2. Install dependencies:
   ```
   pip install flask flask-sqlalchemy requests python-dotenv
   ```
3. Set up environment variables
4. Initialize the database:
   ```
   flask db upgrade
   ```
5. Run the application:
   ```
   python app.py
   ```

The application will be available at `http://localhost:5000`

## Features
- Responsive design for all devices
- Newsletter subscription system
- Email notifications via Mailgun
- Modern animations and transitions
- Blog section
- Testimonials section

## Deployment
The application is ready to be deployed to any hosting platform that supports Python/Flask applications. Make sure to:

1. Set up all required environment variables
2. Configure your database URL
3. Set up your Mailgun credentials
4. Configure your web server (e.g., Gunicorn, uWSGI)

## Contact
For any questions or support, please contact: mxzadeh@gmail.com
