import cv2
from huggingface_hub import hf_hub_download
from ultralytics import YOLO


# Download and load the model
weights = hf_hub_download(
    repo_id="mancalazure/construction-ppe-safety",
    filename="best.pt"
)

model = YOLO(weights)


def analyze_video(video_path):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        raise ValueError("Could not open video")

    # Overall statistics
    total_frames = 0
    people_detected = 0
    hardhats_detected = 0
    no_hardhats_detected = 0
    safety_vests_detected = 0
    no_safety_vests_detected = 0
    no_masks_detected = 0

    # PPE compliance for each processed frame
    frame_compliance_scores = []

    # Process every 5th frame
    frame_skip = 10

    while True:
        success, frame = cap.read()

        if not success:
            break

        total_frames += 1

        # Skip frames to make processing faster
        if total_frames % frame_skip != 0:
            continue

        # Run YOLO
        results = model.predict(
            source=frame,
            imgsz =640 ,
            verbose=False
        )

        # Statistics for this particular frame
        frame_people = 0
        frame_no_hardhat = 0
        frame_no_vest = 0
        frame_no_mask = 0

        # Process detections
        for result in results:

            for box in result.boxes:

                class_id = int(box.cls[0])
                class_name = result.names[class_id]

                # Overall statistics
                if class_name == "Person":
                    people_detected += 1
                    frame_people += 1

                elif class_name == "Hardhat":
                    hardhats_detected += 1

                elif class_name == "NO-Hardhat":
                    no_hardhats_detected += 1
                    frame_no_hardhat += 1

                elif class_name == "Safety Vest":
                    safety_vests_detected += 1

                elif class_name == "NO-Safety Vest":
                    no_safety_vests_detected += 1
                    frame_no_vest += 1

                elif class_name == "NO-Mask":
                    no_masks_detected += 1
                    frame_no_mask += 1

        # Calculate PPE compliance for this frame
        if frame_people > 0:

            violations = (
                frame_no_hardhat
                + frame_no_vest
                + frame_no_mask
            )

            compliance = max(
                0,
                100 - (violations / frame_people * 100)
            )

            frame_compliance_scores.append(compliance)

    cap.release()

    # Calculate average PPE compliance
    if frame_compliance_scores:
        ppe_compliance = (
            sum(frame_compliance_scores)
            / len(frame_compliance_scores)
        )
    else:
        ppe_compliance = 0

    return {
        "frames_processed": total_frames,
        "people_detected": people_detected,
        "hardhats_detected": hardhats_detected,
        "no_hardhats_detected": no_hardhats_detected,
        "safety_vests_detected": safety_vests_detected,
        "no_safety_vests_detected": no_safety_vests_detected,
        "no_masks_detected": no_masks_detected,
        "ppe_compliance": round(ppe_compliance, 2)
    }


# Test the analyzer
if __name__ == "__main__":

    video_path = "test.mp4"

    results = analyze_video(video_path)

    print("\n--- Safety Vision Results ---")

    for key, value in results.items():
        print(f"{key}: {value}")