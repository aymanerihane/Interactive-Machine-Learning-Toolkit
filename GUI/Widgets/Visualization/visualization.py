import customtkinter as ctk
from tkinter import Scrollbar
import os
from PIL import Image
import json

class VisualizationPage(ctk.CTkFrame):
    def __init__(self, parent, switch_page):
        super().__init__(parent)
        self.switch_page = switch_page  # Function to switch pages

        self.training_done = False  # Flag to check if training is done


        self.current_dir = os.path.dirname(__file__)  # Path to the current file
        self.current_dir = os.path.join(self.current_dir, "../../") # Parent directory
        # Load the charts data from the JSON file
        self.charts_type = self.load_charts_data()

        # Create tabs for pre-training and post-training
        self.tab_view = ctk.CTkTabview(self, width=850, height=650)
        self.tab_view.pack(pady=20, padx=20, fill="both", expand=True)

        # Create scrollable tabs
        self.pre_training_canvas, self.pre_training_tab = self.create_scrollable_tab(self.tab_view.add("Pre-Training"))
        self.post_training_canvas, self.post_training_tab = self.create_scrollable_tab(self.tab_view.add("Post-Training"))

        # Populate tabs
        self.populate_tab(self.pre_training_tab, self.charts_type["pre-training"],"pre-training")
        self.populate_tab(self.post_training_tab, self.charts_type["post-training"],"post-training")

        # Poll the active tab to bind the mouse wheel dynamically
        self.active_tab = "Pre-Training"  # Default tab
        self.bind_mousewheel(self.pre_training_canvas)  # Initial binding
        self.poll_active_tab()


    def create_scrollable_tab(self, parent):
        """Create a scrollable container for a tab."""
        # Create a canvas and a scrollbar
        canvas = ctk.CTkCanvas(parent, highlightthickness=0, width=850, height=650)
        scrollbar = Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = ctk.CTkFrame(canvas)

        # Configure the canvas
        scrollable_frame_id = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Bind events for resizing and scrolling
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(scrollable_frame_id, width=e.width))

        # Pack everything
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        return canvas, scrollable_frame

    def poll_active_tab(self):
        """Continuously check for the active tab and update mouse wheel binding."""
        current_tab = self.tab_view.get()  # Get the name of the active tab
        if current_tab != self.active_tab:
            self.active_tab = current_tab
            if current_tab == "Pre-Training":
                self.bind_mousewheel(self.pre_training_canvas)
            elif current_tab == "Post-Training":
                self.bind_mousewheel(self.post_training_canvas)

        # Repeat this function every 200ms (improved performance)
        self.after(200, self.poll_active_tab)

    def bind_mousewheel(self, widget):
        """Bind mouse wheel scrolling to the given widget."""
        widget.bind_all("<MouseWheel>", lambda event: self.on_mousewheel(widget, event))  # Windows/Unix
        widget.bind_all("<Button-4>", lambda event: self.on_mousewheel(widget, event))   # macOS/Linux (scroll up)
        widget.bind_all("<Button-5>", lambda event: self.on_mousewheel(widget, event))   # macOS/Linux (scroll down)

    def on_mousewheel(self, widget, event):
        """Handle mouse wheel scrolling."""
        if event.num == 4 or event.delta > 0:  # Scroll up
            widget.yview_scroll(-1, "units")
        elif event.num == 5 or event.delta < 0:  # Scroll down
            widget.yview_scroll(1, "units")

    def populate_tab(self, tab, chart_dict, dict_parent, lisModel_available=None):
        """Populate a tab with chart sections and charts dynamically."""
        # Setting default value for lisModel_available if not provided
        if lisModel_available is None:
            lisModel_available = []

        # Pre-training data is always available
        for i in range(3):  # Assuming 3 columns
            tab.grid_columnconfigure(i, weight=1)  # Distribute space equally

        row = 0
        # Iterate through the dictionary based on the parent (pre-training or post-training)
        for section, charts in chart_dict.items():
            print(f"Section: {section} in {dict_parent}")
            # Add section title
            section_label = ctk.CTkLabel(tab, text=section, font=("Arial", 18, "bold"), anchor="w")
            section_label.grid(row=row, column=0, columnspan=3, sticky="w", pady=10, padx=10)
            row += 1

            col = 0
            for chart_name, details in charts.items():
                description = details["description"]
                available_models = details["models"]

                # Create a frame for each chart
                frame = ctk.CTkFrame(tab, corner_radius=10)
                frame.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")  # Sticky ensures full stretch
                frame.grid_propagate(False)  # Prevent resizing

                # Load and add icon dynamically for each chart
                image_path = os.path.join(self.current_dir, "images")  # Path to images folder
                icon_path = os.path.join(image_path, "defaultIcon.png")

                try:
                    icon1 = Image.open(icon_path)
                except FileNotFoundError:
                    icon1 = Image.open(os.path.join(image_path, "iconCharts.png"))  # Default icon

                icon = ctk.CTkImage(light_image=icon1, dark_image=icon1, size=(24, 24))
                icon_label = ctk.CTkLabel(frame, image=icon, compound="left", text="")
                icon_label.pack(pady=5)

                # Add chart name
                label = ctk.CTkLabel(frame, text=chart_name, font=("Arial", 14, "bold"), anchor="center")
                label.pack(pady=2)

                # Add description
                desc = ctk.CTkLabel(frame, text=description, font=("Arial", 12), wraplength=220, justify="center")
                desc.pack(pady=5)

                # Logic for availability checks
                if not dict_parent == "post-training":
                    if not self.training_done:
                        self.post_training_tab.grid_forget()  # Hide the tab
                        not_available_label = ctk.CTkLabel(frame, text="Available", font=("Arial", 10, "italic"), fg_color="green",corner_radius=15)
                        not_available_label.pack(pady=5)
                    else:
                        self.post_training_tab.grid(row=row, column=0, columnspan=3, sticky="nsew")  # Show the tab again
                    frame.bind("<Button-1>", lambda event, chart_name=chart_name: self.switch_page(chart_name))

                else:
                    # For pre-training, all charts are available
                    self._add_chart_interaction(frame, chart_name, available_models, lisModel_available)

                col += 1
                if col == 3:  # Adjust number of columns per row
                    col = 0
                    row += 1

            # Add spacing after each section
            row += 1

    
    def _add_chart_interaction(self, frame, chart_name, available_models, lisModel_available):
        """Handles chart interaction logic based on available models."""
        if not available_models:
            # Display a "Not Available" message if no models match
            not_available_label = ctk.CTkLabel(frame, text="Not Available", font=("Arial", 10, "italic"), fg_color="gray")
            not_available_label.pack(pady=5)

            # Make the frame unclickable
            # frame.bind("<Button-1>", lambda event: None)  # Do nothing when clicked
        else:
            # Check if model is available in lisModel_available
            if any(model in lisModel_available for model in available_models):
                # Bind the frame to call the switch_page method with a unique page name
                frame.bind("<Button-1>", lambda event, chart_name=chart_name: self.switch_page(chart_name))
            else:
                # If the model is not available, disable click interaction
                not_available_label = ctk.CTkLabel(frame, corner_radius=15,text="Model Not Available", font=("Arial", 10, "italic"), fg_color="red")
                not_available_label.pack(pady=5)
                # frame.bind("<Button-1>", lambda event: None)  # Do nothing when clicked

    def load_charts_data(self):
        """Load charts data from the JSON file."""
        try:
            file_path = os.path.join(self.current_dir, "../Data/chartsType.json")
            print(file_path)
            with open(file_path, 'r') as json_file:
                print("Charts data loaded successfully!")
                return json.load(json_file)
        except FileNotFoundError:
            print("charts_type.json file not found!")
            return {}
    def get_icon_path(self, chart_name, image_path):
        """Get a specific icon for each chart type."""
        # Map each chart type to a corresponding icon
        chart_icons = {
            "Table": "tableIcon.png",
            "Histograms": "histogramIcon.png",
            "Scatter Plots": "scatterPlotIcon.png",
            "Box Plots": "boxPlotIcon.png",
            "Heatmaps": "heatmapIcon.png",
            "Pie Charts": "pieChartIcon.png",
            "Violin Plots": "violinPlotIcon.png",
            "Pair Plots": "pairPlotIcon.png",
            "Stacked Bar Charts": "stackedBarIcon.png",
            "Line Graphs": "lineGraphIcon.png",
            "Confusion Matrix": "confusionMatrixIcon.png",
            "ROC Curves": "rocCurveIcon.png",
            "Precision-Recall Curve": "precisionRecallIcon.png",
            "Bar Graphs": "barGraphIcon.png",
            "Dendrograms": "dendrogramIcon.png",
            "Cluster Scatter Plots": "clusterScatterIcon.png"
        }

        # Return the icon path or default icon if not found
        return os.path.join(image_path, chart_icons.get(chart_name, "defaultIcon.png"))
