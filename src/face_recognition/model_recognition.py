import argparse
import pickle
from pathlib import Path
import cv2
from face_recognizer import recognize_faces

import face_recognition

DEFAULT_ENCODINGS_PATH = Path("../../output/encodings.pkl")

PATH_TRAINING = "../../images/faces/training"
PATH_OUTPUT = "../../output"
PATH_VALIDATION = "../../images/faces/validation"


# Create directories if they don't already exist
Path(PATH_TRAINING).mkdir(exist_ok=True)
Path(PATH_OUTPUT).mkdir(exist_ok=True)
Path(PATH_VALIDATION).mkdir(exist_ok=True)

parser = argparse.ArgumentParser(description="Recognize faces in an image")
parser.add_argument("--train", action="store_true", help="Train on input data")
parser.add_argument(
    "--validate", action="store_true", help="Validate trained model"
)
parser.add_argument(
    "--test", action="store_true", help="Test the model with an unknown image"
)
parser.add_argument(
    "-m",
    action="store",
    default="hog",
    choices=["hog", "cnn"],
    help="Which model to use for training: hog (CPU), cnn (GPU)",
)
parser.add_argument(
    "-f", action="store", help="Path to an image with an unknown face"
)
args = parser.parse_args()


def encode_known_faces(
    model: str = "hog", encodings_location: Path = DEFAULT_ENCODINGS_PATH
) -> None:
    """
    Loads images in the training directory and builds a dictionary of their
    names and encodings.
    """
    names = []
    encodings = []

    for filepath in Path(PATH_TRAINING).glob("*/*"):
        name = filepath.parent.name
        image = face_recognition.load_image_file(filepath)

        face_locations = face_recognition.face_locations(image, model=model)
        face_encodings = face_recognition.face_encodings(image, face_locations)

        for encoding in face_encodings:
            names.append(name)
            encodings.append(encoding)

    name_encodings = {"names": names, "encodings": encodings}
    with encodings_location.open(mode="wb") as f:
        pickle.dump(name_encodings, f)


def validate(model: str = "hog"):
    """
    Runs recognize_faces on a set of images with known faces to validate
    known encodings.
    """
    for filepath in Path(PATH_VALIDATION).rglob("*"):
        if filepath.is_file():
            recognize_faces(
                img=str(filepath.absolute()), model=model
            )


if __name__ == "__main__":
    if args.train:
        encode_known_faces(model=args.m)
    if args.validate:
        validate(model=args.m)
    if args.test:
        video = cv2.VideoCapture(0) #lê da webcam
        check, img = video.read() #lê o vídeo
        recognize_faces(img=img, model=args.m, encodings_location=DEFAULT_ENCODINGS_PATH)
        video.release()
        cv2.destroyAllWindows()
