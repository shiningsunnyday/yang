from process_faces import FaceDetector, normalize_faces
import cv2
import tensorflow as tf
import numpy as np
import argparse

def label_yang(img, model):
    interpreter = tf.lite.Interpreter(model_path=model)
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    # check the type of the input tensor
    floating_model = input_details[0]['dtype'] == np.float32

    # NxHxWxC, H:1, W:2
    height = input_details[0]['shape'][1]
    width = input_details[0]['shape'][2]

    # add N dim
    input_data = np.expand_dims(img, axis=0)

    if floating_model:
        input_data = (np.float32(input_data)) / 255
    interpreter.set_tensor(input_details[0]['index'], input_data)

    interpreter.invoke()

    output_data = interpreter.get_tensor(output_details[0]['index'])
    results = np.squeeze(output_data)

    top_k = results.argsort()[-5:][::-1]
    labels = ['not_yang_face', 'yang_face']
    print(floating_model, "floating")
    for i in top_k:
        if floating_model:
            print('{:08.6f}: {}'.format(float(results[i]), labels[i]))
        else:
            print('{:08.6f}: {}'.format(float(results[i] / 255.0), labels[i]))

def has_yang(path, model):
    image = cv2.imread(path)
    detector = FaceDetector("haarcascade_frontalface_default.xml")
    faces_coord = detector.detect(image, True)
    faces = normalize_faces(image, faces_coord)

    yang = False
    for f in faces:
        if label_yang(f, model):

            yang = True
    return yang

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i',
        '--image')
    parser.add_argument(
        '-m',
        '--model_file')
    args = parser.parse_args()
    print(has_yang(args.image, args.model_file))