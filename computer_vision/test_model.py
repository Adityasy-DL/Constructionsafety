from huggingface_hub import hf_hub_download
from ultralytics import YOLO

# Download the model
weights = hf_hub_download(
    repo_id="mancalazure/construction-ppe-safety",
    filename="best.pt"
)

# Load the model
model = YOLO(weights)

# Test image
source = "test.jpg"

# Run detection
results = model.predict(
    source=source,
    save=True
)

# Print detections
for result in results:
    for box in result.boxes:
        class_id = int(box.cls[0])
        confidence = float(box.conf[0])
        class_name = result.names[class_id]

        print(f"{class_name}: {confidence:.2f}")