from flask import Flask 
from flask_mail import Mail, Message

app = Flask(__name__)


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'adebashisdas626@gmail.com'
app.config['MAIL_PASSWORD'] = 'nhnf ijme dryb cqhq'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)   # instance of the mail class

@app.route('/')
def index():
    try:
        msg = Message(
            'Hello',
            sender = 'adebashisdas626@gmail.com',
            recipients = ['adebashisdas626@gmail.com']
        )

        msg.body = 'Hello Flask message sent from Flask-Mail'
        mail.send(msg)
        return 'Message Sent'
    
    except Exception as e:
        return f'An error occurred while sending the email: {e}'

    
if __name__ == '__main__':
   app.run(debug = True)

