from PIL import Image
import base64
import io
import re
import numpy as np
from models.sealIntactness.seal_intactness import seal_intactness
from models.containerHealth.health import get_health
from models.hazardourSign.detection import run_detections
from models.alpr.alpr import alpr
from models.containerNumber.container_number import container_number
import cv2


def convert_image_to_numpy_array(image):
    im = Image.open(io.BytesIO(image)).convert("RGB")
    arr = np.array(im)
    return arr


def seal_intactness_connector(image):
    im = convert_image_to_numpy_array(image)
    results = seal_intactness(im)
    ##for now we are choosing the first result only
    if len(results):
        return results[0]
    return {"found": False}


def container_health_connector(image):
    im = convert_image_to_numpy_array(image)
    try:
        results = get_health(im)
    except Exception as e:
        return {"Exception occured": str(e)}
    if len(results):
        return results
    return {"found": False}


def hazardour_detection_connector(image):
    im = convert_image_to_numpy_array(image)
    results = run_detections(im)
    if len(results):
        return results
    return {"found": False}


def alpr_connector(image):
    im = convert_image_to_numpy_array(image)
    result = alpr(im)
    if result["number"] != "":
        return {"result": True, "number": result["number"]}
    else:
        return {"result": False}


# TODO
def container_number_connector(image):
    im = convert_image_to_numpy_array(image)
    results = container_number(image)
    return results
