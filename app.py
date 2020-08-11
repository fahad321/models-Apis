from fastapi import FastAPI, File
from fastapi.websockets import WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from connectors.connector import (
    seal_intactness_connector,
    container_health_connector,
    hazardour_detection_connector,
    container_number_connector,
    alpr_connector,
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return jsonable_encoder({"🪴": "🪴"})


@app.post("/seal_intactness")
def seal_intactness(file: bytes = File("file")):
    res = seal_intactness_connector(file)
    return jsonable_encoder(res)


@app.post("/container_health")
def seal_intactness(file: bytes = File("file")):
    res = container_health_connector(file)
    return jsonable_encoder(
        {"ratio": res["ratio"], "confidence": res["confidence"], "img": "img"}
    )


# TODO
@app.post("/container_number")
def seal_intactness(file: bytes = File("file")):
    res = container_number_connector(file)
    return jsonable_encoder(res)


@app.post("/alpr")
def seal_intactness(file: bytes = File("file")):
    res = alpr_connector(file)
    return jsonable_encoder(res)


@app.post("/hazardour_sign_detector")
def seal_intactness(file: bytes = File("file")):
    res = hazardour_detection_connector(file)
    return jsonable_encoder({"maybe": "working"})
