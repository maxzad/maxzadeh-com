from flask import Flask, render_template, request, jsonify
import os
import requests
import logging
import sys
from database import db

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

app = Flask(__name__, static_url_path='/static')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///blog.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the app with the extension
db.init_app(app)

def send_subscription_email(subscriber_email):
    try:
        MAILGUN_DOMAIN = os.environ.get('MAILGUN_DOMAIN')
        MAILGUN_API_KEY = os.environ.get('MAILGUN_API_KEY')
        
        app.logger.info(f"Attempting to send email for subscriber: {subscriber_email}")
        app.logger.info(f"Using Mailgun Domain: {MAILGUN_DOMAIN}")
        
        if not MAILGUN_DOMAIN or not MAILGUN_API_KEY:
            app.logger.error("Mailgun credentials are missing")
            raise ValueError("Mailgun configuration is incomplete")

        response = requests.post(
            f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
            auth=("api", MAILGUN_API_KEY),
            data={
                "from": f"Newsletter <mailgun@{MAILGUN_DOMAIN}>",
                "to": ["mxzadeh@gmail.com"],
                "subject": "New Newsletter Subscription",
                "text": f"New subscriber: {subscriber_email}"
            }
        )
        
        app.logger.info(f"Mailgun API response status: {response.status_code}")
        if response.status_code != 200:
            app.logger.error(f"Mailgun API error: {response.text}")
            
        return response
        
    except Exception as e:
        app.logger.error(f"Error in send_subscription_email: {str(e)}")
        raise

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/subscribe', methods=['POST'])
def subscribe():
    try:
        # Log the incoming request
        app.logger.info("Received subscription request")
        app.logger.info(f"Request form data: {request.form}")
        
        # Get email from form data instead of json
        email = request.form.get('email')
        
        if not email:
            app.logger.error("No email provided in request")
            return jsonify({
                "success": False,
                "message": "Email is required"
            }), 400

        # Send notification email
        app.logger.info(f"Sending subscription email for: {email}")
        response = send_subscription_email(email)

        if response.status_code == 200:
            app.logger.info("Subscription successful")
            return jsonify({
                "success": True,
                "message": "Thank you for subscribing to our newsletter!"
            })
        else:
            app.logger.error(f"Mailgun API error: {response.status_code}")
            return jsonify({
                "success": False,
                "message": "There was an error processing your subscription. Please try again later."
            }), 500

    except Exception as e:
        app.logger.error(f"Error in subscription: {str(e)}")
        return jsonify({
            "success": False,
            "message": "There was an error processing your subscription. Please try again later."
        }), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
