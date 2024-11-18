import customtkinter as ctk
import os
from PIL import Image, ImageDraw, ImageOps

class HeaderWidget(ctk.CTkFrame):  
    def __init__(self, parent, text="HOME"):
        super().__init__(parent)

        # Define image path, moving one directory up
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../images")

        # Load the header image and apply rounded corners
        image = Image.open(os.path.join(image_path, "images_header.jpg"))
        rounded_image = self._create_rounded_image(image, radius=15)
        self.large_test_image = ctk.CTkImage(rounded_image, size=(500, 100))

        # Header Section
        self.header_label = ctk.CTkLabel(
            self, 
            text=text, text_color="white",
            image=self.large_test_image, 
            compound="center",  # Text above the image
            font=("Arial", 24, "bold")  # Large and bold font
        )
        self.header_label.grid(row=0, column=0, padx=20, pady=10)

        # Configure grid to center the header
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

    def update_text(self, new_text):
        """Method to update the header text."""
        self.header_label.configure(text=new_text)

    def _create_rounded_image(self, img, radius):
        """
        Creates an image with smooth rounded corners.
        :param img: Original PIL Image.
        :param radius: Radius for the rounded corners.
        :return: Image with rounded corners.
        """
        # Ensure image is in RGBA mode
        img = img.convert("RGBA")

        # Create a larger mask for anti-aliasing
        scale = 4  # Scaling factor for better anti-aliasing
        width, height = img.size
        mask = Image.new("L", (width * scale, height * scale), 0)
        draw = ImageDraw.Draw(mask)

        # Draw a larger rounded rectangle and then downscale
        draw.rounded_rectangle(
            [(0, 0), (width * scale, height * scale)], 
            radius=radius * scale, 
            fill=255
        )
        mask = mask.resize((width, height), Image.LANCZOS)  # Downscale with anti-aliasing

        # Apply the mask to the original image
        rounded_img = ImageOps.fit(img, img.size, centering=(0.5, 0.5))
        rounded_img.putalpha(mask)
        return rounded_img

