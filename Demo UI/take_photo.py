import cv2
import numpy as np

# loads the face cascade
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


def take_photo():
    """ Opens the camera and takes a picture.

    Returns:
    capture_success (bool): True if image capture was successful.

    """

    # prevents openCL usage and unnecessary logging messages
    cv2.ocl.setUseOpenCL(False)

    # start camera feed
    camera = cv2.VideoCapture(0)  # The integer is the index of the user's camera

    capture_success = False

    while True:
        ret, frame = camera.read()  # ret is just a confirmation and frame is the image frame captured
        if not ret:
            print("Failed to capture image! Aborting!")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # makes it grayscale
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)  # returns the faces detected as (x, y, w, h)

        for(x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y - 50), (x + w, y + h + 10), (255, 0, 0), 2)  # drawing an rectangle on the original colored frame

        cv2.imshow('Camera', cv2.resize(frame, (700, 500)))

        key = cv2.waitKey(1)
        if key % 256 == 27:
            break  # esc is pressed. Quitting function
        elif key % 256 == 32:
            # space bar is pressed and saving the current frame
            # the dir of the file is hardcoded for now
            if cv2.imwrite('data/capture.png', frame):
                print("Capture Succesfull")
                capture_success = True
                break
            else:
                print("Could not capture")

    camera.release()
    cv2.destroyAllWindows()
    return capture_success


def detect_mood(img_src, model):
    """ Detects the mood from the given photo.

    Parameters:
    img_src (str): Source of the image.
    model (obj): Keras of the preloaded model.

    Returns:
    emotion_dict[maxindex] (str): Name of the mood that was detected if any mood was detected.
    "No faces detected" (str): If no face was detected in the photo.

    """

    # reads the image
    image = cv2.imread(img_src)  # reads the image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # makes it grayscale

    # dictionary which assigns each label an emotion (alphabetical order)
    emotion_dict = {0: "Angry", 1: "Disgusted", 2: "Fearful", 3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}

    # loads the face cascade
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)  # returns the faces detected as (x, y, w, h)

    if len(faces) != 0:
        for(x, y, w, h) in faces:
            roi_gray = gray[y:y + h, x:x + w]
            cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray, (48, 48)), -1), 0)
            prediction = model.predict(cropped_img)
            maxindex = int(np.argmax(prediction))
            return emotion_dict[maxindex]  # returns the detected emotion
    else:
        return "No faces detected"
