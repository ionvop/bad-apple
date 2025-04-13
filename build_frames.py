import os
import cv2
import numpy
import random
import json


def main() -> None:
    random.seed(42)
    config = json.load(open("config.json"))
    canvas_width = config["width"]
    canvas_height = config["height"]
    chunk_width = config["chunk_width"]
    chunk_height = config["chunk_height"]
    art_images = {}
    images = os.listdir("ranked_art")
    images = sorted([image for image in images if image.endswith(".jpg")])
    image_count = len(images)

    for image_id in range(image_count):
        image = cv2.imread(f"ranked_art/{image_id}.jpg")
        art_images[image_id] = resize_and_crop_cover(image, chunk_width, chunk_height)

    files = sorted([
        file for file in os.listdir("original_frames")
        if file.endswith(".jpg")
    ])

    id_map = [[0] * (canvas_width // chunk_width) for _ in range(canvas_height // chunk_height)]
    image_map = [[0] * (canvas_width // chunk_width) for _ in range(canvas_height // chunk_height)]
    lower_bag = create_bag(0, (image_count // 2) - 1)
    upper_bag = create_bag(image_count // 2, image_count - 1)

    for y in range(canvas_height // chunk_height):
        for x in range(canvas_width // chunk_width):
            image_map[y][x] = get_from_bag(lower_bag, 0, (image_count // 2) - 1)

    if not os.path.exists("processed_frames"):
        os.mkdir("processed_frames")

    for file in files:
        canvas = numpy.zeros((canvas_height, canvas_width, 3), dtype=numpy.uint8)
        frame = cv2.imread(f"original_frames/{file}")
        original_height, original_width = frame.shape[:2]

        for y in range(canvas_height // chunk_height):
            for x in range(canvas_width // chunk_width):
                rel_y = int(((y * chunk_height) + (chunk_height // 2)) * (original_height / canvas_height))
                rel_x = int(((x * chunk_width) + (chunk_width // 2)) * (original_width / canvas_width))
                rel_y = min(rel_y, original_height - 1)
                rel_x = min(rel_x, original_width - 1)
                pixel = frame[rel_y, rel_x]
                brightness = numpy.mean(pixel)

                if brightness > 128:
                    if id_map[y][x] == 0:
                        image_map[y][x] = get_from_bag(upper_bag, image_count // 2, image_count - 1)
                        id_map[y][x] = 1
                else:
                    if id_map[y][x] == 1:
                        image_map[y][x] = get_from_bag(lower_bag, 0, (image_count // 2) - 1)
                        id_map[y][x] = 0

                image_id = image_map[y][x]
                fitted = art_images[image_id]
                canvas[y * chunk_height:(y * chunk_height) + chunk_height, x * chunk_width:(x * chunk_width) + chunk_width] = fitted

        cv2.imwrite(f"processed_frames/{file}", canvas)
        print(f"Processed frame: {file}")

    print("Build frames done!")


def resize_and_crop_cover(image: cv2.typing.MatLike, target_width: int, target_height: int) -> cv2.typing.MatLike:
    src_h, src_w = image.shape[:2]
    target_ratio = target_width / target_height
    src_ratio = src_w / src_h

    if src_ratio > target_ratio:
        scale = target_height / src_h
    else:
        scale = target_width / src_w

    resized = cv2.resize(image, (int(src_w * scale), int(src_h * scale)))
    mid_x, mid_y = resized.shape[1] // 2, resized.shape[0] // 2
    half_w, half_h = target_width // 2, target_height // 2
    cropped = resized[mid_y - half_h:mid_y + half_h, mid_x - half_w:mid_x + half_w]
    return cropped


def create_bag(start: int, end: int) -> list[int]:
    bag = list(range(start, end + 1))
    random.shuffle(bag)
    return bag


def get_from_bag(bag: list[int], start: int, end: int) -> int:
    if not bag:
        bag.extend(create_bag(start, end))

    return bag.pop()


if __name__ == "__main__":
    main()