import os
import sys, getopt
import ffmpeg
from pathlib import Path

def get_all_dirs(dirname):
    subfolders = [f.path for f in os.scandir(dirname) if f.is_dir()]
    for dirname in list(subfolders):
        subfolders.extend(get_all_dirs(dirname))
    return subfolders


def get_all_mp4_files_in_dirs(all_dirs):
    all_mp4_files = []
    for i in all_dirs:
        files_in_dir=os.listdir(i)
        for u in files_in_dir:
            if os.path.getsize(i+"\\"+u) == 0:
                continue
            filename, file_extension = os.path.splitext(u)
            if file_extension.lower() == '.mp4':
                all_mp4_files.append(i+"\\"+filename+file_extension)
    return all_mp4_files


def ffmpeg_joiner(videos_to_join, out_file_name):
    working_dir = os.getcwd()
    if not os.path.exists(working_dir+'\\joined_videos'):
        os.mkdir(working_dir+'\\joined_videos')
    with open("joined_videos\\temp_videos_paths.txt", "w", encoding="utf-8") as f:
        for video in videos_to_join:
            f.write("file '"+video+"'\n")

    outFile = Path(working_dir+'\\joined_videos\\'+out_file_name+'.mp4')

    input_files_path = Path(working_dir+'\\joined_videos\\temp_videos_paths.txt')

    ffInput = ffmpeg.input(input_files_path, format='concat', safe=0)

    params =    {
                'c:a': 'aac'
                }
    
    ffOutput = ffInput.output(outFile.as_posix(), **params)

    #ffOutput = ffOutput.global_args('-loglevel', 'error')

    ffOutput.run(overwrite_output=True)

    os.remove(input_files_path)

def join_videos_by_day(folder_path):
    subfolders = [f.path for f in os.scandir(folder_path+"record\\") if f.is_dir()]
    for subfolder in subfolders:
        all_folders = get_all_dirs(subfolder)
        all_files_in_folders = get_all_mp4_files_in_dirs(all_folders)
        video_name = subfolder.split("\\")[-1]
        video_name = video_name[-2:] +"-"+ video_name[4:6] +"-"+ video_name[:-4]
        ffmpeg_joiner(all_files_in_folders, "Video_dia_"+video_name)


def join_videos_by_hour(folder_path):
    subfolders = [f.path for f in os.scandir(folder_path+"record\\") if f.is_dir()]
    for subfolder in subfolders:
        hour=[f.path for f in os.scandir(subfolder) if f.is_dir()]
        for i in hour:
                all_folders = get_all_dirs(i)
                all_files_in_folders = get_all_mp4_files_in_dirs(all_folders)
                video_day = i.split("\\")[-2]
                video_day = video_day[-2:] +"-"+ video_day[4:6] +"-"+ video_day[:-4]
                video_name="Video_dia_"+video_day+"_"+i.split("\\")[-1]+"H"
                ffmpeg_joiner(all_files_in_folders, video_name)


def main(argv):
    try:
        opts, args = getopt.getopt(argv,"hp:dt",["help","path=","day","thour"])
    except getopt.GetoptError:
        print('\nInvalid argument!\nUse -h to see the possible arguments to insert.\n')
        sys.exit(0)
    if not opts:
        print('\nNo argument passed!\nUse -h to see the possible arguments to insert.\nShutting down...\n')
        sys.exit(0)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print('\n-- Video Joiner --')
            print('Arguments accepted by the Script:')
            print('--help (-h): To see the available arguments.\n')
            print('--path (-p) <PATH>: The path to search the videos.')
            sys.exit(0)
        elif opt in ("-p", "--path"):
            folder_path = arg
        elif opt in ("-d", "--day"):
            join_videos_by_day(folder_path)
            sys.exit(0)
        elif opt in ("-t", "--thour"):
            join_videos_by_hour(folder_path)
            sys.exit(0)


    all_folders = get_all_dirs(folder_path)
    all_files_in_folders = get_all_mp4_files_in_dirs(all_folders)

    ffmpeg_joiner(all_files_in_folders, "All_Videos")



if __name__ == "__main__":
   main(sys.argv[1:])