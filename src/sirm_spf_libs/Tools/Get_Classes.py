from pyodbc import Cursor


def get_classes(dbcurs: Cursor) -> dict[str, dict[int, dict[str, int | float]]] | None:
    dbcurs.execute(
        "SELECT [Label], [Code], [Min], [Max] FROM CLASS ORDER BY [Label], [Code];"
    )

    classes = {}

    for row in dbcurs.fetchall():
        if row[0] not in classes:
            classes[row[0]] = {}

        classes[row[0]][row[1]] = {
            "GT": row[2],
            "EQ": row[2],
            "LT": row[3],
        }

    return classes
