from flask import Flask
from flask_mail import Mail, Message
from flask_restful import Api, Resource
import config
app = Flask(__name__)
api = Api(app)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = config.MAIL_USERNAME
app.config['MAIL_PASSWORD'] = config.MAIL_PASSWORD
mail = Mail(app)


class Mail_api(Resource):
    def get(self):
        msg = Message("MAIL API", sender=config.MAIL_USERNAME, recipients=config.MAIL_USERNAME)
        msg.body = "This is the email body"
        mail.send(msg)
        return "Sent"


api.add_resource(Mail_api, '/mailapp')
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
