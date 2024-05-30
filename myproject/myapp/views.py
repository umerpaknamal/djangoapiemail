[9:07 PM] Muhammad Kamran
from rest_framework.decorators import api_view
from rest_framework.response import Response
import base64
 
@api_view(['POST'])
def concatenate_email(request):
    data = request.data
 
    to = data.get('to', [])
    sender = data.get('sender', '')
    bcc = data.get('bcc', [])
    cc = data.get('cc', [])
    subject = data.get('subject', '')
    message = data.get('message', '')
    attachment_data = data.get('attachment_data', '')  # Binary data
    attachment_name = data.get('attachment_name', 'attachment')  # Default name if not provided
    attachment_type = data.get('attachment_type', 'octet-stream')  # Default type if not provided
 
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
 
    # Convert the binary data to base64
    base64_encoded_data = base64.b64encode(attachment_data.encode()).decode()
 
    str_parts.extend([
        "--" + boundary + "\n",
        "Content-Type: application/{}\n".format(attachment_type),
        "Content-Disposition: attachment; filename=\"{}\"\n".format(attachment_name),
        "Content-Transfer-Encoding: base64\n\n",
        base64_encoded_data, "\n",
    ])
 
    # End the MIME structure
    str_parts.append("--" + boundary + "--")
 
    # Join the parts to form the complete email body
    email_body = "".join(str_parts)
 
    # Encode the entire email body to base64
    encodedMail = base64.b64encode(email_body.encode()).decode()
 
    return Response({'encoded_string': encodedMail})
 
