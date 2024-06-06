from rest_framework.decorators import api_view
from rest_framework.response import Response
import base64
import json
import google.auth
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
 
@api_view(['POST'])
def concatenate_email(request):
    data = request.data
 
    access_token = data.get('access_token', '')
    thread_id = data.get('threadId', '')
 
    to = data.get('to', [])
    sender = data.get('sender', '')
    bcc = data.get('bcc', [])
    cc = data.get('cc', [])
    subject = data.get('subject', '')
    message = data.get('message', '')
    encoded_attachments = data.get('encodedAttachments', [])
    attachment_name = data.get('attachmentname', [])
    attachment_type = data.get('attachmenttype', [])
 
    to_str = ", ".join(to) if isinstance(to, list) else to
    bcc_str = ", ".join(bcc) if isinstance(bcc, list) else bcc
    cc_str = ", ".join(cc) if isinstance(cc, list) else cc
 
    boundary = "boundary_string"
 
    str_parts = [
        "Content-Type: multipart/mixed; boundary=" + boundary + "\n",
        "MIME-Version: 1.0\n",
        "To: {}\n".format(to_str),
        "Bcc: {}\n".format(bcc_str),
        "Cc: {}\n".format(cc_str),
        "From: {}\n".format(sender),
        "Subject: {}\n\n".format(subject),
        "--" + boundary + "\n",
        "Content-Type: text/html; charset=\"UTF-8\"\n",
        "Content-Transfer-Encoding: 7bit\n\n",
        message, "\n",
    ]
 
    for attachment_data, attachment_name, attachment_type in zip(encoded_attachments, attachment_name, attachment_type):
        filename = attachment_name + "." + attachment_type
        str_parts.extend([
            "--" + boundary + "\n",
            "Content-Type: application/{}\n".format(attachment_type),
            "Content-Disposition: attachment; filename=\"{}\"\n".format(filename),
            "Content-Transfer-Encoding: base64\n\n",
            attachment_data, "\n",
        ])
 
    str_parts.append("--" + boundary + "--")
    email_body = "".join(str_parts)
    encoded_mail = base64.urlsafe_b64encode(email_body.encode()).decode()
 
    # Send the email using Gmail API
    credentials = Credentials(token=access_token)
    service = build('gmail', 'v1', credentials=credentials)
 
    message_data = {
        'raw': encoded_mail
    }
    if thread_id:
        message_data['threadId'] = thread_id
 
    try:
        message = service.users().messages().send(userId='me', body=message_data).execute()
        message_id = message['id']
        return Response({'messageId': message_id})
    except Exception as e:
        return Response({'error': str(e)}, status=400)
