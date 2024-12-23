import customtkinter as ctk
from tkinter import messagebox, Canvas, Scrollbar, Frame, VERTICAL, HORIZONTAL
from pdf2image import convert_from_path
import os
from PIL import Image, ImageTk
import threading  # Import threading to run the PDF conversion in a separate thread
class DocumentationPage(ctk.CTkFrame):
    def __init__(self, parent, switch_page=None, sharedState=None):
        super().__init__(parent)

        # Define Fonts
        self.FONT_TITLE = ctk.CTkFont(size=18, weight="bold")

        # Return button
        self.return_button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.return_button_frame.pack(fill="x", padx=10, pady=10)
        self.return_button = ctk.CTkButton(self.return_button_frame, text="Return", command=lambda: switch_page("home"))
        self.return_button.pack(side="left", padx=10, pady=10)

        # Title
        self.title_label = ctk.CTkLabel(self, text="Documentation Viewer", font=self.FONT_TITLE)
        self.title_label.pack(pady=10)

        # PDF Display Frame
        self.pdf_frame = Frame(self)
        self.pdf_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Scrollbars
        self.v_scrollbar = Scrollbar(self.pdf_frame, orient=VERTICAL)
        self.v_scrollbar.pack(side="right", fill="y")

        self.h_scrollbar = Scrollbar(self.pdf_frame, orient=HORIZONTAL)
        self.h_scrollbar.pack(side="bottom", fill="x")

        # Canvas for displaying PDF images
        self.canvas = Canvas(self.pdf_frame, yscrollcommand=self.v_scrollbar.set, xscrollcommand=self.h_scrollbar.set)
        self.canvas.pack(fill="both", expand=True)

        self.v_scrollbar.config(command=self.canvas.yview)
        self.h_scrollbar.config(command=self.canvas.xview)

        # Add a loader to indicate that the PDF is loading
        self.loader = ctk.CTkLabel(self, text="Loading...", font=ctk.CTkFont(size=16, weight="bold"))
        self.loader.pack(pady=20)

        # Path to the PDF file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.join(current_dir, "..", "..", "..")
        documentation_file = os.path.join(root_dir, "documentation/documentation.pdf")

        # Load the PDF pages (now in a separate thread)
        self.images = []  # Store references to images to prevent garbage collection
        self.load_pdf_in_background(documentation_file)

        # Bind mouse wheel for scrolling
        self.canvas.bind_all("<MouseWheel>", self.on_mouse_wheel)

    def load_pdf_in_background(self, file_path):
        """Start the PDF loading process in a separate thread."""
        thread = threading.Thread(target=self.load_pdf, args=(file_path,))
        thread.daemon = True  # Allow the thread to close when the app closes
        thread.start()

    def load_pdf(self, file_path):
        """Convert PDF pages to images and display them."""
        if not os.path.exists(file_path):
            messagebox.showerror("Error", f"Documentation file not found: {file_path}")
            return

        try:
            # Convert PDF to images with lower DPI for faster loading
            pages = convert_from_path(file_path, dpi=80)  # Reduced DPI
            y_position = 0

            # Get the canvas width and height
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()

            for page in pages:
                # Convert the page to an image
                img = ImageTk.PhotoImage(page)
                self.images.append(img)  # Keep reference to avoid garbage collection

                # Calculate the center position for the image
                img_width = img.width()
                img_height = img.height()

                # Calculate x and y position to center the image
                x_position = (canvas_width - img_width) // 2
                y_position = y_position + (canvas_height - img_height) // 2

                # Add the image to the canvas (run this in the main thread)
                self.canvas.after(0, self.add_image_to_canvas, img, x_position, y_position)
                y_position += img_height + 10  # Adjust spacing between images


            # Hide the loader after PDF is loaded
            self.loader.destroy()

            # Update the canvas scroll region
            self.canvas.after(0, self.update_scrollregion)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load the PDF: {e}")

    def add_image_to_canvas(self, img, x_position, y_position):
        """Add an image to the canvas (this must be run in the main thread)."""
        self.canvas.create_image(x_position, y_position, anchor="nw", image=img)

    def update_scrollregion(self):
        """Update the scroll region of the canvas (this must be run in the main thread)."""
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def on_mouse_wheel(self, event):
        """Handle mouse wheel scrolling."""
        if event.delta > 0:  # Scroll up
            self.canvas.yview_scroll(-1, "units")
        else:  # Scroll down
            self.canvas.yview_scroll(1, "units")
