"""
Simple HTTP server for serving WebApp files
"""
from aiohttp import web
import os
from loguru import logger

async def serve_webapp(request):
    """Serve registration WebApp"""
    file_path = os.path.join(os.path.dirname(__file__), 'registration.html')
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return web.Response(
            text=content,
            content_type='text/html',
            headers={
                'Cache-Control': 'no-cache',
                'Access-Control-Allow-Origin': '*'
            }
        )
    except Exception as e:
        logger.error(f"Error serving webapp: {e}")
        return web.Response(text="Error loading webapp", status=500)

async def start_webapp_server(port=8080):
    """Start WebApp server"""
    app = web.Application()
    app.router.add_get('/registration', serve_webapp)
    app.router.add_get('/registration.html', serve_webapp)
    
    runner = web.AppRunner(app)
    await runner.setup()
    
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    
    logger.info(f"✅ WebApp server started on http://0.0.0.0:{port}")
    return runner

if __name__ == '__main__':
    import asyncio
    
    async def main():
        runner = await start_webapp_server()
        logger.info("WebApp server is running. Press Ctrl+C to stop.")
        try:
            await asyncio.Event().wait()
        except KeyboardInterrupt:
            logger.info("Stopping WebApp server...")
            await runner.cleanup()
    
    asyncio.run(main())
