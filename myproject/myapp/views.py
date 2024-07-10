from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import base64
import json
import google.auth
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


@api_view(['POST'])
def base64_view(request):
    try:
        data = json.loads(request.body)  # Ensure data is loaded as a dictionary
        if not isinstance(data, dict):
            return JsonResponse({'error': 'Invalid data format, expected a JSON object'}, status=400)
        
        base64_string = data.get('base64_string')
        if base64_string is None:
            return JsonResponse({'error': 'base64_string is required'}, status=400)

        # Process the base64_string
        return JsonResponse({'data': base64_string})
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)


@api_view(['POST'])
def concatenate_email(request):
    data = request.data
 
    access_token = data.get('access_token', '')
    thread_id = data.get('threadId', '')
    original_message_id = data.get('originalMessageId', '')
 
    to = data.get('to', [])
    sender = data.get('sender', '')
    bcc = data.get('bcc', [])
    cc = data.get('cc', [])
    subject = data.get('subject', '')
    message_text = data.get('message', '')
    encoded_attachments = data.get('encodedAttachments', [])
    attachment_names = data.get('attachmentname', [])
    attachment_types = data.get('attachmenttype', [])
 
    to_str = ", ".join(to) if isinstance(to, list) else to
    bcc_str = ", ".join(bcc) if isinstance(bcc, list) else bcc
    cc_str = ", ".join(cc) if isinstance(cc, list) else cc
 
    # Authenticate Gmail API
    credentials = Credentials(access_token)
    service = build('gmail', 'v1', credentials=credentials)
 
    try:
        # Create the email message
        message = MIMEMultipart()
        message['to'] = to_str
        message['from'] = sender
        message['subject'] = subject
 
        # Add In-Reply-To and References headers if replying
        if original_message_id:
            original_message = service.users().messages().get(userId='me', id=original_message_id).execute()
            reply_to = next((header['value'] for header in original_message['payload']['headers'] if header['name'] == 'Message-ID'), None)
            if reply_to:
                message['In-Reply-To'] = reply_to
                message['References'] = reply_to
 
        # Attach the message body
        msg = MIMEText(message_text, 'html')
        message.attach(msg)
 
        # Attach any attachments
        for attachment_data, name, type in zip(encoded_attachments, attachment_names, attachment_types):
            part = MIMEBase('application', type)
            part.set_payload(base64.urlsafe_b64decode(attachment_data))
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename="{name}.{type}"')
            message.attach(part)
 
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
 
        message_data = {
            'raw': raw_message
        }
        if thread_id:
            message_data['threadId'] = thread_id
 
        # Send the email
        sent_message = service.users().messages().send(userId='me', body=message_data).execute()
        message_id = sent_message['id']
        thread_id = sent_message['threadId']
        return Response({'messageId': message_id, 'threadId': thread_id})
 
    except Exception as e:
        return Response({'error': str(e)}, status=400)
