import os
import shutil
import cv2
import numpy


def main() -> None:
    files = os.listdir("original_art")
    brightness_ranks = []

    for filename in files:
        if filename.endswith(".jpg") == False:
            continue

        gray = cv2.cvtColor(cv2.imread(f"original_art/{filename}"), cv2.COLOR_BGR2GRAY)
        brightness = numpy.mean(gray)
        brightness_ranks.append((filename, brightness))
        print(f"Ranked brightness: {filename}")

    brightness_ranks.sort(key=lambda x: x[1])

    if not os.path.exists("ranked_art"):
        os.mkdir("ranked_art")
    
    for rank, brightness_rank in enumerate(brightness_ranks):
        shutil.copyfile(f"original_art/{brightness_rank[0]}", f"ranked_art/{rank}.jpg")
        print(f"Copied brightness: {brightness_rank[0]}")

    print("Rank brightness done!")


if __name__ == "__main__":
    main()