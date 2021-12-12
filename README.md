log4shell self-test
=================
log4shell self-test povides a platform allowing users to self-test their environment by pasting around payloads to try and trigger a DNS lookup.

It consists of a webserver and dns server (started seperately) to generate payloads and catch hits.

Requirements
---------------
Make sure you point you delegate a subdomain as a name server by using the NS record. This is required to catch any DNS lookups executed by your payload, example:

```
ns.dnsexample.com. A <ip of your server>
log4shell.dnsexample.com. NS ns.dnsexample.com.
```

Additionally this tool requires TLS certificates in order to be used, use LetsEncrypt and provide your "/etc/letsencrypt/live/\<domain\>/" path.

Quick Start
---------------
Clone the master branch, install the requirements and run.

```
git clone https://github.com/Retrospected/log4shell_selftest; cd log4shell_selftest
sudo pip3 install -r requirements.txt
sudo python3 webserver.py <domain of dns server> <path with TLS files>
sudo python3 dnsserver.py
```

Default webserver port: 8443

Credits
---------------
Chen Zhaojun of Alibaba for discovering the vulnerability (CVE-2021-44228)

