import os


def main() -> None:
    for folder in ["ranked_art", "original_art", "original_frames", "processed_frames"]:
        if not os.path.exists(folder):
            os.mkdir(folder)


if __name__ == "__main__":
    main()