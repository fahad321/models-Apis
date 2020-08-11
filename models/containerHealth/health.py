from imageai.Detection.Custom import CustomObjectDetection
from imageai.Detection.Custom import DetectionModelTrainer
import imageai
import os
import cv2

os.environ["TF_FORCE_GPU_ALLOW_GROWTH"] = "true"


detector = CustomObjectDetection()
detector.setModelTypeAsYOLOv3()
detector.setModelPath(
    "models/containerHealth/models/detection_model-ex-041--loss-0006.173.h5"
)
detector.setJsonPath("models/containerHealth/json/detection_config.json")
detector.loadModel()


def get_area(a):
    x1, y1, x2, y2 = a["box_points"]

    area = abs(x2 - x1) * (y2 - y1)
    return area


def get_health(image):
    detections = detector.detectObjectsFromImage(
        input_image=image, input_type="array", output_type="array"
    )
    area = 0
    total_area = 0
    probs = []
    dic = dict.fromkeys(["ratio", "confidence", "image"])
    for detection in detections[1]:
        # print(detection)
        if detection["name"] == "Container":
            total_area = get_area(detection)
            print("total_area: ", total_area)
        else:
            area += get_area(detection)
            # print("Area added: ", area)
        ratio = (total_area - area) / total_area
        probs.append(detection["percentage_probability"])
        print(
            detection["name"],
            " : ",
            detection["percentage_probability"],
            " : ",
            detection["box_points"],
            "Ratio: ",
            ratio,
        )
    dic["ratio"] = ratio
    dic["confidence"] = probs
    dic["image"] = detections[0]
    return dic


def train():
    trainer = DetectionModelTrainer()
    trainer.setModelTypeAsYOLOv3()
    trainer.setDataDirectory(data_directory="")
    trainer.setTrainConfig(
        object_names_array=["Container", "Dent", "Rust", "Crack"],
        batch_size=4,
        num_experiments=100,
        train_from_pretrained_model="pretrained-yolov3.h5",
    )
    trainer.trainModel()
