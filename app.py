from flask import Flask, render_template, request, jsonify
import os
import requests
from database import db

app = Flask(__name__, static_url_path='/static')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///blog.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the app with the extension
db.init_app(app)

def send_subscription_email(subscriber_email):
    MAILGUN_DOMAIN = os.environ.get('MAILGUN_DOMAIN')
    MAILGUN_API_KEY = os.environ.get('MAILGUN_API_KEY')

    return requests.post(
        f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
        auth=("api", MAILGUN_API_KEY),
        data={"from": f"Newsletter <mailgun@{MAILGUN_DOMAIN}>",
              "to": ["mxzadeh@gmail.com"],
              "subject": "New Newsletter Subscription",
              "text": f"New subscriber: {subscriber_email}"})

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/subscribe', methods=['POST'])
def subscribe():
    try:
        email = request.json.get('email')
        if not email:
            return jsonify({"success": False, "message": "Email is required"}), 400

        # Send notification email
        response = send_subscription_email(email)

        if response.status_code == 200:
            return jsonify({
                "success": True,
                "message": "Thank you for subscribing to our newsletter!"
            })
        else:
            return jsonify({
                "success": False,
                "message": "There was an error processing your subscription. Please try again later."
            }), 500

    except Exception as e:
        print(f"Error in subscription: {str(e)}")
        return jsonify({
            "success": False,
            "message": "There was an error processing your subscription. Please try again later."
        }), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)