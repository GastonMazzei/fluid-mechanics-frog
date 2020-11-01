#!/bin/sh

echo "clearing old data..."
rm -r temporal_frames >> logs.txt
mkdir data >> logs.txt
rm data/audio.wav >> logs.txt
echo "Done!\nGenerating audio"
ffmpeg -i original/video.mp4 -ac 1 data/audio.wav >> logs.txt
echo "Done!\nGenerating frames... (this may take up to 5 minutes)"
python3 scripts/script.py >> logs.txt
echo "Done!\nGenerating video..."
mkdir output >> logs.txt
rm output/result.mp4 >> logs.txt
ffmpeg -framerate 30 -i temporal_frames/frame-%03d.png -i data/audio.wav -shortest output/result.mp4 >> logs.txt
echo "Done!\nRemoving old frames, audio and logs"
rm -r data
rm -r temporal_frames
rm logs.txt
echo "Done!\nIf 'xdg' is installed (Ubuntu-default); the video will now play"
xdg-open output/result.mp4
echo "Done!\nOutput video was saved in 'output/result.mp4'"
echo "ENDED"
