import os #para mudar a diretoria de trabalho
import sys, getopt
import ffmpeg
from pathlib import Path


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

            #A camera cria todos os ficheiros para o determinado minuto
            #Caso seja desligada a meio, ficam ficheiros vazios na diretoria que iriam criar erros na junção de videos
            #Assim, todos os ficheiros com 0 Kb irão ser ignorados
            if os.path.getsize(i+"\\"+u) == 0:
                continue

            #Verifica se a extenção do ficheiro é .mp4
            #Caso seja, adiciona à lista all_mp4_files[] com o caminho ("path") completo do ficheiro
            filename, file_extension = os.path.splitext(u)
            if file_extension.lower() == '.mp4':
                all_mp4_files.append(i+"\\"+filename+file_extension)
    return all_mp4_files


def ffmpeg_joiner(videos_to_join, out_file_name):
    #Guarda a diretoria onde o ficheiro .py está a ser executado
    working_dir = os.getcwd()
    
    #Caso não exista a diretoria "joined_videos" vai ser criada
    if not os.path.exists(working_dir+'\\joined_videos'):
        os.mkdir(working_dir+'\\joined_videos')
    
    #Escreve no ficheiro temp_videos_paths os caminhos dos vídeos
    with open("joined_videos\\temp_videos_paths.txt", "w", encoding="utf-8") as f:
        for video in videos_to_join:
            f.write("file '"+video+"'\n")


    #https://stackoverflow.com/questions/17668996/python-how-to-join-multiple-video-files
    # set output filename
    outFile = Path(working_dir+'\\joined_videos\\'+out_file_name+'.mp4')

    # create file object that will contain files for ffmpeg to concat
    input_files_path = Path(working_dir+'\\joined_videos\\temp_videos_paths.txt')

    # this seems to be the proper concat input, with the path containing the list
    # of files for ffmpeg to concat, along with the format parameter, and safe, if i
    # read the docs correctly, is default/optional
    ffInput = ffmpeg.input(input_files_path, format='concat', safe=0)

    # output parameters
    params =    {
                'c:a': 'aac'
                }
    
    # input stream -> output stream with output filename and expanded params
    ffOutput = ffInput.output(outFile.as_posix(), **params)

    # something, something, run.
    ffOutput.run(overwrite_output=True)

    #Removing temp file of videos paths
    os.remove(input_files_path)


def join_videos_by_day():
    subfolders = [f.path for f in os.scandir("F:\\record") if f.is_dir()]
    for subfolder in subfolders:
        all_folders = get_all_dirs(subfolder)
        all_files_in_folders = get_all_mp4_files_in_dirs(all_folders)
        video_name = subfolder.split("\\")[-1]
        video_name = video_name[-2:] +"-"+ video_name[4:6] +"-"+ video_name[:-4]
        ffmpeg_joiner(all_files_in_folders, "Video_dia_"+video_name)


def join_videos_by_hour():
    subfolders = [f.path for f in os.scandir("F:\\record") if f.is_dir()]
    for subfolder in subfolders:
        hour=[f.path for f in os.scandir(subfolder) if f.is_dir()]
        for i in hour:
                all_folders = get_all_dirs(i)
                all_files_in_folders = get_all_mp4_files_in_dirs(all_folders)
                video_day = i.split("\\")[-2]
                video_day = video_day[-2:] +"-"+ video_day[4:6] +"-"+ video_day[:-4]
                video_name="Video_dia_"+video_day+"_"+i.split("\\")[-1]+"H"
                print(video_name)
                ffmpeg_joiner(all_files_in_folders, video_name)


def main(argv):
    try:
        opts, args = getopt.getopt(argv,"hp:di",["help","path=","day","ihour"])
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
        elif opt in ("-d", "--day"):
            join_videos_by_day()
            sys.exit(0)
        elif opt in ("-i", "--ihour"):
            join_videos_by_hour()
            sys.exit(0)


    #Executar as funções para obter todos os ficheiros .mp4
    all_folders = get_all_dirs(folder_path)
    all_files_in_folders = get_all_mp4_files_in_dirs(all_folders)

    #Executar a função para juntar os vídeos
    ffmpeg_joiner(all_files_in_folders, "All_Videos")



if __name__ == "__main__":
   main(sys.argv[1:])