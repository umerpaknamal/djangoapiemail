from rest_framework.decorators import api_view
from rest_framework.response import Response
import base64
 
@api_view(['POST'])
def concatenate_email(request):
    data = request.data
    files = request.FILES  # Access uploaded files
 
    to = data.get('to', [])
    sender = data.get('sender', '')
    bcc = data.get('bcc', [])
    cc = data.get('cc', [])
    subject = data.get('subject', '')
    message = data.get('message', '')
 
    # Ensure that to, bcc, and cc are properly formatted as comma-separated strings
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
 
    # Add attachment parts
    for file_key in files:
        file = files[file_key]
        attachment_data = base64.b64encode(file.read()).decode()
        attachment_name = file.name
        attachment_type = file.content_type.split('/')[-1]  # Get the file type (e.g., 'pdf', 'jpeg')
 
        str_parts.extend([
            "--" + boundary + "\n",
            "Content-Type: application/{}\n".format(attachment_type),
            "Content-Disposition: attachment; filename=\"{}\"\n".format(attachment_name),
            "Content-Transfer-Encoding: base64\n\n",
            attachment_data, "\n",
        ])
 
    # End the MIME structure
    str_parts.append("--" + boundary + "--")
 
    # Join the parts to form the complete email body
    email_body = "".join(str_parts)
 
    # Encode the entire email body to base64
    encodedMail = base64.b64encode(email_body.encode()).decode()
 
    return Response({'encoded_string': encodedMail})
