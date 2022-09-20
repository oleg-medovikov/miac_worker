from base import covid_sql

def hospitalised_in_fr():
    """Отчет по ежедневно госпитализированным"""
    
    SQL = "EXEC [dbo].[p_Hospitalized_in_FedReg]"

    df = covid_sql(SQL)
    
    MESS = f"Число госпитализированных пациентов на дату {df.at[0,'date']} составляет {df.at[0,'Count']} человек."

    return MESS 
    
