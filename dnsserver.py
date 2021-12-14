#!/usr/bin/python
import socket
from dnslib import *

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
            real_question = ""
            for question in d.questions:
               real_question = re.findall(r"^;(.*)\..*$", str(question))[0]
               log(real_question)

            q = DNSRecord(DNSHeader(id=d.header.id, qr=1, aa=1, ra=1), q=d.q)
            reply = q.reply()

            reply.add_answer(RR(real_question, QTYPE.A,rdata=A("127.0.0.1"),ttl=0))

            response_packet = reply.pack()

            s.sendto(response_packet, addr)

        except Exception as e:
            print(e)
