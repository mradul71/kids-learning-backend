import os
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
if not __package__ or (__package__ and __package__[:3]!="app"):
    from config import DevelopmentConfig
else:
    from app.config import DevelopmentConfig

load_dotenv()

def send_email(to_emails: str, subject: str, content: str) -> tuple[bool,int]:
    message: Mail = Mail(
    	from_email='support@kidslearning.com',
	    to_emails=to_emails,
	    subject=subject,
	    html_content= content
	)		
    try:
        sg: SendGridAPIClient =SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response: str = sg.send(message)
        return True,response.status_code        
    except Exception as e:        
        return False,500

def send_signup_email(to_email: str, password: str) -> None:
    verification_link: str = DevelopmentConfig.AUTH.generate_email_verification_link(to_email)
    pass_reset_link: str = DevelopmentConfig.AUTH.generate_password_reset_link(to_email)
    subject: str = "kids learning Account Created"
    content: str = f"""<p>Your kids learning account creation was successful. Thanks!</p><br>
    <p>Verify Your email by clicking on this link : <a href={verification_link}>{verification_link}</a></p><br>
    <p>Current Password : {password} . Update password using think link: <a href={pass_reset_link}>{pass_reset_link}</a></p><br>
    <p>You account db setup is in process. YOU will be able login and create project but will not be able to create models until the stup is complete. YOu will notified via email once the setup is complete.</p><br>
    <p>Please go to the login page for sign-in onto the platform. url: <a href= "https://kids learningsolutions.com/auth/sign-in">https://kids learningsolutions.com/auth/sign-in</a></p><br>
    <p>Thanks,<br>
    <strong>kids learning Support</strong></p><p>In case of questions, please reach out to support@kidslearning.com</p>"""
    send_email(to_email, subject, content)
    return verification_link, pass_reset_link

def send_db_setup_completion_email(to_email: str) -> None:
    subject: str = "kids learning Organization Setup Completed"
    content: str = f"""<p>Your kids learning acount organization setup is complete.</p><br>
    <p>Please check admin section for created resources and to configure them.</p><br>
    <p>Please go to the login page for sign-in onto the platform. url: <a href= "https://kids learningsolutions.com/auth/sign-in">https://kids learningsolutions.com/auth/sign-in</a></p><br>
    <p>Thanks,<br>
    <strong>kids learning Support</strong></p><p>In case of questions, please reach out to support@kidslearning.com</p>"""
    send_email(to_email, subject, content)

def send_db_setup_fail_email(to_email: str) -> None:
    subject: str = "kids learning Organization Setup Failed"
    content: str = f"""<p>Your kids learning acount organization setup failed due to some error.</p><br>
    <p>Please check admin section to restart the setup process. Contact support in case of any querries.</p><br>`
    <p>Please go to the login page for sign-in onto the platform. url: <a href= "https://kids learningsolutions.com/auth/sign-in">https://kids learningsolutions.com/auth/sign-in</a></p><br>
    <p>Thanks,<br>
    <strong>kids learning Support</strong></p><p>In case of questions, please reach out to support@kidslearning.com</p>"""
    send_email(to_email, subject, content)

def send_db_modification_completion_email(to_email: str) -> None:
    subject: str = "kids learning Organization Database Modification Completed"
    content: str = f"""<p>Your kids learning acount organization databse modification is complete.</p><br>
    <p>Please check admin section for created resources and to configure them.</p><br>
    <p>Please go to the login page for sign-in onto the platform. url: <a href= "https://kids learningsolutions.com/auth/sign-in">https://kids learningsolutions.com/auth/sign-in</a></p><br>
    <p>Thanks,<br>
    <strong>kids learning Support</strong></p><p>In case of questions, please reach out to support@kidslearning.com</p>"""
    send_email(to_email, subject, content)

