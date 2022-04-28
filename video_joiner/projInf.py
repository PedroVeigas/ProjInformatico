import tkinter
from tkinter import filedialog #para abrir o explorador ficheiros
import os #para mudar a diretoria de trabalho
from moviepy.editor import VideoFileClip, concatenate_videoclips
import sys
sys.setrecursionlimit(10000)

working_dir = os.getcwd()

tkinter.Tk().withdraw()

folder_path=filedialog.askdirectory() #vai buscar a pasta selecionada pelo utilizador

folder_path+='record/'
os.chdir(folder_path) #muda a diretoria trabalho

folders=os.listdir(folder_path)

#print("Current working directory: {0}".format(os.getcwd()))

#print(folders)

#https://stackoverflow.com/questions/973473/getting-a-list-of-all-subdirectories-in-the-current-directory
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

all_folders = get_all_dirs(folder_path)
all_files_in_folders = get_all_mp4_files_in_dirs(all_folders)
#print(all_files_in_folders)
#print(len(all_files_in_folders))

os.chdir(working_dir)

final_clip = VideoFileClip(all_files_in_folders[0])
for i in range(1,len(all_files_in_folders)-270):
    """
    if (i % 200) == 0:
        final_clip.write_videofile('myvideo'+str(int(i/200))+'.mp4')
        final_clip = VideoFileClip('myvideo'+str(int(i/200))+'.mp4')
    """
    last_clip = VideoFileClip(all_files_in_folders[i])
    final_clip = concatenate_videoclips([final_clip, last_clip])
    print('\r' + str(i+1) + '/' + str(len(all_files_in_folders)-270), end='')

final_clip.write_videofile("final.mp4")
