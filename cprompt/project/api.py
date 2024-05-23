from ninja import NinjaAPI

api = NinjaAPI(version="1.0.0")
api.add_router("/darulez/", "cprompt.darulez.api.router", tags=["darulez"])
