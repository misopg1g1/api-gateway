import pandas

from fastapi import APIRouter

countries_router = APIRouter(prefix="/countries", tags=["countries resource"])


@countries_router.get("")
def get_countries():
    df = pandas.read_csv('static/worldcities.csv')
    return set(map(lambda iv: iv[1], df["country"].items()))


@countries_router.get("/{country}/cities")
def get_country(country: str):
    df = pandas.read_csv('static/worldcities.csv')
    return list(map(lambda kv: kv[1], df.loc[df["country"].str.contains(country), 'city_ascii'].items()))


__all__ = ["countries_router"]
