import os
import sys
import smtplib
from email.mime.text import MIMEText

class EmailClient(object):
  @staticmethod
  def send(recipient_email, subject, body):
    sender_address = 'email@xingyibo.com'
    sender_password = '13513515268'

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From']    = sender_address
    msg['To']      = ", ".join(recipient_email)

    succeed = False
    while not succeed:
      try:
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(sender_address, sender_password)
        s.sendmail(sender_address, recipient_email, msg.as_string())
        s.quit()
        succeed = True
      except Exception as e:
        continue

