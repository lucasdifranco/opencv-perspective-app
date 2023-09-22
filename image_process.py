import os
import cv2
import numpy as np
from PIL import Image, ImageTk
import io

class image_process:
    '''
    Classe feita para acomodar funções de processamento de imagem, desde demostração na interface até seu salvamento.
    '''
    def __init__(self,image:Image, resized_image:Image, points:list, canvas2 , image_paths, src_img_path:str) -> None:

        self.image = image
        self.resized_image = resized_image
        self.points = points
        self.canvas2 = canvas2
        self.image_paths = image_paths
        self.src_img_path = src_img_path

    def perspective_calculation(self):
        '''
            Transforma a imagem para perspectiva.

            Parameters:
                image (img): imagem original;
                resized_image (img): imagem apresentada no programa;
                points (list): lista de pontos para montar perspectiva;
                canvas2 (Tk.canvas): canvas onde aparece resized_image.

            Returns:
                pil_image (img): retorna PIL Image.
        '''

        # calculo da razão da imagem
        aspect_ratio = self.image.width / self.resized_image.width
        
        # ajustando pontos de acordo com aspect_ratio
        adjusted_points = [(x * aspect_ratio, y * aspect_ratio) for x, y in self.points]
        
        # pontos -> numpy array
        src_points = np.array(adjusted_points, dtype=np.float32)
        
        # dimensões de canvas2
        self.canvas2_width = self.canvas2.winfo_reqwidth()
        self.canvas2_height = self.canvas2.winfo_height()
        
        # pontos de canvas2 -> numpy array
        dst_points = np.array([(0, 0), (self.canvas2_width, 0), (self.canvas2_width, self.canvas2_height), (0, self.canvas2_height)], dtype=np.float32)
        
        # cria a matriz de perspectiva com src_points e dst_points
        self.perspective_matrix = cv2.getPerspectiveTransform(src_points, dst_points)

    def transform_img(self):
        '''
        Pela perspectiva calculada, gera a imagem transformada.

        Parameters:
            image (img): imagem original
        Returns:
            trasnformed_img (photo_img): imagems para tkinter
        '''
        self.perspective_calculation()
        # transforma imagem
        original_image = np.array(self.image)
        transformed_image = cv2.warpPerspective(original_image, self.perspective_matrix, (self.canvas2_width, self.canvas2_height))
        
        self.pil_image = Image.fromarray(transformed_image)
        
    def img_show(self) -> ImageTk.PhotoImage:
        '''
        Transforma a imagem para ser visualizada na interface.

        Parameters:
            pil_image (img): imagem trasnformada
        Returns:
            trasnformed_img (photo_img): imagems para tkinter
        '''
        self.transform_img()
        # PIL img -> PhotoImage

        # Create a PhotoImage from the converted bytes
        transformed_img = ImageTk.PhotoImage(self.pil_image)

        return transformed_img

    def save_single(self) -> None:
        '''
        Salva a imagem em perspectiva.
        
        Parameters:
            src_img_path (path): Caminho da imagem original.

        Returns:
            None

        '''
        self.transform_img()
        src_img_path = self.src_img_path.replace('.jpg','_pp.jpg')
        self.pil_image.save(src_img_path)
        print('Imagem Salva!')

    def save_bach(self) -> None:
        '''
        Salva imagens em loop de acordo com save_single.
            -> cria lista com caminho das imagens
            -> roda save_single em loop para salvar as imagens

        Parameters:
            folder_path (path): Caminho da pasta com imagens
        
        '''
        for image_path in self.image_paths:
            self.image = Image.open(image_path)
            self.src_img_path = image_path
            self.save_single()