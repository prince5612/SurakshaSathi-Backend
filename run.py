# from app import create_app
# from flask_mail import Mail
# import os
# from dotenv import load_dotenv

# load_dotenv()

# app = create_app()

# # app.config.update(
# #     MAIL_SERVER='smtp.gmail.com',
# #     MAIL_PORT=587,
# #     MAIL_USE_TLS=True,
# #     MAIL_USERNAME=os.getenv('MAIL_USERNAME'),
# #     MAIL_PASSWORD=os.getenv('MAIL_PASSWORD'),
# #     MAIL_DEFAULT_SENDER=('SurakshaSathi', os.getenv('MAIL_USERNAME'))
# # )

# # mail = Mail(app)

# if __name__ == "__main__":
#     app.run(debug=True)

# run.py
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
