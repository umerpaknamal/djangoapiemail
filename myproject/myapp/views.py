from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
import base64

@api_view(['POST'])
def concatenate_email(request):
        data = request.data
        email = data.get('email', '')
        to = data.get('to', '')
        subject = data.get('subject', '')
        sender = data.get('sender', '')
        encodedAttachments = data.get('encodedAttachments', [])
        attachmentname=data.get('attachmentname',[])
        attachmenttype=data.get('attachmenttype',[])

        boundary = "boundary_string"
    
        str_parts = [
                "Content-Type: multipart/mixed; boundary=" + boundary + "\n",
                "MIME-Version: 1.0\n",
                "to: {}\n".format(to),
                "from: {}\n".format(sender),
                "subject: {}\n\n".format(subject),
                "--" + boundary + "\n",
                "Content-Type: text/plain; charset=\"UTF-8\"\n",
                "Content-Transfer-Encoding: 7bit\n\n",
                email, "\n",
            ]

    # Add attachment parts
    # Add attachment parts
        for attachment_data, attachment_name, attachment_type in zip(encodedAttachments, attachmentname, attachmenttype):
            filename = attachment_name + "." + attachment_type  # Concatenate name and type
            str_parts.extend([
            "--" + boundary + "\n",
            "Content-Type: Application\{}\n".format(attachment_type),  
            "Content-Disposition: attachment; filename=\"{}\"\n".format(filename),
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
