import cv2, os

class FaceDetector(object):
    def __init__(self, xml_path):
        self.classifier = cv2.CascadeClassifier(xml_path)

    def detect(self, image, biggest_only=True):
        scale_factor = 1.2
        min_neighbors = 5
        min_size = (10, 10)
        faces_coord = self.classifier.detectMultiScale(image,
                                                       scaleFactor=scale_factor,
                                                       minNeighbors=min_neighbors,
                                                       minSize=min_size,
                                                       flags=cv2.CASCADE_SCALE_IMAGE)
        return faces_coord


def cut_faces(image, faces_coord):
    faces = []

    for (x, y, w, h) in faces_coord:
        w_rm = int(0.3 * w / 2)
        faces.append(image[y: y + h, x + w_rm: x + w - w_rm])

    return faces


def resize(images, size=(224, 224)):
    images_norm = []
    for image in images:
        if image.shape < size:
            image_norm = cv2.resize(image, size,
                                    interpolation=cv2.INTER_AREA)
        else:
            image_norm = cv2.resize(image, size,
                                    interpolation=cv2.INTER_CUBIC)
        images_norm.append(image_norm)

    return images_norm


def normalize_faces(image, faces_coord):
    faces = cut_faces(image, faces_coord)
    faces = resize(faces)
    return faces

def get_all_img_paths(path):
    files = []
    for (d, _, filepaths) in os.walk(path):
        files.append('%s/%s' % (d, filepaths[0]))
        # files.extend(['%s/%s' % (d, f) for f in filepaths])
        if len(files) == 200:
            break

    return files

def get_imgs_matrix(folder):
    paths = get_all_img_paths(folder)
    matrices = []
    for path in paths:
        if os.path.splitext(path)[-1] == '.jpg':
            print(path)
            img = cv2.imread(path)
            matrices.append(img)
    return matrices

if __name__ == '__main__':
    images = get_imgs_matrix('./lfw-deepfunneled')
    print(images)
    count = 0
    for image in images:
        detector = FaceDetector("haarcascade_frontalface_default.xml")
        faces_coord = detector.detect(image, True)
        faces = normalize_faces(image, faces_coord)
        for i, face in enumerate(faces):
            cv2.imwrite('faces/not_yang_face/%s.jpeg' % (count), faces[i])
            count += 1