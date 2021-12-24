log4shell self-test
=================
log4shell self-test povides a platform allowing users to self-test their environment by pasting around payloads to try and trigger a DNS lookup.

It consists of a web, mysql and dns server in a dockerized environment to generate unique subdomains, catch and display when a callback was received.

Requirements
---------------
Make sure you point you delegate a subdomain as a name server by using the NS record. This is required to catch any DNS lookups executed by your payload, example:

```
ns.dnsexample.com. A <ip of your server>
log.dnsexample.com. NS ns.dnsexample.com.
```

Quick Start
---------------
Clone the master branch and modify the domainname of which you configured the above mentioned NS records in config.json.\
Optionally change the MySQL parameters in the docker-compose.yaml and config.json files.\
\
Run the containers via:

```
sudo docker-compose up
```

This will setup the webserver on port 8080 and a DNS server on TCP/UDP port 53.

Credits
---------------
Chen Zhaojun of Alibaba for discovering the vulnerability (CVE-2021-44228)
