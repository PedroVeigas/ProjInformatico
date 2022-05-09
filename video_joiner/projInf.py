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

    # make ffmpeg quiet
    #ffOutput = ffOutput.global_args('-loglevel', 'error')

    # something, something, run.
    ffOutput.run(overwrite_output=True)

    #Removing temp file of videos paths
    os.remove(input_files_path)


#Como funcionam as diretorias:
#Dentro do disco temos 2 pastas, apenas nos interessa a pasta "record"
#Dentro da pasta "record", temos os vídeos separados pelo dia que foram gravados
#Dentro de uma das pastas do dia da gravação, encontramos os vídeos separados pela hora da gravação

#Função que vai organizar e juntar os vídeos por dia
def join_videos_by_day(folder_path):
    #Procura na pasta "record" pelas subpastas dos dias de gravação
    subfolders = [f.path for f in os.scandir(folder_path+"record\\") if f.is_dir()]

    #Vai percorrer cada um desses dias
    for subfolder in subfolders:

        #Procura todas as subpastas
        all_folders = get_all_dirs(subfolder)

        #Procura todos os ficheiros .mp4 dessa pasta e das suas subpastas
        all_files_in_folders = get_all_mp4_files_in_dirs(all_folders)

        #Algoritmo para dar o nome ao vídeo final, neste caso vai ser "Vido_dia_DIA-MÊS-ANO"
        video_name = subfolder.split("\\")[-1]
        video_name = video_name[-2:] +"-"+ video_name[4:6] +"-"+ video_name[:-4]

        #Chamda da função que vai juntar os vídeos encontrados, recebe como parametros a lista de vídeos e o nome do vídeo final
        ffmpeg_joiner(all_files_in_folders, "Video_dia_"+video_name)


def join_videos_by_hour(folder_path):
    #Procura na pasta "record" pelas subpastas dos dias de gravação
    subfolders = [f.path for f in os.scandir(folder_path+"record\\") if f.is_dir()]

    #Vai percorrer cada um desses dias
    for subfolder in subfolders:

        #Procura na pasta do dia pelas subpastas das horas de gravação
        hours=[f.path for f in os.scandir(subfolder) if f.is_dir()]

        #Percorre cada uma dessas horas
        for hour in hours:

                #Procura todas as subpastas
                all_folders = get_all_dirs(hour)

                #Procura todos os ficheiros .mp4 dessa pasta e das suas subpastas
                all_files_in_folders = get_all_mp4_files_in_dirs(all_folders)

                #Algoritmo para dar o nome ao vídeo final, neste caso vai ser "Vido_dia_DIA-MÊS-ANO_HORAH"
                video_day = hour.split("\\")[-2]
                video_day = video_day[-2:] +"-"+ video_day[4:6] +"-"+ video_day[:-4]
                video_name="Video_dia_"+video_day+"_"+hour.split("\\")[-1]+"H"

                #Chamda da função que vai juntar os vídeos encontrados, recebe como parametros a lista de vídeos e o nome do vídeo final
                ffmpeg_joiner(all_files_in_folders, video_name)


def main(argv):

    #Definir quais os argumentos vão existir no Script
    try:
        opts, args = getopt.getopt(argv,"hp:dt",["help","path=","day","thour"])

    #Caso o argumento não seja nenhum dos argumentos possíveis
    except getopt.GetoptError:
        print('\nInvalid argument!\nUse -h to see the possible arguments to insert.\n')
        sys.exit(0)

    #Caso não sejam passados argumentos, apresenta mensagem de erro
    if not opts:
        print('\nNo argument passed!\nUse -h to see the possible arguments to insert.\nShutting down...\n')
        sys.exit(0)
    
    #Tratamento dos argumentos
    for opt, arg in opts:

        #Caso o argumento seja o -h(--help)
        if opt in ("-h", "--help"):
            print('\n-- Video Joiner --')
            print('Arguments accepted by the Script:\n')
            print('--help (-h): To see the available arguments.\n')
            print('--path (-p) <PATH>: The path to search the videos.\n')
            print('--day (-d): To join videos by day.\n')
            print('--thour (-t): To join videos by hour.\n')
            sys.exit(0)

        #Caso o argumento seja o -p(--path)
        elif opt in ("-p", "--path"):
            folder_path = arg

        #Caso o argumento seja o -d(--day)
        elif opt in ("-d", "--day"):
            join_videos_by_day(folder_path)
            sys.exit(0)

        #Caso o argumento seja o -t(--thour)
        elif opt in ("-t", "--thour"):
            join_videos_by_hour(folder_path)
            sys.exit(0)

    #Caso não seja inserido nenhum dos argumentos para juntar os vídeos ou
    #por hora ou por dia, o Script irá juntar todos os vídeos em apenas um 
    #vídeo só

    #Executar as funções para obter todos os ficheiros .mp4
    all_folders = get_all_dirs(folder_path)
    all_files_in_folders = get_all_mp4_files_in_dirs(all_folders)

    #Executar a função para juntar os vídeos
    ffmpeg_joiner(all_files_in_folders, "All_Videos")


#Chamada da função main passando os argumentos
if __name__ == "__main__":
   main(sys.argv[1:])