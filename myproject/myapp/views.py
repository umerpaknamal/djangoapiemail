from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response

import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

import base64

@api_view(['POST'])
def concatenate_email(request):
    data = request.data
    email = data.get('email', '')
    to = data.get('to', '')
    subject = data.get('subject', '')
    sender = data.get('sender', '')
    
    concatenated_string = f"Email: {email}, To: {to}, Subject: {subject}, Sender: {sender}"

    
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = to
    msg['Subject'] = subject
    msg['MIME-Version'] = '1.0'
    msg['Content-Type'] = 'multipart/mixed; boundary=foo_bar_baz'

    # Add body text
    body_part = MIMEText(concatenated_string, 'plain', 'utf-8')
    msg.attach(body_part)

    # Add attachment
    attachment_base64 = data.get('attachment_base64', '')
    attachment_filename = data.get('attachment_filename', 'Attachment_file.png')

    attachment_part = MIMEBase('application', 'octet-stream')
    attachment_part.set_payload(base64.b64decode(attachment_base64))
    encoders.encode_base64(attachment_part)
    attachment_part.add_header('Content-Disposition', f'attachment; filename="{attachment_filename}"')
    msg.attach(attachment_part)

    # Convert the message to a string
    email_text = msg.as_string()
    
    
    return Response({'encoded_string': email_text})
