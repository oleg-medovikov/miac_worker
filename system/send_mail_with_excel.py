import smtplib
from email.message import EmailMessage

from clas import Dir



def send_mail_with_excel(
        recipient_email: str,
        subject: str,
        content: str,
        excel_file: str
        ):
    "отправляем отчёт почтой"

    SENDER_EMAIL = Dir.get('SENDER_EMAIL')

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = SENDER_EMAIL
    msg['To'] = recipient_email
    msg.set_content(content)

    with open(excel_file, 'rb') as f:
        file_data = f.read()

    msg.add_attachment(
            file_data,
            maintype="application",
            subtype="pdf",
            filename=excel_file
            )

    with smtplib.SMTP(Dir.get('MIAC_MAIL'), 587) as smtp:
        smtp.send_message(msg)
