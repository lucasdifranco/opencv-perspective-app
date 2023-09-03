import os


def gather_info(file_path:str) -> [str,list]:
    '''
        Abre pasta do vídeo e retorna elementos para análise.

        Parameters: 
            file_path (path): Recebe caminho da pasta.

        Returns:
            camera_folder (str): Retorna str com caminho de pasta;
            FOTOS (list): Retorna lista com nome das fotos.
    '''
    # --- CAMERA 1 --- #

    camera_path = file_path
    FOTOS = []
    for photo in os.listdir(camera_path):
        if photo.endswith('.jpg'):
            FOTOS.append(os.path.join(photo))

    return camera_path,FOTOS

def ajuste_kms(camera_folder:str,FOTOS:list) -> list:
    '''
        Recebe parâmetros da pasta do vídeo e retorna infos de odometro e quilômetro.

        Parameters: 
            camera_folder (str): Recebe str com caminho de pasta
            FOTOS (list): Recebe lista com nome das fotos

        Returns:
            trecho_list (list): Retorna lista com quilômetro atrelado à foto.
    '''
    trecho_list = []
    
    for photo in (FOTOS):
        photo_path = os.path.join(camera_folder[0],str(photo))

        trecho_list.append((photo_path))

        ''' OBSERVAÇÃO:
            -> PARA PEGAR O VALOR DA COLUNA 1 DA LISTA, UTILIZAR LISTA[0][0], SENDO O PRIMEIO [0] O INDICE E O SEGUNDO PARA NÚMERO DA COLUNA
            -> LISTA[i][0] === caminho_foto
        '''
    return trecho_list