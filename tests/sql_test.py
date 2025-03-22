import mysql.connector

# mysql://root:qzRTZodSVLiKMWATQJWLWOgcThBxqaem@hopper.proxy.rlwy.net:43283/railway

def sql_test():
  conn = mysql.connector.connect(
    host="hopper.proxy.rlwy.net",
    user="root",
    password="qzRTZodSVLiKMWATQJWLWOgcThBxqaem",
    database="NahrimWaterDashboard",
    port=43283
  )

  cursor = conn.cursor()

  sql = """
SELECT * FROM Temperature_Data;
"""

  cursor.execute()

  for row in cursor:
    print(f"{row}")

  cursor.close()
  conn.close()

  return