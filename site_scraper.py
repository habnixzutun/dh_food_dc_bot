from bs4 import BeautifulSoup
from requests import get
from dotenv import load_dotenv
import datetime

def get_kw(date: datetime.date) -> int:
    calender = date.isocalendar()
    return calender.week


def get_week_source(date: datetime.date = None) -> BeautifulSoup | None:
    url = "https://www.sw-ka.de/de/hochschulgastronomie/speiseplan/mensa_erzberger/"
    if date is not None:
        url += f"?kw={get_kw(date)}"

    response = get(url)
    if not response.ok:
        return None
    soup = BeautifulSoup(response.content, "html.parser")
    return soup


def get_week_data(soup: BeautifulSoup) -> dict:
    return {}

def main():
    soup = get_week_source(datetime.date.today() + datetime.timedelta(weeks=0))
    print(get_week_data(soup))


if __name__ == '__main__':
    load_dotenv()
    main()