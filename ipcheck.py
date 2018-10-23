'''
22.10.2017
@author = Jan Wieczorek
@email: j.wieczorek34@gmail.com
Script checking external ip of the router and sends !WARNING email if IP changes.
'''
import datetime, os, re, smtplib, urllib, time

start_time = time.time()
#Check external ip of router
ext_ip = re.search('"([0-9.]*)"', urllib.urlopen("http://ip.jsontest.com/").read()).group(1)
#Check if file ext_ip.txt exists
ext_ip_exists = True if "ext_ip.txt" in os.listdir(".") else False
email = "" #Email addres to where send mail when external ip of router changes
sender = "" #First, give an addres of email server
os.chdir(".") #Change direcotry to current folder

if ext_ip_exists == False:
    f= open("ext_ip.txt","w+") #Write external IP to file if filenot existst
    f.write(ext_ip)
    f.close()

f2 = open("ext_ip.txt", "r") #Read external ip from the file
prev_ip = f2.read()
f2.close()

f= open("ext_ip.txt","w+") #Write external IP to file ext_ip.tx
f.write(ext_ip)
f.close()
print "External IP: " + ext_ip
print "Previous IP: " + prev_ip

if ext_ip == prev_ip:
    print "Ext IP the same as previous IP noticed."
else:
    print "External IP changed: " + prev_ip +  " -> " + ext_ip
    print "Sending email to: " + email
    exe_time = time.time() - start_time
    body = "External IP changed: " + prev_ip +  " -> " + ext_ip  +"\nScript execution time:" + str(exe_time) + " seconds."
    #Send the mail
    email_text = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (sender, email, "Ext IP of Raspberry changed", body)
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(sender, "")
        server.sendmail(sender, email, email_text)
        server.close()
        print 'Email sent!'
    except:
        print 'Something went wrong...'
