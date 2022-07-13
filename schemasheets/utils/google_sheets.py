BASE = "https://docs.google.com/spreadsheets/d"

def gsheets_download_url(sheet_id: str, sheet_name: str) -> str:
    """
    Get the google sheets download URL

    :param sheet_id: 1wVoaiFg47aT9YWNeRfTZ8tYHN8s8PAuDx5i2HUcDpvQ
    :param sheet_name: e.g. personinfo
    :return:
    """
    return f"{BASE}/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"


