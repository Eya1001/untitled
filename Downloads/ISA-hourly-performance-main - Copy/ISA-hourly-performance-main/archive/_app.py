# """
#     PYTHON APP(/SCRIPT) TO CALCULATE PERFORMANCES HOURLY AND STORE DATA IN
#     DATABASE
# """

# import logging
# import time
# from datetime import datetime

# from mysql.connector import Error, connect

# logging.basicConfig(
#     filename="log.txt", level=logging.DEBUG, format="%(asctime)s %(message)s"
# )

# triggers = {
#     "08:30": {"start": "07:30:00", "end": "08:29:59", "work_time": "60"},
#     "09:30": {"start": "08:30:00", "end": "09:29:59", "work_time": "60"},
#     "10:30": {"start": "09:30:00", "end": "10:29:59", "work_time": "60"},
#     "11:30": {"start": "10:30:00", "end": "11:29:59", "work_time": "60"},
#     "11:50": {"start": "11:30:00", "end": "11:50:00", "work_time": "20"},
#     "13:30": {"start": "12:30:00", "end": "13:29:59", "work_time": "60"},
#     "14:30": {"start": "13:30:00", "end": "14:29:59", "work_time": "60"},
#     "15:30": {"start": "14:30:00", "end": "15:29:59", "work_time": "60"},
#     "16:58": {"start": "15:30:00", "end": "16:29:59", "work_time": "60"},
#     "17:10": {"start": "16:30:00", "end": "17:10:00", "work_time": "40"},
# }


# def main():
#     """MAIN FUNCTION: FOR LOCAL SCOPING"""
#     logging.info("Program Started")

#     while True:
#         now = datetime.now()
#         cur_day = now.strftime("%d/%m/%Y")
#         cur_time = now.strftime("%H:%M")

#         if cur_time in triggers:
#             try:
#                 with connect(
#                     host="localhost",
#                     user="ISA",  # ETC
#                     password="SmarTex2021",  # SmarTex2021
#                     database="db_isa",
#                 ) as conn:
#                     print("Connection to DB succeeded!")
#                     select_query = (
#                         """
#                         SELECT
#                             registration_number,
#                             Firstname,
#                             Lastname,
#                             ROUND(SUM((quantity * tps_ope_uni)) / """
#                         + triggers[cur_time]["work_time"]
#                         + """, 2) AS performance
#                         FROM
#                             `pack_operation`
#                         WHERE
#                             cur_day = '"""
#                         + cur_day
#                         + """' AND cur_time BETWEEN '"""
#                         + triggers[cur_time]["start"]
#                         + """' AND '"""
#                         + triggers[cur_time]["end"]
#                         + """'
#                         GROUP BY
#                             registration_number;
#                     """
#                     )
#                     insert_query = """
#                         INSERT INTO performance_per_hour
#                         (registration_number, first_name,
#                         last_name, performance, cur_day, cur_time)
#                         VALUES (%s, %s, %s, %s, %s, %s)
#                     """

#                     with conn.cursor() as cursor:
#                         cursor.execute(select_query)
#                         results = cursor.fetchall()

#                         if len(results) > 0:
#                             insert_records = [
#                                 (
#                                     result[0],
#                                     result[1],
#                                     result[2],
#                                     result[3],
#                                     cur_day,
#                                     cur_time,
#                                 )
#                                 for result in results
#                             ]
#                             cursor.executemany(insert_query, insert_records)
#                             conn.commit()
#                             conn.close()

#                             logging.info(
#                                 "Performance of operators calculated
#                                  successfully"
#                             )

#                         else:
#                             logging.info("No Performance of operators exist")

#             except Error as msg_err:
#                 logging.error("DB Error: %s", msg_err)

#         print(cur_day, cur_time)
#         time.sleep(60)


# if __name__ == "__main__":
#     try:
#         main()

#     except KeyboardInterrupt:
#         logging.error("Keyboard Interrupt")

#     except Exception as err:
#         logging.error("Crashing Error: %s", err)
#         # logging.error("Error Type: %s", type(err).__name__)
