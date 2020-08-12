from fastapi.websockets import WebSocket, WebSocketDisconnect


class Notifier:
    def __init__(self):
        self.connections: List[WebSocket] = []
        self.generator = self.get_notification_generator()

    async def get_notification_generator(self):
        while True:
            message = yield
            await self._notify(message)

    async def push(self, msg: dict):
        await self.generator.asend(msg)

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connections.append(websocket)

    async def remove(self, websocket: WebSocket):
        # await websocket.close()
        try:
            if websocket in self.connections:
                self.connections.remove(websocket)
        except Exception as e:
            print("Remove Exception: ", str(e))

    async def _notify(self, message: str):
        living_connections = []
        while len(self.connections) > 0:
            # Looping like this is necessary in case a disconnection is handled
            # during await websocket.send_text(message)
            websocket = self.connections.pop()
            try:
                await websocket.send_json(message)
                living_connections.append(websocket)
            except WebSocketDisconnect as e:
                print("websocke error in _notify: ", str(e))
            except Exception as e:
                print("Some error here in _nofity:", str(e))
        self.connections = living_connections
