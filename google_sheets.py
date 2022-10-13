import pygsheets


class GoogleSheet:
    def __init__(self, google_sheet_link: str, google_auth_file_path: str):
        gc = pygsheets.authorize(service_file=google_auth_file_path)
        sh = gc.open_by_url(google_sheet_link)
        self.wks = sh[0]

    def insert_row(self, row: list) -> None:
        self.wks.insert_rows(row=1, number=1, values=[row])

    def get_records_by_telegram_id(self, telegram_id: str) -> list:
        table = self.wks.get_all_values()[1::]
        result = []
        for row in table:
            if row[0] == telegram_id:
                result.append(
                    {"answer": row[1], "yellow": row[2], "blue": row[3], "red": row[4]}
                )

            if row[0] == "":
                break
        return result
