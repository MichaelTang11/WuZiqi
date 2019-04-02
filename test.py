from Methods.ConnectDB import cursor

cursor.execute("SELECT * FROM user WHERE user_id=1")
row=cursor.fetchone()
print(row["table_id"])