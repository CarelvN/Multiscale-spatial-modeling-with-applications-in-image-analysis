import smtplib

def SendNotification(email):
	frm = 'runningcode17@gmail.com'
	pswr = "MyCode17"
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(frm, pswr)
	body = "Subject: Your Code is finished running"
	server.sendmail(frm, 'cvnbul@gmail.com', body)
	server.quit()