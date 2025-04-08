import cv2
import os
import json


def main() -> None:
    config = json.load(open("config.json"))
    framerate = config["framerate"]
    video_to_frames("input.mp4", "output", framerate)


def video_to_frames(video_path: str, output_folder: str, target_fps: int=1) -> None:
    vidcap = cv2.VideoCapture(video_path)
    original_fps = vidcap.get(cv2.CAP_PROP_FPS)
    frame_interval = int(original_fps / target_fps)
    count = 0
    saved_count = 0
    success, image = vidcap.read()

    while success:
        if count % frame_interval == 0:
            frame_filename = os.path.join(output_folder, f"frame_{saved_count:05d}.jpg")
            cv2.imwrite(frame_filename, image)
            print(f"Extracted frame {frame_filename}")
            saved_count += 1

        success, image = vidcap.read()
        count += 1

    vidcap.release()
    print("Extract frames done!")


if __name__ == "__main__":
    main()