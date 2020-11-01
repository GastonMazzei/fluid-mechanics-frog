import cv2
import os
import sys
import wave
import pylab

import numpy as np
import matplotlib.pyplot as plt
import datetime as dt


# Two functions for the spectrogram
def graph_spectrogram(wav_file,C):
    f,ax = pylab.subplots(1,figsize=(15, 5))
    sound_info, frame_rate = get_wav_info(wav_file)
    ax.specgram(sound_info,
                NFFT=1024, #default?
                Fs=frame_rate)
    f0 = 730
    modemax = 4
    ax.set_yticks([f0*i for i in range(1,modemax+1)])
    ax.set_yticklabels([f'Mode {i} - {round(i*f0/1000,1)} kHz' for i in range(1,modemax+1)])
    for i in range(1,modemax+1): ax.axhline(y=f0*i ,linewidth=1, color='r', ls='--', alpha=0.5)

    ax.set_ylim(0,5000)
    ax.axvline(x=C/frames_per_second ,linewidth=4, color='b')
    ax.tick_params(axis='y', colors='k',
                          width=25,
                          labelsize=20,
                             )
    plt.tight_layout()
    f.canvas.draw()
    image_from_plot = np.frombuffer(f.canvas.tostring_argb(), dtype=np.uint8)
    L = image_from_plot.shape[0]
    side = int(np.sqrt(L/12))
    plt.close(f)
    return image_from_plot.reshape(side,side*3, 4)

def get_wav_info(wav_file):
    wav = wave.open(wav_file, 'r')
    frames = wav.readframes(-1)
    sound_info = pylab.frombuffer(frames, 'int16')
    frame_rate = wav.getframerate()
    wav.close()
    return sound_info, frame_rate

# Create a timer function
def timer(a,b):
  T = (b-a)
  return f'{round(T.seconds+T.microseconds/1e6,2)}'

# Create a directory to store the edited video frames
try: 
  import os
  os.mkdir('temporal_frames')
except:
  pass

# Video parameters
input_video = cv2.VideoCapture('original/video.mp4')
frames_per_second = int(input_video.get(cv2.CAP_PROP_FPS))
frame_width = int(input_video.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(input_video.get(cv2.CAP_PROP_FRAME_HEIGHT))
no_of_frames = int(input_video.get(cv2.CAP_PROP_FRAME_COUNT))

# Add spectrogram to the video and save while iterating over frames
count = 1
x,y = 0,0
mapping = {1:3,2:2,3:1}
W,H = int(frame_width/1.5), int(frame_height /4 )
while count<=no_of_frames:
  ret, frame = input_video.read()
  ta = dt.datetime.now()
  img = graph_spectrogram('data/audio.wav',count)
  tb = dt.datetime.now()
  new = cv2.resize(
                 img, 
                 (W,H),
                 interpolation = cv2.INTER_AREA)
  for i in range(3):
    frame[x:x+H,y:y+W,i] = np.where(new[:,:,0]>0,new[:,:,mapping[i+1]],frame[x:x+H,y:y+W,i])
  tc = dt.datetime.now()
  cv2.imwrite(f'temporal_frames/frame-{count:03}.png',frame)
  td = dt.datetime.now()
  count += 1
  print('times were: ',timer(ta,tb), timer(tb,tc), timer(tc,td)) 
  if not ret:
    print('Processed all frames')
    break
