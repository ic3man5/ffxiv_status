# cat ffxiv_status.py
#!/usr/bin/python3
import urllib.request
import argparse
import smtplib
from bs4 import BeautifulSoup
import re

#× Excalibur
# Old:
#http://na.finalfantasyxiv.com/lodestone/news/detail/80cd4583bf743600105b947d6906d0909189e479
# New:
#https://na.finalfantasyxiv.com/lodestone/worldstatus/


def is_server_open(url, server):  
    page = urllib.request.urlopen(url)
    data = page.read()
    soup = BeautifulSoup(data, 'html.parser')
    server_divs = soup.find_all('div', attrs={'class':'world-list__item'})
    reg_exp_match = re.compile('world-ic__.*available js__tooltip')
    for server_div in server_divs:
        if server.upper() not in server_div.text.upper():
            continue
        i_class = server_div.find('i', reg_exp_match)#, attrs={'class':'world-ic__available js__tooltip'})
        #print(i_class)
        if 'Creation of New Characters Available'.upper() == i_class['data-tooltip'].upper():
            return True
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
        parser.add_argument('--email', metavar='-e', type=bool, help="Send an email")
        parser.add_argument('--nopause', metavar='-e', type=bool, help='Don\'t Pause at the end')

        email_only_variables = ('smtp_server', 'smtp_port', 'username', 'password', 'recipient')
        args = vars(parser.parse_args())
        url = 'https://na.finalfantasyxiv.com/lodestone/worldstatus/'
        no_pause = False
        dont_send_email = True
        server = 'Excalibur'
        if args['server']:
                server = args['server']
        if args['nopause']:
                no_pause = args['nopause']
        if args['email']:
                dont_send_email = args['email']
        if args['url']:
                url = args['url']
        is_open = is_server_open(url, server)
        if is_open:
                info = "Server '%s' is open for character creation!" % server
                print(info)
                if not dont_send_email:
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
        if not no_pause:
            input("Press any key to continue...")