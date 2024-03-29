from pandas import ExcelWriter, DataFrame


def write_styling_excel_file(path: str, df: DataFrame, sheet_name: str):
    "форматируем колонки файла эксель"
    with ExcelWriter(path) as writer:
        df.to_excel(writer, sheet_name=sheet_name, index=False, na_rep='NaN')

        # автонастройка ширины колонок
        # решил что больше ничего и не нужно
        for column in df:
            width = max(df[column].astype(str).map(len).max(), len(column)) + 5
            if width > 45:
                width = 45

            col_idx = df.columns.get_loc(column)
            writer.sheets[sheet_name].set_column(col_idx, col_idx, width)

        writer.save()


"""
from styleframe import StyleFrame, Styler, utils
from pandas import DataFrame


def write_styling_excel_file(
    path: str,
    df: 'DataFrame',
    sheet_name: str
        ) -> None:
    "Создает отформатированный файл экслеля"
    if len(df) == 0:
        for col in df.columns:
            df.loc[0, col] = 'Внесите значение...'

    excel_writer = StyleFrame.ExcelWriter(path)
    sf = StyleFrame(df)
    sf.apply_headers_style(
            cols_to_style=set(df.columns),
            styler_obj=Styler(
                bg_color=utils.colors.grey,
                bold=True,
                border_type=utils.borders.dash_dot
                )
            )
    sf.apply_column_style(
            cols_to_style=set(df.columns),
            styler_obj=Styler(
                horizontal_alignment=utils.horizontal_alignments.left,
                wrap_text=True,
                font=utils.fonts.dejavu_sans
                ),
            style_header=False
            )
    StyleFrame.A_FACTOR = len(df.columns)*1.2
    StyleFrame.P_FACTOR = 1.1

    sf.to_excel(
        excel_writer=excel_writer,
        best_fit=set(df.columns),
        row_to_add_filters=0,
        sheet_name=sheet_name,
            )
    excel_writer.save()
"""


