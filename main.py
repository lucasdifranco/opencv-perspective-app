
import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk
import os
import video_config

class perspective_app(tk.Tk):

    def __init__(self, root:tk) -> None:
        '''
            Cria início para interface.

            Returns:
                None
        '''

        # Definição inicial da tela principal
        self.root = root
        self.image = None
        self.root.title("Transformação de Perspectiva")
        root_w = int(1100)
        root_h = int(670)
        self.root.geometry((str(root_w) + 'x' + str(root_h)))
        self.root.resizable(height = False, width = False)
        # Define que inicialmente não existem pontos selecionados pelo usuário
        self.selected_points = 0
        self.image_paths = []
        self.current_image_index = -1
        self.trecho_list = []
        self.current_image_index = 0
        
        # Criação do canvas2, onde é mostrada a imagem planada
        canvas2_width = 614
        canvas2_height = canvas2_width
        self.canvas2 = tk.Canvas(root, width=canvas2_width, height=canvas2_height, bg="grey")
        self.canvas2.place(x=10, y=10)  # Usa o método place para definir a posição fixa

        # Calcula o tamanho do canvas1 com base no espaço restante na tela
        self.canvas1_width = abs(root_w - canvas2_width - 40)
        self.canvas1_height = int(self.canvas1_width*0.564)
        canvas1_x = self.canvas2.winfo_reqwidth() + 20

        # Criação do canvas1 com o tamanho calculado
        self.canvas1 = tk.Canvas(root, width=self.canvas1_width, height=self.canvas1_height, bg="grey")
        self.canvas1.place(x=canvas1_x, y=9)

        # Criação do canvas3 com o tamanho calculado
        self.canvas3 = tk.Canvas(root, width = (root_w - 20), height = (root_h - canvas2_height - 30), bg="grey")
        self.canvas3.place(x=10, y=canvas2_height + 20)

        # Criação do canvas4 com o tamanho calculado
        self.canvas4 = tk.Canvas(root, width = self.canvas1_width, height = (canvas2_height - self.canvas1_height - 12))#, bg="grey")
        self.canvas4.place(x = canvas1_x , y = (self.canvas1_height + 20))

        # Botão para abrir a imagem
        self.load_button = tk.Button(self.canvas4, text="Load Folder", command=self.load_folder, height= 1, width= 20)
        self.load_button.place(x=5, y=325)

        # Botão para salvar parametros
        self.save_parameters = tk.Button(self.canvas4, text="Save", height= 1, width= 20)
        self.save_parameters.place(x=170, y=95)

        # Input Largura
        self.width_label = ttk.Label(self.canvas4, text='Width')
        self.width_label.place(x=10,y=80)
        self.width_entry = tk.Entry(self.canvas4, width= 5)
        self.width_entry.place(x=10,y=100)

        self.x_label = tk.Label(self.canvas4, text='X')
        self.x_label.place(x=55,y=100)

        # Input Altura
        self.height_label = tk.Label(self.canvas4, text='Height')
        self.height_label.place(x=80,y=80)
        self.height_entry = tk.Entry(self.canvas4, width= 5)
        self.height_entry.place(x=80,y=100)

        self.selected_corner = None
        self.points = [(0, 0),
            (self.canvas1_width, 0),
            (self.canvas1_width, self.canvas1_height),
            (0, self.canvas1_height)
        ]

        self.root.bind("<Next>", self.next_image)
        self.root.bind("<Prior>", self.prev_image)
        self.canvas1.bind("<Button-1>", self.on_mouse_press)
        self.canvas1.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas1.bind("<ButtonRelease-1>", self.on_mouse_release)

        

# ========= Botões ========== #

    def load_folder(self) -> None:
        '''
            Carrega pasta na interface, obtendo valores de gather_info()

            Se na pasta carregada existe fotos, ativa funções: 
               ->  update_points()
               ->  load_and_display_current_image()
               ->  transform_image()

            Parameters: 
                folder_path (path): Recebe caminho por askdirectory.

            Returns:
                None

        '''

        folder_path = filedialog.askdirectory()

        if folder_path:
            camera_folder, fotos = video_config.gather_info(folder_path)
            self.image_paths = [os.path.join(camera_folder, photo) for photo in fotos]
            self.trecho_list = video_config.ajuste_kms(camera_folder, fotos)
            self.current_image_index = 0

            if self.image_paths:
                self.update_points()
                self.load_and_display_current_image()
                self.transform_image()

    def next_image(self, event) -> None:
        '''
            Atualiza self.current_image_index para índice da foto atual, mostra e trasnforma a imagem atualizada.  
        
            Parameters: 
                event (event): Bind (Page Down);
                current_image_index (var): Recebe índice mais atualizado das fotos.

            Returns:
                None
        '''
        
        self.current_image_index += 1
        if self.current_image_index >= len(self.image_paths):
            self.current_image_index = self.current_image_index

        self.load_and_display_current_image()
        self.transform_image()

    def prev_image(self, event) -> None:
        '''
            Atualiza self.current_image_index para índice da foto atual, mostra e trasnforma a imagem atualizada.  
        
            Parameters: 
                event (event): Bind (Page Up);
                current_image_index (var): Recebe índice mais atualizado das fotos.

            Returns:
                None
        '''

        self.current_image_index -= 1
        if self.current_image_index < 0:
            self.current_image_index = self.current_image_index

        self.load_and_display_current_image()
        self.transform_image()

    def on_mouse_press(self, event) -> None:
        '''
            Atrelado à canvas1, define canto mais perto das coordenadas de canvas1.
        
            Parameters: 
                event (event): Bind (B1-Motion);
                event.x (float): Recebe Coordenada X;
                event.y (float): Recebe Coordenada Y;

            Returns:
                None
        '''

        self.selected_corner = self.get_nearest_corner(event.x, event.y)
        
    def on_mouse_drag(self, event) -> None:
        '''
            Atrelado à canvas1, atualiza coordenada de self.points para coordenada atual.

            Parameters: 
                event (event): Bind (Button-01);
                event.x (float): Recebe Coordenada X;
                event.y (float): Recebe Coordenada Y;

            Returns:
                None
        '''

        if self.selected_corner is not None:
            self.points[self.selected_corner] = (event.x, event.y)
            self.draw_lines_between_points()

    def on_mouse_release(self, event) -> None:
        '''
            Atrelado à canvas1, ao soltar botão esquerdo do mouse, atualiza as linhas vermelhas e transforma imagem em perspectiva.

            Parameters: 
                event (event): Bind (ButtonRelease-1);
            Returns:
                None
        '''

        self.selected_corner = None
        self.draw_lines_between_points()
        self.transform_image()

