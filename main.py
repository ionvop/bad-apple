import extract_frames
import rank_brightness
import build_frames
import build_video


def main() -> None:
    extract_frames.main()
    rank_brightness.main()
    build_frames.main()
    build_video.main()


if __name__ == "__main__":
    main()