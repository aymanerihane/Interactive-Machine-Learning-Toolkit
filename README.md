# **Interactive Machine Learning Toolkit**  

This project is an **interactive machine learning toolkit** built with **CustomTkinter**, designed to provide a user-friendly graphical interface for data preprocessing, visualization, and machine learning model building. The toolkit simplifies the end-to-end machine learning workflow, enabling users to efficiently interact with their data and models without writing extensive code.

---

## **Features**
- **Custom Widgets:** Enhanced interface elements like custom checkboxes, buttons, and radio buttons.
- **Dynamic Target Selection:** Toggleable options for selecting and splitting target variables in datasets.
- **Scrollable Frame for Options:** Scrollable frames to handle additional options like column selection.
- **Data Uploading:** Easy integration to upload datasets directly into the application.
- **Model Exporting:** Export processed results with a single click.
- **Background Images:** Custom visuals for an aesthetically pleasing design.
- **Error Handling:** Seamlessly manages file paths and errors during runtime.

---

## **Requirements**
To run this application, you need:
- **Python 3.8+**
- **CustomTkinter Library**  
  Install it using:  
  ```bash
  pip install customtkinter
  ```

---

## **Installation**
1. Clone the repository:  
   ```bash
   git clone https://github.com/your-username/ml-toolkit.git
   cd ml-toolkit
   ```
2. Install the required dependencies using `pip`.
3. Run the application:  
   ```bash
   python gui_main.py
   ```

---

## **Usage**
1. **Data Upload:** Click the "Upload Data" button to load your dataset.  
2. **Target Variable:** Use the "Has Target?" checkbox to enable or disable target selection.  
3. **Dynamic Column Selection:** Use the scrollable frame with radio buttons to choose specific columns for processing.  
4. **Export Results:** Once the processing is complete, use the "Export Result" button to save the output.

---

## **Project Structure**
```plaintext
├── GUI
│   ├── main.py          # Main GUI application
|   ├── home.py          # Home GUI application
│   ├── Widgets          
|         ├── Visualization
|               ├── visualization.py          # Main GUI application
|         ├── HomePage
|               ├── infoData.py          # info Data GUI Widget
|               ├── fonctionality.py          # fonctionality GUI Widgets
|         ├── headerwgt.py          # Header Widget
│   ├── images               # Folder containing image assets
│       └── training_image.png   # Button image for training
|       ├── ...        
├── requirements.txt         # List of dependencies
└── README.md                # Project documentation
```

---

## **Contributing**
Contributions are welcome! If you'd like to contribute, please fork the repository and submit a pull request. For major changes, please open an issue first to discuss what you’d like to change.

---

## **License**
This project is licensed under the [MIT License](LICENSE).

---

## **Acknowledgments**
- Built using the **CustomTkinter** library for a modern Python GUI experience.
- Inspired by the need for intuitive tools in machine learning workflows. 

--- 

## **Contact**
For any inquiries or issues, feel free to contact:  
**Rihane Aymane**  
Email: rihaneaymanee@example.com  
GitHub: [aymanerihane](https://github.com/aymanerihane)  
