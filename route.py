from aiohttp import web

routes = web.RouteTableDef()

@routes.get("/", allow_head=True)
async def root_route_handler(request):
    return web.json_response({
        "status": "ok",
        "service": "auto-rename-bot",
        "message": "CodeRips auto-rename bot is running",
    })


@routes.get("/health", allow_head=True)
async def health_route_handler(request):
    return web.json_response({"status": "healthy"})


async def web_server():
    web_app = web.Application(client_max_size=30000000)
    web_app.add_routes(routes)
    return web_app



# Jishu Developer 
# Don't Remove Credit 🥺
# Telegram Channel @Madflix_Bots
# Developer @JishuDeveloper
