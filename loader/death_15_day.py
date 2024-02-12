from base import covid_sql

SQL = """
SELECT
	date_range as 'Временной диапозон',
	[COVID-19],
	[ОРВИ],
	[Пневмонии],
	[ГРИПП]
FROM
	dbo.v_Count_dead_Covid_Pnev_ORVI_Gripp_all
ORDER BY
	month_start desc
"""


def death_15_day():
    df = covid_sql(SQL)

    filename = "/tmp/Умершие_по_месяцам_на_15_число.xlsx"

    df.set_index("Временной диапозон", inplace=True)
    df.to_excel(filename)

    return filename