# ========= Imagem ========== #

    def load_and_display_current_image(self) -> None:
        '''
            Carrega e insere imagem em canvas1.

            Parameters: 
                current_image_index (index): Recebe índice da imagem atual;
                image_paths[] (list[value]): Recebe valor em lista para definir caminho da imagem atual;
                available_width (int): Recebe valor de largura para ajustar tamanho da imagem;
                available_height (int): Recebe valor de altura para ajustar tamanho da imagem;
                trecho_list[] (list[value]): Recebe valor de km atrelado à imagem atual.

            Returns:
                None
        '''

        if 0 <= self.current_image_index < len(self.image_paths):
            image_path = self.image_paths[self.current_image_index]
            self.image = Image.open(image_path)
            self.resized_image = self.image.resize((self.canvas1_width, self.canvas1_height), Image.LANCZOS)
            self.tk_image = ImageTk.PhotoImage(self.resized_image)
            self.canvas1.create_image(0, 0, anchor='nw', image=self.tk_image)
            self.draw_lines_between_points()

    def transform_image(self) -> None:
        '''
            Transforma a imagem numa perspectiva e gera uma grade para amostragem.

            Parameters: 
                points (list): Recebe lista de pontos para montar perspectiva;
                image.width (int): Recebe tamanho da imagem no tamanho original;
                resized_image.width (int): Recebe tamanho da imagem em tamanho atual;
                image (photo_image): Recebe foto para montar perspectiva como photo_image.

            Returns:
                None
            '''
        
        if len(self.points) == 4:
            # calcula razão do aspecto entre a imagem original com atual.
            self.aspect_ratio = self.image.width / self.resized_image.width
            # ajusta pontos para o aspecto calculado.
            adjusted_points = [(x*self.aspect_ratio, y*self.aspect_ratio) for x, y in self.points]
            # transforma em np.array os pontos ajustado.
            src_points = np.array(adjusted_points, dtype=np.float32)
            # calcula tamanho de canvas2.
            canvas2_width = self.canvas2.winfo_reqwidth()
            canvas2_height = self.canvas2.winfo_height()
            # define np.array para tamanho de canvas2.
            dst_points = np.array([(0, 0), (canvas2_width, 0), (canvas2_width, canvas2_height), (0, canvas2_height)], dtype=np.float32)
            # cria uma matriz de perspectiva com pontos da imagem e canvas2.
            perspective_matrix = cv2.getPerspectiveTransform(src_points, dst_points)
            
            # Transforma imagem.
            if self.image:
                original_image = np.array(self.image)
                transformed_image = cv2.warpPerspective(original_image, perspective_matrix, (canvas2_width, canvas2_height))
                pil_image = Image.fromarray(transformed_image)
                self.transformed_photo = ImageTk.PhotoImage(pil_image)

                self.canvas2.create_image(0, 0, anchor="nw", image=self.transformed_photo)

# ========= Vis. Linhas ========== #

    def draw_lines_between_points(self) -> None:
        '''
            Desenha linhas vermelhas entre os pontos em canvas1 por loop.

            Parameters: 
                points (list): Recebe lista de pontos para desenhar linhas.

            Returns:
                None
            '''
        
        self.canvas1.delete("line")  # Clear previous lines
        for i in range(len(self.points)):
            x1, y1 = self.points[i]
            x2, y2 = self.points[(i + 1) % 4]
            self.canvas1.create_line(x1, y1 , x2, y2, tags="line", fill="red")

    def get_nearest_corner(self, x:int, y:int) -> int:
        '''
            Calcula qual o ponto, em self.points, está mais próximo das coordenadas clicadas na tela.

            Parameters: 
                points (list): Recebe lista de pontos parapydesenhar linhas.

            Returns:
                clossest_point (index): retorna índice do ponto mais perto.
        '''

        distances = [((x  - point[0])**2 + (y - point[1])**2) for point in self.points]
        clossest_point = distances.index(min(distances))

        return clossest_point
    
    def update_points(self) -> None:
        '''
            Atualiza a lista self.points para o tamanho atual da imagem.

            Parameters: 
                available_width (int): Recebe de self a largura da canvas1;
                available_height (int): Recebe de self a altura da canvas1;

            Returns:
                None
        '''     

        self.points = [(10, 10),
            (self.canvas1_width -10, 10),
            (self.canvas1_width - 10, self.canvas1_height - 10),
            (10, self.canvas1_height - 10)
        ]

if __name__ == "__main__":
    root = tk.Tk()
    app = perspective_app(root)
    root.mainloop()