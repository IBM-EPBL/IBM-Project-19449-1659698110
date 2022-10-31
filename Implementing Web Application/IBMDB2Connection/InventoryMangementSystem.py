from flask import Flask
import ibm_db

conn = ibm_db.connect("DATABASE=bludb;HOSTNAME = b0aebb68-94fa-46ec-a1fc-1c999edb6187.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;PORT = 31249;SECURITY = SSL;SSLSererCertificate = DigiCertGlobalRootCA.crt;UID = rnj93429;PWD = kzoIIKcwZ05e4tyW","","")

sql = "SELECT * FROM STOREDETAILS"

stmt = ibm_db.exec_immediate(conn,sql)

dictionary = ibm_db.fetch_assoc(stmt)

print(dictionary)