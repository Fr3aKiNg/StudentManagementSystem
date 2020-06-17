import cv2
import datetime
from src.Loader import Loader

class FaceDetection:

    def __init__(self, model):
        self.img_index = 0
        self.model = model
        self.classes = list(set(Loader().get_classes()))
        self.cam = cv2.VideoCapture(0)
        self.cascade_path = "haarcascade_frontalface_default.xml"
        self.face_cascade = cv2.CascadeClassifier(self.cascade_path)

    def __del__(self):
        self.cam.release()
        cv2.destroyAllWindows()

    def draw_rectangle(self, image, coords):
        (x, y, w, h) = coords
        cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)

    def draw_text(self, image, text, frame):
        (x, y, _, h) = frame
        center = (x, int(y + h / 2))
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(image, text, center, font, 0.8, (0, 255, 0), 2, cv2.LINE_AA)

    def open(self):
        cv2.namedWindow("acd_face")
        while True:
            ret, frame = self.cam.read()

            if not ret:
                break

            image, faces = self.detect_faces(frame)

            if (cv2.getWindowProperty("acd_face", 1) == -1):
                break
            
            cv2.imshow("acd_face", frame)
            cv2.waitKey(1)

    def detect_faces(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        coord_faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags = cv2.CASCADE_SCALE_IMAGE
        )
        
        faces = []

        for (x, y, w, h) in coord_faces:
            temp = image[y:y+h, x:x+w]
            faces.append(temp)
            pred = self.model.predict(temp)
            self.draw_text(image, self.classes[pred], (x, y, w, h))
            self.draw_rectangle(image, (x, y, w, h))
            
        return image, faces

    def save_img(self, face):
        imgname = "sample/" + str(self.img_index) + ".png"
        self.img_index += 1
        print("Save new image " + imgname)
        cv2.imwrite(imgname, face)
        cv2.imwrite(imgname, face)
