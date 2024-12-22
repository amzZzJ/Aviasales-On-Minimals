from src.instance.flights_models import RequestCache
from src.instance.flights_models import Session

def save_request_to_cache(city_from, city_to, date_from, date_to, response):
    session = Session()
    request = RequestCache(
        city_from=city_from,
        city_to=city_to,
        date_from=date_from,
        date_to=date_to,
        response=response
    )
    session.add(request)
    session.commit()
    session.close()

def get_cached_request(city_from, city_to, date_from, date_to):
    session = Session()
    cached_request = session.query(RequestCache).filter_by(
        city_from=city_from,
        city_to=city_to,
        date_from=date_from,
        date_to=date_to
    ).order_by(RequestCache.timestamp.desc()).first()
    session.close()
    return cached_request.response if cached_request else None
