import pandas
import config

from fastapi import APIRouter

countries_router = APIRouter(prefix="/countries", tags=["countries resource"])


@countries_router.get("")
def get_countries():
    redis_client = config.create_redis_client()
    if countries := redis_client.get_data("countries"):
        redis_client.client.close()
        return countries
    df = pandas.read_csv('static/worldcities.csv')
    countries = set(map(lambda iv: iv[1], df["country"].items()))
    redis_client.set_data(countries, "countries")
    redis_client.client.close()
    return countries


@countries_router.get("/{country}/cities")
def get_country(country: str):
    redis_client = config.create_redis_client()
    if cities := redis_client.get_data(f"{country}-cities"):
        redis_client.client.close()
        return cities
    df = pandas.read_csv('static/worldcities.csv')
    cities = list(map(lambda kv: kv[1], df.loc[df["country"].str.contains(country), 'city_ascii'].items()))
    redis_client.set_data(cities, f"{country}-cities")
    redis_client.client.close()
    return cities


__all__ = ["countries_router"]
