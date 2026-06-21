import uvicorn

def start_server():
    uvicorn.run(
        app='places.main.app',
        host='localhost',
        port=8000,
        workers=1,
    )


if __name__ == '__main__':
    start_server()
