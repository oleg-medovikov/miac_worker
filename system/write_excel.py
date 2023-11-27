from pandas import ExcelWriter


def write_excel(filename: str, dict_: dict):
    with ExcelWriter(filename, engine="xlsxwriter") as wb:
        for key, value in dict_.items():
            value.to_excel(wb, sheet_name=key, index=False, header=False, startrow=1)
            sheet = wb.sheets[key]

            cell_format = wb.book.add_format()
            cell_format.set_align("top")
            cell_format.set_font_size(11)
            cell_format.set_text_wrap()
            cell_format.set_bold()

            for col, name in enumerate(value.columns):
                try:
                    width = max(value[name].astype(str).map(len).max(), len(name))
                except:
                    width = 40

                width = {
                    width > 45: 45,
                    width < 20: 20,
                }.get(True, width)

                sheet.write(0, col, name, cell_format)
                sheet.set_column(0, col, width)
            sheet.autofilter(0, 0, value.shape[0], len(value.columns) - 1)
