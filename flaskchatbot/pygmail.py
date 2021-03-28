import smtplib

def sendEmail( mailto, date, time, name, report ):
    gmailaddress = "EMAIL_ID"
    gmailpassword = "PASSWORD"
    
    sub = "Successful login"
    if (len(report) == 0): report = "Checkup"
    msag = "Hey " + name + ",\n\nYour survey is sucessfully completed" + doctor + "\n\nDate : " + date + "\nTime : " + time + "\nProblem : " + report + "\n\nThank you for using Logistic Chatbot."
    msg = 'Subject: {}\n\n{}'.format(sub, msag)
    
    sub2 = "Survey done on "+ date
    msag2 = "User Email: "+ mailto + "\n\nReport: " + report
    msg2 = 'Subject: {}\n\n{}'.format(sub2, msag2)
    
    mailServer = smtplib.SMTP('smtp.gmail.com' , 587)
    mailServer.starttls()
    mailServer.login(gmailaddress , gmailpassword)
    mailServer.sendmail(gmailaddress, mailto , msg)
    print("--------------------\nUser Email Sent!\n--------------------")
    mailServer.sendmail(gmailaddress, gmailaddress , msg2)
    print("\n--------------------\nAdmin Email Sent!\n--------------------")
    mailServer.quit()
    return

# Turn ON/OFF
# https://myaccount.google.com/lesssecureapps
# Check Spam Folder if message not delivered
