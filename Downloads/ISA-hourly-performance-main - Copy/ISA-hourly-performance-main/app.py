"""
    Python script to calculate performances hourly and store data in Database

    PS: Automated LINUX cron job runs the script every minute
    Created: 16/02/2023
    Author: Othman Turki
    edit by: Ayman Ben Ismail
"""

import os
from pathlib import Path
import logging
import re  # RegEx
from datetime import datetime  # , timedelta
from time import sleep
import json
from mysql.connector import Error, connect

log_f = os.path.join(Path(__file__).resolve().parent, "log.txt")
logging.basicConfig(
    filename=log_f,
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def main():
    """Main function: for local scoping"""

    now = datetime.now()
    cur_time = now.strftime("%H:%M")

    try:
        with connect(
            host="127.0.0.1",
            user="root",  # root admin
            password="",  # DigiTex@2022
            database="db_isa",
        ) as conn:
            with conn.cursor() as cursor:
                schedule = getSchedule(cursor)

                if cur_time in schedule:
                    t_start = schedule[cur_time]["start"]
                    t_end = schedule[cur_time]["end"]
                    minutes = schedule[cur_time]["minutes"]
                    logging.info("Start of calculation")
                    calc_op_perf(cursor, t_start, t_end, minutes)
                    calc_group_perf(cursor, t_start, t_end, minutes)
                    logging.info("End of calculation")
                conn.commit()
                conn.close()

    except Error as con_err:
        logging.info(con_err)


def getSchedule(cursor):
    query = """
    SELECT * FROM `prod__work_schedule`
    """
    query = re.sub(r"\s+", " ", query.strip())
    cursor.execute(query)
    schedule = cursor.fetchall()
    scheduleJson = json.loads(schedule[0][1])
    now = datetime.now()
    week_day = int(now.strftime("%w"))

    schedule = {}

    if week_day in range(1, 6):  # Monday to Friday
        schedule = scheduleJson[0]
    elif week_day == 6:  # Saturday
        schedule = scheduleJson[1]
    return schedule


def calc_op_perf(cursor, t_start, t_end, minutes):
    logging.info("calculation of operator performance")
    calc_op_perf_query = f"""
        INSERT INTO prod__operator_perf_hr (operator,prod_line,performance,tot_qty,cur_date,cur_time)
        SELECT
            `operator`,
            GROUP_CONCAT(DISTINCT `prod_line` SEPARATOR '/') as prod_line,
           ROUND(((SUM(`unit_time` * `pack_qty`) / {minutes}) * 100), 2) AS performance,
           SUM(`pack_qty`) AS tot_qty,
           CURRENT_DATE,
           CURRENT_TIME
        FROM
            `prod__pack_operation`
        WHERE
            `cur_date` = CURRENT_DATE AND
            `cur_time` BETWEEN '{t_start}' AND '{t_end}'
        GROUP BY
            `operator`;
    """
    calc_op_perf_query = re.sub(r"\s+", " ", calc_op_perf_query.strip())
    # print(f"\n{calc_op_perf_query=}")

    cursor.execute(calc_op_perf_query)


def calc_group_perf(cursor, t_start, t_end, minutes):
    logging.info("calculation of group performance")
    calc_group_perf_query = f"""
        INSERT INTO prod__prod_line_perf_hr (prod_line,performance,cur_date,cur_time)
        SELECT 
        prod_line,
        ROUND(AVG (perf),2) AS prod_line_performance,
        CURRENT_DATE,
        CURRENT_TIME
        FROM (SELECT
                    `operator`,
                    `prod_line` ,
                    ROUND(((SUM(`unit_time` * `pack_qty`) / {minutes}) * 100), 2) AS perf
                FROM
                    `prod__pack_operation`
                WHERE
                    `cur_date` = CURRENT_DATE AND 
              		`cur_time` BETWEEN '{t_start}' AND '{t_end}'
                GROUP BY
                    `operator`,`prod_line`) T1
        GROUP BY prod_line;
    """
    calc_group_perf_query = re.sub(r"\s+", " ", calc_group_perf_query.strip())
    # print(f"\n{calc_group_perf_query=}")

    cursor.execute(calc_group_perf_query)


if __name__ == "__main__":
    # LOG
    # logging.info("Program Started")
    main()
    # while True:
    #     main()
    #     sleep(60)
