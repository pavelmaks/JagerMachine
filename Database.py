



#for i in range(0, 100):
#    curs.execute("INSERT INTO qrs VALUES ('testqrcode" + str(i) + "')")

#conn.commit()

"""
sql = "SELECT * FROM qrs WHERE qr=?"
curs.execute(sql, [("testqrcode66")])
print(len(curs.fetchall()))
print(curs.fetchall()) # or use fetchone()
"""

"""
print "\nEntire database contents:\n"
for row in curs.execute("SELECT * FROM temps"):
    print row

print "\nDatabase entries for the garage:\n"
for row in curs.execute("SELECT * FROM temps WHERE zone='garage'"):
    print row
"""
