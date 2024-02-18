def database_dsn() -> dict[str, str]:
    """Generate needed DSN dict from database.dsn

    Raises:
        SystemExit: If the environment variable not set
        SystemExit: If database.dsn doesn't exist
        SystemExit: Improperly formatted DSN
        SystemExit: Database doesn't exist
        SystemExit: Database driver does not exist

    Returns:
        dict[str, str]: DSN variables
    """
    from os import environ
    from pathlib import Path, PurePath
    from configparser import ConfigParser
    from pyodbc import drivers
    import logging

    locallogger = logging.getLogger(__name__)

    fp7dataenviron: str = str(environ.get("FP7Data"))

    # REM - Does the environment variable exist?
    if not fp7dataenviron:
        locallogger.error("* Environment variable does not exist *")
        raise SystemExit

    dsnlocation: Path = Path(fp7dataenviron, "database.dsn")

    # REM - Check if Database.DSN exists
    if not dsnlocation.is_file():
        locallogger.error("* database.dsn does not exist *")
        raise SystemExit

    config = ConfigParser()
    config.read(dsnlocation)

    # REM - Check if ODBC is in the DSN file
    if "ODBC" not in config.sections():
        locallogger.error("* Improperly formatted DSN file *")
        raise SystemExit

    databasedsn: dict[str, dict[str, str]] = {}

    for sect in config.sections():
        # HACK - must strip NULL values that are inserted AFTER executables read DSN
        databasedsn[sect] = {
            key.upper(): value.strip("\x00").replace("?", " ")
            for key, value in config.items(sect)
        }

    if not Path(databasedsn["ODBC"]["DBQ"]).is_file():
        locallogger.error(
            f"* Database ({PurePath(databasedsn['ODBC']['DBQ'])}) does not exist *"
        )
        raise SystemExit

    upgrade: bool = False

    if databasedsn["ODBC"]["DRIVER"] not in drivers():
        databasedsn["ODBC"]["DRIVER"] = str(databasedsn["ODBC"]["DRIVER"]).replace(
            "(*.mdb)", "(*.mdb, *.accdb)"
        )
        upgrade = True

    if databasedsn["ODBC"]["DRIVER"] not in drivers():
        locallogger.error("* Database driver does not exist * (UPGRADE TRIED)")
        raise SystemExit

    if upgrade:
        locallogger.info("Driver upgrade found")

    return databasedsn["ODBC"]
