import cv2
import os
import subprocess
import json


def main() -> None:
    config = json.load(open("config.json"))
    framerate = config["framerate"]
    width = config["width"]
    height = config["height"]
    frames_to_video("processed_frames", "processed_video.mp4", framerate, (width, height))
    add_audio_to_video("input.mp4", "processed_video.mp4", "output.mp4")


def frames_to_video(frames_folder: str, output_path: str, fps: int, frame_size: tuple):
    out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, frame_size)

    frame_files = sorted(
        [f for f in os.listdir(frames_folder) if f.endswith('.jpg')]
    )

    for filename in frame_files:
        frame = cv2.imread(os.path.join(frames_folder, filename))
        out.write(frame)
        print(f"Processed frame: {filename}")

    out.release()
    print("Build video done!")


def add_audio_to_video(original_video: str, processed_video: str, output_video: str):
    audio_file = "temp_audio.aac"
    subprocess.run(["bin/ffmpeg", "-y", "-i", original_video, "-q:a", "0", "-map", "a", audio_file])
    subprocess.run(["bin/ffmpeg", "-y", "-i", processed_video, "-i", audio_file, "-c:v", "copy", "-c:a", "aac", output_video])
    print("Added audio to video done!")
    os.remove(audio_file)


if __name__ == "__main__":
    main()