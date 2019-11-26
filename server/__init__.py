from aiohttp.web import *


routes = RouteTableDef()
app = Application()

@routes.get('/')
async def hello(request):
    return Response(text="Hello, world")

