
import os
import sys
import subprocess
import datetime
import argparse
import json
from shutil import which

class VideoProcessor():
    def __init__(self, source_file):
        self.video_file = source_file
        self.video_object = None

    def getVideoStreamDuration (self) -> str:
        streamDuration = None
        for i in range(len(self.video_object)):
            
            if self.video_object['streams'][i]["codec_type"] == "video":
                streamDuration = str(self.video_object['streams'][i]["duration"])
                break
            elif self.video_object['streams'][i]["codec_type"] == "audio":
                streamDuration = str(self.video_object['streams'][i]["duration"])
                break
        formatedDuration =  datetime.datetime.strftime(datetime.datetime.strptime(streamDuration.strip(), "%H:%M:%S.%f"), "%H:%M:%S:%f")
        return formatedDuration

    def parseVideoData(self) -> datetime:
        '''Returns JSON of video duration requested from ffprobe'''

        attributes_request = "stream=codec_type,duration,width,height"
        
        stdout, stderr = subprocess.Popen(
            [
                "ffprobe", "-sexagesimal", "-print_format", "json",
                "-show_entries", attributes_request,
                self.video_file, "-sexagesimal"] , 
                universal_newlines=True, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE
                ).communicate() 
        self.video_object = json.loads(stdout)
        if self.video_object is not None:
            videoDuration = self.getVideoStreamDuration()
            if videoDuration:
                return videoDuration
            else:
                print("No attributes found")
                return None
        else:
            print("No attributes found")
            return None

def installed(program):
    ''' Check if a program is installed'''
    if which(program):
        return True
    else:
        return False



def generateTotalDuration(videoFileList):
    '''Get Duration and sum total'''
    aggregatedVideoDurations = []
    for file in videoFileList:        
        videoDuration = VideoProcessor(file).parseVideoData()
        aggregatedVideoDurations.append(videoDuration)


    sum = datetime.timedelta()
    for videoDuration in aggregatedVideoDurations:
        (h, m, s, ms) = videoDuration.split(':')

        durationTimeDelta = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s),microseconds=int(ms))
        sum += durationTimeDelta
    return datetime.datetime.strftime(datetime.datetime.strptime(str(sum),"%H:%M:%S.%f"), "%H:%M:%S.%f")        


acceptedFormats = ('.avi', '.mp4', '.mp3', '.mxf', '.mov', '.wav', '.aif')

if __name__ == "__main__":
    if not installed("ffprobe"):
        print("FFprobe Not Installed")
        exit(1)
    parser = argparse.ArgumentParser(description="A program that generates metadata summaries and can extract audio from video files")
    parser.add_argument("-f", "--files", nargs="*", help="Indivudal files or directories to process")

    args = parser.parse_args()

    fileList = [] #Create list of files to process.
    for files in args.files:
        if os.path.isdir(files):
            directoryFiles = sorted(os.listdir(files))
            for file in directoryFiles:
                if file.lower().endswith(acceptedFormats):
                    fileList.append(os.path.join(files, file))
        elif os.path.isfile(files):
            if files.lower().endswith(acceptedFormats):
                fileList.append(os.path.abspath(files))

    sourceFiles = sorted(fileList)
    if not sourceFiles:
        print('No accepted files found. Drag files or folders or both.')
    else:
        totalDuration = generateTotalDuration(sourceFiles)
        print(totalDuration)
        