import threading
import asyncio
from websockets import serve, ConnectionClosedError

class WebSocket:
    def __init__(self, port=5556) -> None:
        self.message = ''
        self.port = port
        
        self.server_thread = threading.Thread(target=self.run_server)
        self.server_thread.daemon = True
        self.server_thread.start()
        
        print("Server started")

    async def start_server(self):
        try:
            async with serve(self.server, "127.0.0.1", self.port):
                await asyncio.Event().wait()  # Keeps the server running indefinitely
        except OSError as e:
            print(f"Failed to start server on port {self.port}: {e}")

    def run_server(self):
        asyncio.run(self.start_server())

    async def server(self, websocket, path):
        try:
            async for message in websocket:
                self.message = message
        except ConnectionClosedError:
            print("Connection closed unexpectedly")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            await websocket.close()

    def get_last_message(self):
        return self.message

# Example usage:
if __name__ == "__main__":
    ws = WebSocket(5555)
