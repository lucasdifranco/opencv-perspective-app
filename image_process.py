import os
import cv2
import numpy as np
from PIL import Image, ImageTk

def img_trasnform(image:Image, resized_image:Image, points:list, canvas2) -> ImageTk.PhotoImage:
    '''
    '''

    # Calculate the aspect ratio between the original image and the resized image.
    aspect_ratio = image.width / resized_image.width
    
    # Adjust points for the calculated aspect ratio.
    adjusted_points = [(x * aspect_ratio, y * aspect_ratio) for x, y in points]
    
    # Convert adjusted points to a numpy array.
    src_points = np.array(adjusted_points, dtype=np.float32)
    
    # Calculate the dimensions of canvas2.
    canvas2_width = canvas2.winfo_reqwidth()
    canvas2_height = canvas2.winfo_height()
    
    # Define a numpy array for the dimensions of canvas2.
    dst_points = np.array([(0, 0), (canvas2_width, 0), (canvas2_width, canvas2_height), (0, canvas2_height)], dtype=np.float32)
    
    # Create a perspective matrix with points from the image and canvas2.
    perspective_matrix = cv2.getPerspectiveTransform(src_points, dst_points)
    
    # Transform the image.
    original_image = np.array(image)
    transformed_image = cv2.warpPerspective(original_image, perspective_matrix, (canvas2_width, canvas2_height))
    
    # Convert the transformed image to a PIL Image.
    pil_image = Image.fromarray(transformed_image)
    
    # Convert the PIL Image to a PhotoImage.
    transformed_photo = ImageTk.PhotoImage(pil_image)
    
    return transformed_photo

def save_single(src_img_path:os.path) -> None:
    '''
    Salva a imagem em perspectiva.
    
    Parameters:
        src_img_path (path): Caminho da imagem original.

    Returns:
        None

    '''

def save_bach(folder_path:os.path) -> None:
    '''
    Salva imagens em loop de acordo com save_single.
        -> cria lista com caminho das imagens
        -> roda save_single em loop para salvar as imagens

    Parameters:
        folder_path (path): Caminho da pasta com imagens
    
    '''