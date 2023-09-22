# opencv-perspective-app! 

![perspective-logo](https://github.com/lucasdifranco/opencv-perspective-app/assets/130804578/81573b50-6ace-46d4-a9ec-1237d7882227)


This Python application is specifically crafted for image perspective modification using the powerful OpenCV library. Its primary function is to simplify the process of selecting four key points within an original image, enabling the precise application of the cv2.warpPerspective function to alter the image's perspective.

Originally designed to streamline the standardization of images for training machine learning models, this versatile tool has found utility in various domains. Its initial purpose was to rectify perspective issues in pavement images for defect labeling. However, it has since proven invaluable in an array of tasks, including the correction of distortions in photographs and the preparation of images for perspective-based transformations, among others.

## Features

* User-friendly interface for selecting four corner points in the original image.
* Real-time preview of perspective modification.
* Batch processing: Apply the same perspective adjustment to multiple images in a folder.

## Limitations
* For now, the app only allows jpg type files, however this can be contoured with a few tweaks in the modules!

## Prerequisites
```python
numpy 1.24.4
opencv_python 4.5.3.56
Pillow 10.0.0
tk 0.1.0
```

Please see any additional packages in requirements.txt.

## Usage
1. Clone or download this repository to your local machine.
2. Open the terminal and navigate to the project folder.
3. Run the application using the following command:

```python
python main.py
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
