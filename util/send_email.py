
from fastapi import FastAPI
import smtplib, os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv

load_dotenv()

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_MAIL = os.getenv("SMTP_MAIL")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

def send_mail(to, subject, body, attachment_path=None):
    msg = MIMEMultipart()
    msg['From'] = SMTP_MAIL
    msg['To'] = to
    msg['Subject'] = subject

    # Add HTML news message
    msg.attach(MIMEText(body, 'html'))

    # Attach file/image if provided
    # if attachment_path:
    #     with open(attachment_path, "rb") as file:
    #         part = MIMEBase('application', 'octet-stream')
    #         part.set_payload(file.read())
    #         encoders.encode_base64(part)
    #         part.add_header(
    #             'Content-Disposition',
    #             f'attachment; filename="{os.path.basename(attachment_path)}"'
    #         )
    #         msg.attach(part)

    # Send email
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(SMTP_MAIL, SMTP_PASSWORD)
    server.sendmail(SMTP_MAIL, to, msg.as_string())
    server.quit()

    return {"message": "Email sent successfully"}


# if __name__ == "__main__":
#     html_news_message = """
#     <h2>📰 Welcome to State-City News Portal</h2>
#     <p>Dear Reader,</p>
#     <img src="https://res.cloudinary.com/dmwmbomir/image/upload/v1745178043/ijkvzblo1uwg4awrji6p.jpg" alt="News Image" style="max-width: 100%; height: auto;" />

#     <p>Thank you for signing up with <strong>StateBuzz: State-City News</strong> – your go-to platform for reliable and real-time news updates from every state and city across India.</p>
    
#     <p>Here’s what you can expect:</p>
#     <ul>
#         <li>🌍 Local & National News</li>
#         <li>🗳️ Live Election Coverage</li>
#         <li>📸 Exclusive Reports with Images</li>
#         <li>📢 Citizen Journalism Features</li>
#     </ul>

#     <p>Attached is today’s top highlight. Stay informed and engaged!</p>
#     <br>
#     <p>Best regards,<br><em>StateBuzz: State-City News Team</em></p>
#     """

#     send_mail(
#         to="siffeciquoda-5946@yopmail.com",
#         subject="🗞️ Welcome! Here’s Today’s Top Highlight",
#         body=html_news_message,
#         attachment_path="/util/craft.png"  # Replace with your actual file like PDF or image
#     )


