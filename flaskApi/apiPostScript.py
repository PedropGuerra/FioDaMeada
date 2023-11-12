import tools.flaskSupportTools as apiTools
from flask import request, Response


def apiPostScript():
    import services.crawler.main as NewsCrawl

    apiTools.apiKeyValidate(request.args.get("API_KEY"))
    NewsCrawl.run()
    return Response(status=200)
