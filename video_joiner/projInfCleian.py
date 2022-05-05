import os
import sys, getopt
import ffmpeg
from pathlib import Path

def main(argv):
    try:
        opts, args = getopt.getopt(argv,"hp:",["help","path="])
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
            print('--path (-p) <PATH>: The path to search the videos.')
            print('--help (-h): To see the available arguments.\n')
            sys.exit(0)
        elif opt in ("-p", "--path"):
            folder_path = arg


    working_dir = os.getcwd()


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
                filename, file_extension = os.path.splitext(u)
                if file_extension.lower() == '.mp4':
                    all_mp4_files.append(i+"\\"+filename+file_extension)
        return all_mp4_files
    

    def ffmpeg_joiner(videos_to_join):
        with open("temp_videos_paths.txt", "w", encoding="utf-8") as f:
            for video in videos_to_join:
                f.write("file '"+video+"'\n")


        outFile = Path(working_dir+'\\final.mp4')

        input_files_path = Path(working_dir+'\\temp_videos_paths.txt')

        ffInput = ffmpeg.input(input_files_path, format='concat', safe=0)

        params =    {
                    'c:a': 'aac'
                    }
        
        ffOutput = ffInput.output(outFile.as_posix(), **params)

        ffOutput.run(overwrite_output=True)

        os.remove(input_files_path)

    all_folders = get_all_dirs(folder_path)
    all_files_in_folders = get_all_mp4_files_in_dirs(all_folders)

    ffmpeg_joiner(all_files_in_folders)



if __name__ == "__main__":
   main(sys.argv[1:])