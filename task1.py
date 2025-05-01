#cv2 package of opencv-python used for image processing
import cv2
# Library used for image visualization
import matplotlib.pyplot as plt
# It is a file picker used in python which allows to pick the image locally
from tkinter import filedialog, Tk
#lets you specify the types of elements in a tuple returned or accepted by a function.
from typing import Tuple


class ImageProcessor:
    def __init__(self, image_path: str):
         # It is the constructor that initializes the object with the image path and loads the image
        self.image_path = image_path
        self.image = self._load_image()

    def _load_image(self):
          # it helps in loading the image using OpenCV's imread function
        image = cv2.imread(self.image_path)
        # It helps in check if the image was loaded correctly
        if image is None:
            raise ValueError(f"Could not load image from path: {self.image_path}")
        print(f"[INFO] Loaded image: {self.image_path}")
        return image

    def to_grayscale(self, save_path: str = "gray_image.jpg"):
        """
        Converting the image to grayscale.

         Purpose: it reduces 3 color channels (BGR) into 1 channel, simplifying analysis.
         Formula (Luminance Method):
            Y = 0.299 * R + 0.587 * G + 0.114 * B
            while 
            y = Luminous value of pixel
            r g b = red blue and green value
            and the values are the weights of red green and blue value
        """
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        cv2.imwrite(save_path, gray)
        print(f"[INFO] Grayscale image saved as {save_path}")
        return gray

    def gaussian_blur(self, kernel_size: Tuple[int, int] = (7, 7), save_path: str = "blur.jpg"):
        """
        Apply Gaussian Blur to smooth the image.

         Purpose: Removes high-frequency noise and detail, which helps with tasks like edge detection.

         Formula (2D Gaussian Function):
            G(x, y) = (1 / 2πσ²) * e^(-(x² + y²) / 2σ²)

         where
            - kernel_size: Size of the window 
            - G(x, y): Value at position (x,y) in the kernel
            - σ (sigma): Standard deviation; if 0, OpenCV calculates it automatically.
        """
        blur = cv2.GaussianBlur(self.image, kernel_size, 0)
        cv2.imwrite(save_path, blur)
        print(f"[INFO] Blurred image saved as {save_path}")
        return blur

    def canny_edges(self, threshold1: int = 100, threshold2: int = 200, save_path: str = "edges.jpg"):
        """
        Apply Canny edge detection to extract edges from the image.

         Purpose: Detects sharp changes in intensity (edges), highlighting object boundaries.

         How it works:
            1. Apply Gaussian Blur (already done)
            2. Compute gradients (Sobel Operator)
            3. Non-Max Suppression (keeping the thinnest edges)
            4. Double threshold: keeping edges above threshold2, tracking connected ones above threshold1
        """
        edges = cv2.Canny(self.image, threshold1, threshold2)
        cv2.imwrite(save_path, edges)
        print(f"[INFO] Canny edge image saved as {save_path}")
        return edges

    def display_all(self, gray, blur, edges):
        """
        Displaying all processed images using Matplotlib for visualization.

         Note:
            - OpenCV uses BGR format, Matplotlib uses RGB.
            - Converting images before displaying.
            - Grayscale and edges are single-channel, shown with `cmap='gray'`.
        """
        image_rgb = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)

         # Converting blurred to RGB only if it's 3D (color)
        blurred_rgb = cv2.cvtColor(blur, cv2.COLOR_BGR2RGB) if len(blur.shape) == 3 else blur


        titles = ["Original", "Grayscale", "Gaussian Blur", "Canny Edges"]
        images = [image_rgb, gray, blurred_rgb, edges]
        cmaps = [None, 'gray', None, 'gray']

        plt.figure(figsize=(14, 6))
        for i in range(4):
            plt.subplot(1, 4, i + 1)
            plt.imshow(images[i], cmap=cmaps[i])
            plt.title(titles[i])
            plt.axis('off')
        plt.tight_layout()
        plt.show()


def choose_image_file():
    """
    Open a file dialog window to choose an image file using tkinter.
    """
    root = Tk()
    root.withdraw() # Hides the main tkinter window
    file_path = filedialog.askopenfilename(
        title="Select an Image",
        filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp")]
    )
    return file_path


def main():
     # Asking the user to choose an image file
    file_path = choose_image_file()
    if not file_path:
        print("[WARNING] No image selected. Exiting.")
        return
    
    # Initializing the processor
    processor = ImageProcessor(file_path)
    # Performing the 3 processing tasks
    gray = processor.to_grayscale()
    blurred = processor.gaussian_blur()
    edges = processor.canny_edges()

    # Show all outputs using matplotlib
    processor.display_all(gray, blurred, edges)
    print("[INFO] Task 1 completed.")


if __name__ == "__main__":
    main()
