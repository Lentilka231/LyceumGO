import smtplib,ssl 

EMAIL_ADDRESS = "lyceumgo@gmail.com"
EMAIL_PASS = "Radim23147"

context = ssl.create_default_context()
def SendMail(EmailAddress,UserName,Message):
    KindOfAddress = EmailAddress[EmailAddress.find("@")+1:]
    with smtplib.SMTP_SSL(f"smtp.gmail.com",465,context=context) as smtp:
        smtp.login(EMAIL_ADDRESS,"jlsycsgpdgyrfumr")
        print(f"sending mail to {EmailAddress}")
        if Message=="Welcome":
            subject = "Vitej mezi lyceany"
            body = "Vitame te na te nejvice wierd komunite jmenem LyceumGO."
        msg= f'Subject: {subject}\n\n{body}'
        smtp.sendmail(EMAIL_ADDRESS,EmailAddress,msg)
        smtp.quit()