from imageai.Detection.Custom import CustomObjectDetection
from imageai.Detection.Custom import DetectionModelTrainer
import imageai
import os
import cv2


os.environ['TF_FORCE_GPU_ALLOW_GROWTH'] = 'true'

def train():
	trainer = DetectionModelTrainer()
	trainer.setModelTypeAsYOLOv3()
	trainer.setDataDirectory(data_directory="")
	trainer.setTrainConfig(object_names_array=["Container", "Dent", "Rust", "Crack"], batch_size=4, num_experiments=100, train_from_pretrained_model="pretrained-yolov3.h5")
	#trainer.trainModel()


def get_health(image):
	detector = CustomObjectDetection()
	detector.setModelTypeAsYOLOv3()
	detector.setModelPath("models/detection_model-ex-046--loss-0006.159.h5") 
	detector.setJsonPath("json/detection_config.json")
	detector.loadModel()
	detections = detector.detectObjectsFromImage(
		input_image=image,
		input_type="array",
		output_type="array"
	)
	for detection in detections[1]:
	    print(detection["name"], " : ", detection["percentage_probability"], " : ", detection["box_points"])
	cv2.imshow("frame", detections[0])
	cv2.waitKey(0)
	cv2.destroyAllWindows()

	return detections[1]


im = cv2.imread("detection.jpg")

print(get_health(im))