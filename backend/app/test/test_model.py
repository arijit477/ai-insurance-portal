from pathlib import Path

from ultralytics import YOLO

MODEL_PATH = Path(__file__).resolve().parents[1] / "models" / "vehicel_damage.pt"

model = YOLO(str(MODEL_PATH))  # load a pretrained model (recommended for training)

print(model.names)

SOURCE_PATH = Path(__file__).resolve().parent / "test_image.jpg"

results = model.predict(
    source=str(SOURCE_PATH),
    conf=0.3,
    save=True,
)


print(results)