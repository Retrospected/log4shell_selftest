#!/usr/bin/python
import socket
from dnslib import DNSRecord

from database.database import database

import re

host = ''
port = 53
size = 512
dbfile = "./database/dns.db"

def log(entry):
    print("[DNS] DNS question received: "+entry)
    db.parse_entry(entry)


if __name__ == "__main__":
    print("[MAIN] DNS Server Started")

    db = database(dbfile)

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host, port))
    while True:
        try:
            data, addr = s.recvfrom(size)
            d = DNSRecord.parse(data)
        
            for question in d.questions:
               log(re.findall(r"^;(.*)\..*$", str(question))[0])
        except Exception as e:
            print(e)
