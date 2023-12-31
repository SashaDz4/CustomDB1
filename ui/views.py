import PySimpleGUI as sg

SIZE = (18, 1)


def create_db_view():
    return sg.Window(
        "Create DB",
        [
            [sg.T("Enter DB name"), sg.In(key="-DB-NAME-", size=SIZE)],
            [sg.B("OK"), sg.B("Cancel")],
        ],
    ).read(close=True)


def add_table_view():
    return sg.Window(
        "Add Table",
        [
            [sg.T("Enter Table name"), sg.In(key="-TABLE-NAME-", size=SIZE)],
            [sg.B("OK"), sg.B("Cancel")],
        ],
    ).read(close=True)


def delete_table_view():
    return sg.Window(
        "Delete Table",
        [
            [sg.T("Enter Table name to delete"), sg.In(key="-TABLE-NAME-")],
            [sg.B("OK"), sg.B("Cancel")],
        ],
    ).read(close=True)


def add_column_view(column_choices: list[str], table_name: str = ""):
    return sg.Window(
        "Add Column",
        [
            [
                sg.T("Enter Table name"),
                sg.In(key="-TABLE-NAME-", default_text=table_name, size=SIZE),
            ],
            [sg.T("Choose Column type"), sg.Combo(column_choices, key="-COLUMN-TYPE-")],
            [sg.T("Enter Column name"), sg.In(key="-COLUMN-NAME-", size=SIZE)],
            [sg.B("OK"), sg.B("Cancel")],
        ],
    ).read(close=True)


def add_row_view(column_names: list[str]):
    return sg.Window(
        "Add Row",
        [
            *[
                [
                    sg.T(f"Enter {field}:"),
                    sg.In(key=field),
                ]
                if field.split(": ")[1] != "time interval"
                else [
                    sg.T(f"Enter {field}:"),
                    sg.In(key=f"{field}-1", size=SIZE),
                    sg.In(key=f"{field}-2", size=SIZE),
                ]
                for field in column_names
            ],
            [sg.B("OK"), sg.B("Cancel")],
        ],
    ).read(close=True)


def delete_row_view():
    return sg.Window(
        "Delete Row",
        [
            [sg.T("Enter Row index to delete"), sg.In(key="-ROW-INDEX-", size=SIZE)],
            [sg.B("OK"), sg.B("Cancel")],
        ],
    ).read(close=True)


def change_row_view():
    return sg.Window(
        "Change Row / Step 1",
        [
            [sg.T("Enter Row index to change"), sg.In(key="-ROW-INDEX-", size=SIZE)],
            [sg.B("OK"), sg.B("Cancel")],
        ],
    ).read(close=True)


def change_columns_view(column_names: list[str]):
    return sg.Window(
        "Find rows",
        [
            *[
                [
                    sg.T(f"Column name:"),
                    sg.In(key=field, default_text=field.split(':')[0], size=SIZE),
                    sg.T("Column position:"),
                    sg.In(key=f"{field}-COLUMN-POSITION-", default_text=column_names.index(field) + 1, size=(5, 1)),
                ]
                for field in column_names
            ],
            [sg.B("OK"), sg.B("Cancel")],
        ],
    ).read(close=True)


def change_row_detailed_view(column_names: list[str], default_values: list):
    return sg.Window(
        "Change Row / Step 2",
        [
            *[
                [
                    sg.T(f"Enter new value for {field}:"),
                    sg.In(key=field, default_text=default_values[index], size=SIZE),
                ]
                for index, field in enumerate(column_names)
            ],
            [sg.B("OK"), sg.B("Cancel")],
        ],
    ).read(close=True)


def save_db_view():
    return sg.Window(
        "Save DB",
        [
            [sg.T("Enter path to save db"), sg.In(key="-DB-SAVE-PATH-")],
            [sg.B("OK"), sg.B("Cancel")],
        ],
    ).read(close=True)


def open_db_view():
    return sg.Window(
        "Open DB",
        [
            [sg.T("Enter path to open db"), sg.In(key="-DB-OPEN-PATH-")],
            [sg.B("OK"), sg.B("Cancel")],
        ],
    ).read(close=True)
