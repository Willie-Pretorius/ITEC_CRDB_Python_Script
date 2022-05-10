import datetime
import smtplib,ssl
#adds input text to .log file.
def addLog(input):
    time = datetime.datetime.now()
    try:
        with open("logs.txt","a") as file:
            file.writelines(f"{time}:{input}")
            file.close()
    except:
        print("couldn't save to log file.")

#takes in a subject and a body and sends an email to the configured address in .smtpconfig
def sendEmail(subject,body):
    options = []
    try:
        with open(".smtpconfig", "r") as file:
            text = file.read()
            text = text.replace(" ", "")
            lines = text.split("\n")
            for line in lines:
                options.append(line.split(":")[1])
        smtp_server = options[0]
        from_address = options[1]
        username = options[2]
        password = options[3]
        to_address = options[4]
    except:
        print("Email notification failed. Check SMTP settings.\n")
        addLog("Email notification failed. Check SMTP settings.\n")
    try:
        context = ssl.create_default_context()
        connection = smtplib.SMTP(smtp_server)
        connection.starttls(context=context)
    except:
        print("Smtp connection failed")
    try:
        connection.login(user=username,password=password)
    except:
        print("Login failed.")
    try:
        connection.sendmail(from_addr=from_address,to_addrs=to_address,msg=f"{subject}\n\n{body}")
        print("Send email sent successfully.")
        connection.close()
    except:
        print("Send email failed.")

#This code was written by Willie Pretorius
#Fork me at https://github.com/Willie-Pretorius
