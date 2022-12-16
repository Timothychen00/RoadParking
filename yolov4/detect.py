import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf
physical_devices = tf.config.experimental.list_physical_devices('GPU')
print(physical_devices)
if len(physical_devices) > 0:
    for i in physical_devices:
        tf.config.experimental.set_memory_growth(i, True)

from absl import app, flags, logging
from absl.flags import FLAGS
import yolov4.core.utils as utils
from yolov4.core.functions import *
from PIL import Image
import time
import cv2
import numpy as np

flags.DEFINE_string('framework', 'tflite', '(tf, tflite, trt')
flags.DEFINE_string('weights', './checkpoints/custom-fp16.tflite',
                    'path to weights file')
flags.DEFINE_integer('size', 416, 'resize images to')
flags.DEFINE_boolean('tiny', False, 'yolo or yolo-tiny')
flags.DEFINE_string('model', 'yolov4', 'yolov3 or yolov4')
flags.DEFINE_list('images', './data/images/kite.jpg', 'path to input image')
flags.DEFINE_string('output', './detections/', 'path to output folder')
flags.DEFINE_float('iou', 0.45, 'iou threshold')
flags.DEFINE_float('score', 0.50, 'score threshold')
flags.DEFINE_boolean('count', True, 'count objects within images')
flags.DEFINE_boolean('dont_show', True, 'dont show image output')
flags.DEFINE_boolean('info', True, 'print info on detections')
flags.DEFINE_boolean('crop', True, 'crop detections from images')
flags.DEFINE_boolean('ocr', False, 'perform generic OCR on detection regions')
flags.DEFINE_boolean('plate', False, 'perform license plate recognition')
weights='yolov4/checkpoints/custom-fp16.tflite'

#load model
interpreter = tf.lite.Interpreter(model_path=weights)


def main(images,input_size=416,output='',plate=False):
    t1=time.monotonic()
    # config = ConfigProto()
    # config.gpu_options.allow_growth = True
    # session = InteractiveSession(config=config)
    # STRIDES, ANCHORS, NUM_CLASS, XYSCALE = utils.load_config(FLAGS)
    input_size = 416
    images = [images]

    # loop through images in list and run Yolov4 model on each
    for count, image_path in enumerate(images, 1):
        # t1=time.monotonic()
        original_image = cv2.imread(image_path)
        original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)

        image_data = cv2.resize(original_image, (input_size, input_size))
        image_data = image_data / 255.
        
        # get image name by using split method
        image_name = image_path.split('/')[-1]
        image_name = image_name.split('.')[0]

        images_data = []
        for i in range(1):
            images_data.append(image_data)
        images_data = np.asarray(images_data).astype(np.float32)

        interpreter.allocate_tensors()
        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()
        interpreter.set_tensor(input_details[0]['index'], images_data)
        interpreter.invoke()
        pred = [interpreter.get_tensor(output_details[i]['index']) for i in range(len(output_details))]
        
        print(pred)
        
        print(pred[0][0][0][:4])
        boxes=[]
        pred_conf=[]
        for i in pred[0][0]:
            boxes.append(i[:4])
            pred_conf.append(i[4:])
        print(np.array(boxes,dtype='float32'))
        print(np.array(pred_conf,dtype='float32'))
            # boxes, pred_conf = filter_boxes(pred[0], pred[1], score_threshold=0.25, input_shape=tf.constant([input_size, input_size]))

        # run non max suppression on detections
        print(boxes)
        boxes, scores, classes, valid_detections = tf.image.combined_non_max_suppression(
            boxes=tf.reshape(boxes, (tf.shape(boxes)[0], -1, 1, 4)),
            scores=tf.reshape(
                pred_conf, (tf.shape(pred_conf)[0], -1, tf.shape(pred_conf)[-1])),
            max_output_size_per_class=50,
            max_total_size=50,
            iou_threshold=0.45,
            score_threshold=0.50
        )

        # format bounding boxes from normalized ymin, xmin, ymax, xmax ---> xmin, ymin, xmax, ymax
        original_h, original_w, _ = original_image.shape
        bboxes = utils.format_boxes(boxes.numpy()[0], original_h, original_w)
        
        # hold all detection data in one variable
        pred_bbox = [bboxes, scores.numpy()[0], classes.numpy()[0], valid_detections.numpy()[0]]

        # read in all class names from config
        class_names = utils.read_class_names(cfg.YOLO.CLASSES)

        # by default allow all classes in .names file
        allowed_classes = list(class_names.values())

        # if crop flag is enabled, crop each detection and save it as new image
        crop_path = os.path.join(os.getcwd())
        
        crop_objects(cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB), pred_bbox, crop_path, allowed_classes)
        
        counted_classes = count_objects(pred_bbox, by_class = False, allowed_classes=allowed_classes)
        print(counted_classes)
        # loop through dict and print
        for key, value in counted_classes.items():
            print("Number of {}s: {}".format(key, value))
        image = utils.draw_bbox(original_image, pred_bbox, True, counted_classes, allowed_classes=allowed_classes, read_plate =plate)
        
        image = Image.fromarray(image.astype(np.uint8))
        image = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)
        t2=time.monotonic()
        print("spend_time:",t2-t1,'s')
        # cv2.imwrite(output+ str(count) + '.png', image)
        cv2.imwrite('output_origin.png', image)

if __name__ == '__main__':
    try:
        app.run(main)
    except SystemExit:
        pass
