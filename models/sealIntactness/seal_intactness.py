# !pip3 install tensorflow-gpu==1.13.1
# !pip3 install imageai --upgrade

from imageai.Detection.Custom import DetectionModelTrainer
from imageai.Detection.Custom import CustomObjectDetection
import os

# path variables
root_dir_path = os.path.dirname(os.path.abspath("app.py"))
custom_model_path = (
    root_dir_path + "/models/sealIntactness/detection_model-ex-024--loss-0005.743.h5"
)
custom_model_json_path = root_dir_path + "/models/sealIntactness/detection_config.json"
output_image_path = root_dir_path + "/models/sealIntactness/output_images"
data_directory = root_dir_path + "/models/sealIntactness/data"

detector = CustomObjectDetection()
detector.setModelTypeAsYOLOv3()
detector.setModelPath(custom_model_path)
detector.setJsonPath(custom_model_json_path)
detector.loadModel()


def trainer():
    trainer = DetectionModelTrainer()
    trainer.setModelTypeAsYOLOv3()
    trainer.setDataDirectory(data_directory=data_directory)
    trainer.setTrainConfig(
        object_names_array=["seal", "no_seal"],
        batch_size=4,
        num_experiments=50,
        train_from_pretrained_model="pretrained-yolov3.h5",
    )
    trainer.trainModel()


def seal_intactness(image):
    detections = detector.detectObjectsFromImage(
        input_image=image, input_type="array", output_type="array"
    )
    results = []
    print(detections)
    for detection in detections[1]:
        print(
            detection["name"],
            " : ",
            detection["percentage_probability"],
            " : ",
            detection["box_points"],
        )
        results.append(
            {
                "result": True if detection["name"] == "seal" else False,
                "confidence": detection["percentage_probability"],
            }
        )
    return results
