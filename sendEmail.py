#this is a slightly adapted version of a file the code I found at...
#https://www.geeksforgeeks.org/send-mail-attachment-gmail-account-using-python/

#my version deletes the file after copying and adds timestamp to body
import os
import smtplib
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 
import datetime

#make sure you have low security app acces enabled on your fromaddr google acc
#you also need to have 2 factor authen disabled on the fromaddr

toaddr = "xyz@gmail.com"
fromaddr = "xyz@gmail.com"
   
#instance of MIMEMultipart 
msg = MIMEMultipart() 
  
#storing the senders email address   
msg['From'] = fromaddr 
  
#storing the receivers email address  
msg['To'] = toaddr 
  
#storing the subject  
msg['Subject'] = "Disturbance"
  
#string to store the body of the mail 
body = str(datetime.datetime.now().strftime("%A, %B %d, %Y %I:%M:%p"))
  
#attach the body with the msg instance 
msg.attach(MIMEText(body, 'plain')) 
  
#open the file to be sent  
filename = "clip.avi"
attachment = open("clip.avi", "rb") 
  
#instance of MIMEBase and named as p 
p = MIMEBase('application', 'octet-stream') 
  
#To change the payload into encoded form 
p.set_payload((attachment).read())

#delete File
os.remove("clip.avi")
  
#encode into base64 
encoders.encode_base64(p) 
   
p.add_header('Content-Disposition', "attachment; filename= %s" % filename) 
  
#attach the instance 'p' to instance 'msg' 
msg.attach(p) 
  
#creates SMTP session 
s = smtplib.SMTP('smtp.gmail.com', 587) 
  
#start TLS for security 
s.starttls() 
  
#Authentication 
s.login(fromaddr, "password1234") 
  
#Converts the Multipart msg into a string 
text = msg.as_string() 
  
#sending the mail 
s.sendmail(fromaddr, toaddr, text)

  
# terminating the session 
s.quit() 