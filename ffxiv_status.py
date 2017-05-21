# cat ffxiv_status.py
#!/usr/bin/python3
import urllib.request
import argparse
import smtplib

#× Excalibur
#http://na.finalfantasyxiv.com/lodestone/news/detail/80cd4583bf743600105b947d6906d0909189e479

def is_server_open(url, server):
        page = urllib.request.urlopen(url)
        data = page.read()
        for line in data.decode().split('\n'):
                if server.upper() in line.upper():
                        if '○' in line.upper():
                                return True
                        else:
                                return False
        return False

def send_email(recipient, smtp_server, port, username, password, subject, body):
        server = smtplib.SMTP(smtp_server, port)
        server.ehlo()
        server.starttls()
        server.login(username, password)
        email_data = '\r\n'.join(['To: %s' % recipient,
                'From: %s' % username,
                'Subject: %s' % subject,
                '', body])
        try:
                server.sendmail(username, [recipient], email_data)
                print("Email Sent")
        except Exception as ex:
                print("Failed to send email: ", ex)
        finally:
                server.quit()


if __name__ == "__main__":
        parser = argparse.ArgumentParser(description='Check if FFXIV Server is accepting new character creation')
        parser.add_argument('--server', metavar='-s', type=str, help='Server name (ie. Excalibur)')
        parser.add_argument('--url', metavar='-u', type=str, help='URL of FFXIV Lodestone news page showing character creation status')
        parser.add_argument('--smtp_server', metavar='-m', type=str, help='SMTP Server (ie. smtp.gmail.com)')
        parser.add_argument('--smtp_port', metavar='-p', type=int, help='SMTP Server Port (ie. 587)')
        parser.add_argument('--username', metavar='-n', type=str, help='SMTP Username login')
        parser.add_argument('--password', metavar='-w', type=str, help='SMTP Password login')
        parser.add_argument('--recipient', metavar='-r', type=str, help='Who is getting the email?')

        email_only_variables = ('smtp_server', 'smtp_port', 'username', 'password', 'recipient')
        args = vars(parser.parse_args())
        url = 'http://na.finalfantasyxiv.com/lodestone/news/detail/80cd4583bf743600105b947d6906d0909189e479'
        server = 'Excalibur'
        if args['server']:
                server = args['server']
        if args['url']:
                url = args['url']
        is_open = is_server_open(url, server)
        if is_open:
                info = "Server '%s' is open for character creation!" % server
                print(info)
                if all(k in args for k in email_only_variables):
                        print("Sending email...")
                        send_email(args['recipient'], args['smtp_server'], args['smtp_port'], args['username'], args['password'], info, info)
                        print("Done sending email...")
        else:
                info = "Server '%s' is closed for character creation ;(" % server
                print(info)
                #print("Sending email...")
                #send_email(args['recipient'], args['smtp_server'], args['smtp_port'], args['username'], args['password'], info, info)
                #print("Done sending email...")