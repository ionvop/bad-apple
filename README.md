# bad-apple

A simple video processing pipeline designed to extract frames from a video, rank artworks based on their brightness, create a collage based on the extracted frames, and create a new video by combining the collage frames with audio. This project was used to make my Bad Apple video displayed with Touhou r34.

## Project Structure

```
.
├── bin
│   └── ffmpeg.exe      ← Download FFMPEG and place it here
├── original_art        ← Place artworks you want to use here
│   ├── art1.jpg
│   ├── art2.jpg
│   ├── art3.jpg
│   └── ...
├── build_frames.py
├── build_video.py
├── config.json         ← Configuration file
├── extract_frames.py
├── input.mp4
├── main.py
├── rank_brightness.py
└── requirements.txt
```

## Requirements

Download the FFMPEG binary and place it in the `bin` directory.

You can install the required Python packages using pip:

```bash
pip install -r requirements.txt
```

## Initialization

Place your input video as `input.mp4` in the root directory, and place all the artworks you want to use in the `original_art` directory as `.jpg` files.

## Configuration

Before running the project, you will need a `config.json` file that defines several parameters. Here's an example of what this file might contain:

```json
{
    "width": 960,
    "height": 720,
    "chunk_width": 40,
    "chunk_height": 40,
    "framerate": 15
}
```

- `width`: The width of the output video canvas.
- `height`: The height of the output video canvas.
- `chunk_width`: The width of each chunk in the output video.
- `chunk_height`: The height of each chunk in the output video.
- `framerate`: The desired frame rate for the output video.

## Usage

To start the processing, run the `main.py` script. This will execute the entire pipeline in sequence:

```bash
python main.py
```

### Steps in the Pipeline

1. **Extract Frames**: 
   - Extract frames from `input.mp4` and save them in the `original_frames` folder.

2. **Rank Brightness**: 
   - Read images from the `original_art` folder, rank them by their brightness, and save the sorted images in the `ranked_art` folder.

3. **Build Frames**: 
   - Combine the ranked images with the original frames to create a series of processed frames that are saved in the `processed_frames` folder.

4. **Build Video**: 
   - Assemble the processed frames into a video (`processed_video.mp4`) and add audio from the original video (`input.mp4`) to create the final output (`output.mp4`).

## Notes

- Ensure that your input video file (`input.mp4`) and any art images are placed correctly in the expected directories.