def send_db_modification_fail_email(to_email: str) -> None:
    subject: str = "kids learning Organization Database Modification Failed"
    content: str = f"""<p>Your kids learning acount organization databse modification failed due to some error.</p><br>
    <p>Please check admin section to restart the modification process. Contact support in case of any querries.</p><br>`
    <p>Please go to the login page for sign-in onto the platform. url: <a href= "https://kids learningsolutions.com/auth/sign-in">https://kids learningsolutions.com/auth/sign-in</a></p><br>
    <p>Thanks,<br>
    <strong>kids learning Support</strong></p><p>In case of questions, please reach out to support@kidslearning.com</p>"""
    send_email(to_email, subject, content)

def send_invitation_email(to_email: str, org_name: str, by_user_name: str, by_user_email: str, invitation_link: str) -> None:
    subject: str = f"{org_name} Organization Invitation | kids learning"
    content: str = f"""<p>You have been invited to join '{org_name}' Organization by {by_user_name}({by_user_email}). Thanks!</p><br>
    <p>Accept invitation by clicking on this link : <a href={invitation_link}>{invitation_link}</a></p><br>
    <p>Please go to the login page for sign-in onto the platform. url: <a href= "https://kids learningsolutions.com/auth/sign-in">https://kids learningsolutions.com/auth/sign-in </a></p><br>
    <p>Thanks,<br>
    <strong>kids learning Support</strong></p><p>In case of questions, please reach out to support@kidslearning.com</p>"""
    send_email(to_email, subject, content)

def send_invitation_acceptance_email(to_email: str, org_name: str, accepted_user: str) -> None:
    subject: str = f"{org_name} Organization Invitation Acceptance | kids learning"
    content: str = f"""<p>'{accepted_user}' has accepted your invitation to Organization: {org_name}.</p><br>
    <p>If not invited by you please check user-management section of the mentioned organization on the platform. url: <a href= "https://kids learningsolutions.com/admin/user-management">https://kids learningsolutions.com/admin/user-management </a></p><br>
    <p>Thanks,<br>
    <strong>kids learning Support</strong></p><p>In case of questions, please reach out to support@kidslearning.com</p>"""
    send_email(to_email, subject, content)

def send_invitation_rejection_email(to_email: str, org_name: str, rejected_user: str) -> None:
    subject: str = f"{org_name} Organization Invitation Rejection | kids learning"
    content: str = f"""<p>'{rejected_user}' has rejected your invitation to Organization: {org_name}.</p><br>
    <p>If not invited by you please check user-management section of the mentioned organization on the platform. url: <a href= "https://kids learningsolutions.com/admin/user-management">https://kids learningsolutions.com/admin/user-management </a></p><br>
    <p>Thanks,<br>
    <strong>kids learning Support</strong></p><p>In case of questions, please reach out to support@kidslearning.com</p>"""
    send_email(to_email, subject, content)

def send_verification_email(to_email: str) -> None:
    verification_link: str = DevelopmentConfig.AUTH.generate_email_verification_link(to_email)
    subject: str = "kids learning Email Verification"
    content: str = f"""<p>Verify Your email by clicking on this link : <a href={verification_link}>{verification_link}</a></p><br>
    <p>Please go to the login page for sign-in onto the platform. url: <a href="https://kids learningsolutions.com/auth/sign-in">https://kids learningsolutions.com/auth/sign-in </a></p><br>
    <p>Thanks,<br>
    <strong>kids learning Support</strong></p><p>In case of questions, please reach out to support@kidslearning.com</p>"""
    send_email(to_email, subject, content)

def send_password_reset_email(to_email: str) -> str:
    pass_reset_link: str = DevelopmentConfig.AUTH.generate_password_reset_link(to_email)
    return pass_reset_link
    # subject: str = "kids learning Password Change"
    # content: str = f"""<p>Update password using think link : <a href={pass_reset_link}>{pass_reset_link}</a></p><br>
    # <p>Please go to the login page for sign-in onto the platform. url: <a href="https://kids learningsolutions.com/auth/sign-in">https://kids learningsolutions.com/auth/sign-in </a></p><br>
    # <p>Thanks,<br>
    # <strong>kids learning Support</strong></p><p>In case of questions, please reach out to support@kidslearning.com</p>"""
    # send_email(to_email, subject, content)