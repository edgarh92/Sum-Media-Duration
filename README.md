
# Sum Media Duration

Sum Media Duration is a command line utility to get the total duration of your video or audio files. This will be useful when working with many small files. It uses ffprobe to pull the duration from the video and audio stream and the datetime module to add the values up. Creators may use the tool to quickly see the total length of files that would be used in for social media video (like Tik Tok or Instagram reel) and if they would need to trim the video to their desired length. 


## Run Locally

Clone the project

```bash
  git clone https://github.com/edgarh92/Sum-Media-Duration
```

Go to the project directory

```bash
  cd Sum-Media-Duration
```

Install dependencies if needed. 

```bash
  brew install ffprobe
```

Run the script

```bash
  python3 sum_media_duration.py -f directory/
```

