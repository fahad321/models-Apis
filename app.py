from fastapi import FastAPI, File
from fastapi.websockets import WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
import datetime
from connectors.connector import (
    seal_intactness_connector,
    container_health_connector,
    hazardour_detection_connector,
    container_number_connector,
    alpr_connector,
)
from fastapi.websockets import WebSocket, WebSocketDisconnect
from supporter.notifiier import Notifier

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

notifier = Notifier()


@app.get("/")
def root():
    return jsonable_encoder({"🪴": "🪴"})


@app.post("/seal_intactness")
async def seal_intactness(file: bytes = File("file")):
    time = datetime.datetime.utcnow()
    res = seal_intactness_connector(file)
    res["time"] = time
    res = jsonable_encoder(res)
    await notifier.push(res)
    return res


@app.post("/container_health")
async def seal_intactness(file: bytes = File("file")):
    res = container_health_connector(file)
    res = jsonable_encoder(res)
    await notifier.push(res)
    return jsonable_encoder(
        {"ratio": res["ratio"], "confidence": res["confidence"], "img": "img"}
    )


# TODO
@app.post("/container_number")
async def seal_intactness(file: bytes = File("file")):
    res = container_number_connector(file)
    return jsonable_encoder(res)


@app.post("/alpr")
async def seal_intactness(file: bytes = File("file")):
    res = alpr_connector(file)
    res = jsonable_encoder(res)
    await notifier.push(res)
    return


@app.post("/hazardour_sign_detector")
async def seal_intactness(file: bytes = File("file")):
    res = hazardour_detection_connector(file)
    return jsonable_encoder({"maybe": "working"})


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await notifier.connect(websocket)

    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_json(jsonable_encoder({"response": "connected"}))

    except WebSocketDisconnect as e:
        await notifier.remove(websocket)
        print(
            "Success fully removed connection in which exception has occured: ", str(e)
        )
    except Exception as e:
        print("Exception ::::", str(e))


@app.on_event("startup")
async def startup():
    # Prime the push notification generator
    await notifier.generator.asend(None)
