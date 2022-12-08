from datetime import datetime
from pandas import ExcelWriter, DataFrame
import shutil

from base import ncrn_sql, ncrn_exec
from clas import Dir


def regiz_decomposition():
    "разложение файлов ответа нетрики по ошибкам историй болезней"
    DF = ncrn_sql('SELECT * FROM [dbo].[v_Answer_MO]')
    if len(DF) == 0:
        return "РЕГИЗ РАЗЛОЖЕНИЕ ФАЙЛОВ: Нечего раскладывать по папкам"

    STATISTIC = DataFrame()
    DATE = datetime.now().strftime('%Y-%m-%d')
    ROOT = Dir.get('regiz')

    for FTP in DF.ftp_user.unique():
        PART = DF.loc[DF.ftp_user == FTP]
        LPU_NAME = PART.LPU_name.values[0]

        del PART['ftp_user']
        del PART['LPU_level1_key']
        del PART['LPU_name']
        PART.rename(columns={
            'HistoryNumber': 'Номер истории болезни',
            'OpenDate': 'Дата открытия СМО',
            'Error': 'Ошибка, выявленная в РЕГИЗ',
            }, inplace=True)

        PATH = ROOT + '/' + FTP \
            + f'/Ответы/_{DATE} {LPU_NAME}.xlsx'.replace('"', '')
        with ExcelWriter(PATH) as writer:
            try:
                PART.to_excel(
                    writer,
                    sheet_name='номера',
                    index=False
                        )
            except PermissionError:
                Error = 'Не удалось положить файл из-за ошибки доступа'
                STATISTIC = STATISTIC.append({
                    'MOName':       LPU_NAME,
                    'NameFile':     PATH.split('/')[-1],
                    'CountRows':    len(PART),
                    'TextError':    Error,
                    'OtherFiles':   '',
                    'DateLoadFile': datetime.now(),
                    'InOrOut':      'Out',
                    })
            else:
                STATISTIC = STATISTIC.append({
                    'MOName':       LPU_NAME,
                    'NameFile':     PATH.split('/')[-1],
                    'CountRows':    len(PART),
                    'TextError':    '',
                    'OtherFiles':   '',
                    'DateLoadFile': datetime.now(),
                    'InOrOut':      'Out',
                    })
    DATE = datetime.now().strftime('%d.%m.%Y_%H-%M')
    PATH = Dir.get('regiz_svod') + f'/{DATE}_лог_разложения.xlsx'
    with ExcelWriter(PATH) as writer:
        STATISTIC.to_excel(writer, sheet_name='логи', index=False)

    TEMP_LOG = f'temp/{DATE}_decomposition_log.xlsx'
    shutil.copyfile(PATH, TEMP_LOG)
    SQL = """
    -- после отправки в МО
    -- Обновление даты отправки ответа в МО
    UPDATE [dbo].[HistoryAnswerFromShowcase]
        SET [DateAnswerMO] = GETDATE()
        WHERE [DateAnswerMO] is null
    -- Обновление даты отправки ответа в МО
    UPDATE [dbo].[ErrorRequest]
        SET [DateSend] = GETDATE()
        WHERE [DateSend] is null
            AND [TextError] not like 'MIAC:%'
    """

    ncrn_exec(SQL)

    return TEMP_LOG
