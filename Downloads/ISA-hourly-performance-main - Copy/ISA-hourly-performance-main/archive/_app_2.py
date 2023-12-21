"""
    Python script to calculate performances hourly and store data in Database
    - Step 1: Calculate operators performance
    - Step 2: Calculate groups performance

    PS: Automated LINUX cron job runs the script every minute
    Created: 16/02/2023
    Author: Othman Turki
"""

# import logging
import re  # RegEx
from datetime import datetime  # , timedelta

from mysql.connector import Error, connect

# logging.basicConfig(
#     filename="log.txt",
#     level=logging.DEBUG,
#     format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
# )


triggers = {
    "08:30": {"start": "07:30:00", "end": "08:30:00", "minutes": 60},
    "09:30": {"start": "07:30:00", "end": "09:30:00", "minutes": 120},
    "10:30": {"start": "07:30:00", "end": "10:30:00", "minutes": 180},
    "11:30": {"start": "07:30:00", "end": "11:30:00", "minutes": 240},
    "11:50": {"start": "07:30:00", "end": "11:50:00", "minutes": 260},
    "13:30": {"start": "07:30:00", "end": "13:30:00", "minutes": 320},
    "14:30": {"start": "07:30:00", "end": "14:30:00", "minutes": 380},
    "15:30": {"start": "07:30:00", "end": "15:30:00", "minutes": 440},
    "16:30": {"start": "07:30:00", "end": "16:30:00", "minutes": 500},
    "17:10": {"start": "07:30:00", "end": "17:10:00", "minutes": 540},
}


def main():
    """MAIN FUNCTION: FOR LOCAL SCOPING"""

    now = datetime.now()
    trigger = now.strftime("%H:%M")
    cur_date = now.strftime("%d/%m/%Y")

    # DEBUG:
    trigger = "17:10"
    # cur_date = (now.today() + timedelta(days=-1)).strftime("%d/%m/%Y")
    # print(f"{cur_date=}")
    # @prod_line:=REPLACE(REPLACE(`prod_line`, '\r\n', ''), '\n', '')
    # TRIM(TRAILING '\r' FROM `prod_line`)

    if trigger in triggers:
        try:
            with connect(
                host="127.0.0.1",
                user="root",  # admin
                password="",  # DigiTex@2022
                database="db_isa",
            ) as conn:
                # print("Successful database connection")
                t_start = triggers[trigger]["start"]
                t_end = triggers[trigger]["end"]
                mins = triggers[trigger]["minutes"]

                calc_op_perf = f"""
                    SELECT
                        `operator_reg_num`,
                        `prod_line`,
                        ROUND(
                            ((SUM(`unit_time` * `pack_qte`) / {mins}) * 100), 2
                        )
                    FROM
                        `p4_pack_operation`
                    WHERE
                        `cur_date` = '{cur_date}' AND
                        `cur_time`
                            BETWEEN '{t_start}' AND
                                '{t_end}'
                    GROUP BY
                        `operator_reg_num`;
                """
                calc_op_perf = re.sub(r"\s+", " ", calc_op_perf.strip())
                # print(f"\n{calc_op_perf=}")

                store_op_perf = """
                    INSERT INTO `p8_op_performance_h` (
                        `operator_reg_num`,
                        `prod_line`,
                        `performance`,
                        `cur_date`,
                        `cur_time`
                    )
                    VALUES (%s, %s, %s, %s, %s);
                """
                store_op_perf = re.sub(r"\s+", " ", store_op_perf.strip())
                # print(f"\n{store_op_perf=}")

                with conn.cursor() as cursor:
                    cursor.execute(calc_op_perf)
                    results = cursor.fetchall()

                    if len(results) == 0:
                        print("There is no operator performance")
                        return

                    cleaned_res = [
                        [x.strip() if isinstance(x, str) else x for x in row]
                        for row in results
                    ]
                    # print(f"\n{cleaned_res=}")
                    op_perf_records = [
                        (
                            record[0],
                            record[1],
                            record[2],
                            cur_date,
                            t_end,
                        )
                        for record in cleaned_res
                    ]
                    # print(f"\n{op_perf_records=}")
                    cursor.executemany(store_op_perf, op_perf_records)

                    # PRODLINE PERFORMANCE START
                    calc_prod_perf = f"""
                        SELECT
                            `prod_line`,
                            ROUND(AVG(`performance`), 2) AS `performance`
                        FROM
                            `p8_op_performance_h`
                        WHERE
                            `cur_date` = '{cur_date}' AND
                            `cur_time` = '{t_end}'
                        GROUP BY
                            `prod_line`;
                    """
                    calc_prod_perf = re.sub(
                        r"\s+",
                        " ",
                        calc_prod_perf.strip(),
                    )
                    # print(f"\n{calc_prod_perf=}")
                    cursor.execute(calc_prod_perf)
                    prod_results = cursor.fetchall()

                    store_prod_perf = """
                        INSERT INTO `p9_prod_performance_h`
                        (`prod_line`, `performance`, `cur_date`, `cur_time`)
                        VALUES (%s, %s, %s, %s)
                    """
                    prod_records = [
                        (
                            prod_record[0],
                            prod_record[1],
                            cur_date,
                            t_end,
                        )
                        for prod_record in prod_results
                    ]
                    cursor.executemany(
                        store_prod_perf,
                        prod_records,
                    )

                    conn.commit()
                    conn.close()

        except Error as con_err:
            print(f"Connection error: {con_err}")


if __name__ == "__main__":
    main()
