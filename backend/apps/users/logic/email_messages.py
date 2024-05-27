email_messages = {
    "verify_email":
        {
         "message": "f'''You're receiving this email because "
                    "you need to finish activation process on {domain}."
                    "\n\nPlease go to the following page to activate "
                    "account:\nhttp://{domain}{uri}'''",
         "subject": "f'Verify your email on {domain}'",
         "uri": "f'/me/verify_email/{token}/'"
         },
    "forgot_password":
        {
         "message": "f'''We've got request about changing your password.\n\n"
                    "Please go to the following page to change it:\n"
                    "http://{domain}{uri}'''",
         "subject": "f'Change your password on {domain}'",
         "uri": "f'/me/change_password/{token}/'"
        }
                }
