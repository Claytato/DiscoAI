import cv2
import numpy as np
import time
from tflite_support.task import processor
from twilio.rest import Client 
from picamera import PiCamera

_MARGIN = 10  # pixels
_ROW_SIZE = 10  # pixels
_FONT_SIZE = 1
_FONT_THICKNESS = 1
_TEXT_COLOR = (0, 0, 255)  # red


def visualize(
    image: np.ndarray,
    detection_result: processor.DetectionResult,
) -> np.ndarray:

  for detection in detection_result.detections:
    # Draw bounding_box
    bbox = detection.bounding_box
    start_point = bbox.origin_x, bbox.origin_y
    end_point = bbox.origin_x + bbox.width, bbox.origin_y + bbox.height
    cv2.rectangle(image, start_point, end_point, _TEXT_COLOR, 1)

    # Draw label and score
    category = detection.classes[0]
    class_name = category.class_name
    probability = round(category.score, 2)
    if class_name == 'person':
        if probability > 0.80:
          print("person")
          
          account_sid = 'ACaeb61217c51f11c2655ecbd9a9c2f0fc' 
          auth_token = '97f4077ad0a37263c97073093a0f0aea' 
          client = Client(account_sid, auth_token) 
          
          message = client.messages.create(  
                                        messaging_service_sid='MGcc5e54c0df3f1d8ca17e5abe57ac94ec', 
                                        body='Person Detected!!!',      
                                        to='+14192174630' 
                                    ) 
          camera = PiCamera()
          time.sleep(2)
          camera.capture('../pictures/img.jpg')

          print(message.sid)
          
          time.sleep(60)
          
    result_text = class_name + ' (' + str(probability) + ')'
    text_location = (_MARGIN + bbox.origin_x,
                     _MARGIN + _ROW_SIZE + bbox.origin_y)
    cv2.putText(image, result_text, text_location, cv2.FONT_HERSHEY_PLAIN,
                _FONT_SIZE, _TEXT_COLOR, _FONT_THICKNESS)

  return image
