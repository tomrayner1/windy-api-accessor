import mysql.connector


def sql_test():
  conn = mysql.connector.connect(
    host="hopper.proxy.rlwy.net",
    user="root",
    password="zRTZodSVLiKMWATQJWLWOgcThBxqaem",
    database="NahrimWaterDashboard",
    port=43283
  )

  cursor = conn.cursor()

  cursor.close()
  conn.close()

  return