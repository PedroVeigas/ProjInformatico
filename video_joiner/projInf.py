import tkinter
from tkinter import filedialog #para abrir o explorador ficheiros
import os #para mudar a diretoria de trabalho
from moviepy.editor import VideoFileClip, concatenate_videoclips #procurar saber se é preciso gpu para ser utilizado
import sys
sys.setrecursionlimit(10000)

#Guarda a diretoria onde o ficheiro .py está a ser executado
working_dir = os.getcwd()

tkinter.Tk().withdraw()

folder_path=filedialog.askdirectory() #Vai buscar a pasta selecionada pelo utilizador

folder_path+='record/'
os.chdir(folder_path) #Muda a diretoria trabalho

#Lista todos os ficheiros da diretoria corrente
folders=os.listdir(folder_path)

#print("Current working directory: {0}".format(os.getcwd()))
#print(folders)

#https://stackoverflow.com/questions/973473/getting-a-list-of-all-subdirectories-in-the-current-directory
#Função retirada do stackoverflow, que retorna todas as diretorias e subdiretorias da pasta selecionada
#A função é recursiva, em que vai sempre ser chamada até sejam listadas todas as subdiretorias de uma diretoria
#Todas estas diretorias são adicionadas à lista subfolders[]
def get_all_dirs(dirname):
    subfolders = [f.path for f in os.scandir(dirname) if f.is_dir()]
    for dirname in list(subfolders):
        subfolders.extend(get_all_dirs(dirname))
    return subfolders

#Função que retorna todos os ficheiros .mp4 encontrados nas diretorias e subdiretorias da pasta selecionada
def get_all_mp4_files_in_dirs(all_dirs):
    #Incialização da lista
    all_mp4_files = []

    #Percorrer todas as diretorias e subdiretorias retornadas pela função get_all_dirs()
    for i in all_dirs:

        #Lista os ficheiros contidos na diretoria que está a analizar
        files_in_dir=os.listdir(i)

        #Percorre cada ficheiro da diretoria
        for u in files_in_dir:

            #Verifica se a extenção do ficheiro é .mp4
            #Caso seja, adiciona à lista all_mp4_files[] com o caminho ("path") completo do ficheiro
            filename, file_extension = os.path.splitext(u)
            if file_extension.lower() == '.mp4':
                all_mp4_files.append(i+"\\"+filename+file_extension)
    return all_mp4_files

#Executar as funções para obter todos os ficheiros .mp4
all_folders = get_all_dirs(folder_path)
all_files_in_folders = get_all_mp4_files_in_dirs(all_folders)

#Muda a diretoria para a diretoria onde o .py está a ser executado
#Assim o video completo será criado no mesmo sitio do script python
os.chdir(working_dir)

#Agora vai juntar todos os videos em apenas um
#Quando fizemos este script, existiam cerca de 278 vídeos
#Como são muitos vídeos, este processo é um pouco demorado, decidimos apenas juntar 8 vídeos para fazer a demonstração
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
