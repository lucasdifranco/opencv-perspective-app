# opencv-perspective-app!

![Ico-perspective](https://github.com/lucasdifranco/opencv-perspective-app/assets/130804578/a261b079-7195-47d0-bcba-83f725eaf768)


This Python application is designed to modify the perspective of images using the OpenCV library. It provides an easy way to select four corners in the original image, and then applies the cv2.warpPerspective function to modify the image's perspective. This tool is useful for tasks such as correcting distortions in photos or preparing images for perspective-based transformations, training AI models, etc...

## Features

*  User-friendly interface for selecting four corner points in the original image.
* Real-time preview of perspective modification.
* Batch processing: Apply the same perspective adjustment to multiple images in a folder.

## Prerequisites
```python
numpy==1.24.4
opencv_python==4.5.3.56
Pillow==10.0.0
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
