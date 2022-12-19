from base import dn122_sql
from clas import Dir


class my_except(Exception):
    pass


def vigruska_p122(DATE):
    "выгрузка"

    P = DATE.split('-')
    DATE = f"{P[2]}-{P[1]}-{P[0]}"

    SQL = f"""select *
            from [oleg].[v_Patient]
            where cast(DateCreate as date) = '{DATE}' """

    try:
        DF = dn122_sql(SQL)
    except Exception as e:
        raise my_except(str(e)[:150])
    else:

        NAME = Dir.get('CARDIO') \
            + f"/ori.cardio.miac/p_122/Архив/{DATE}_svod_p122.xlsx"

        DF.to_excel(NAME, index=False)

        return f'Файл выложен \n {NAME}'
