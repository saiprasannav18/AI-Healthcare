import tkinter as tk
from tkinter import filedialog
import cv2
import numpy as np
from PIL import Image, ImageTk, ImageDraw
import json

class BoundingBoxAnnotator:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Annotation Tool")
        self.root.configure(bg="Pink")  

        self.canvas = tk.Canvas(root, bg="Black")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.load_button = tk.Button(root, text="Load Image", command=self.load_image, bg="Yellow")
        self.load_button.pack()

        self.label_entry = tk.Entry(root, width=20)
        self.label_entry.pack()

        self.annotate_button = tk.Button(root, text="Annotate", command=self.annotate, bg="lightgreen")
        self.annotate_button.pack()

        self.save_button = tk.Button(root, text="Save Annotations", command=self.save_annotations, bg="lightcoral")
        self.save_button.pack()

        # Radio buttons for annotation type
        self.annotation_type = tk.StringVar(value="bbox")  # Default annotation type is bounding box
        self.annotation_type_frame = tk.Frame(root, bg="lightgray")
        self.annotation_type_frame.pack()
        
        self.bbox_radio = tk.Radiobutton(self.annotation_type_frame, text="Bounding Box", variable=self.annotation_type, value="bbox", bg="Skyblue")
        self.bbox_radio.pack(side=tk.LEFT, padx=5)
        
        self.obb_radio = tk.Radiobutton(self.annotation_type_frame, text="Oriented Bounding Box", variable=self.annotation_type, value="obb", bg="Skyblue")
        self.obb_radio.pack(side=tk.LEFT, padx=5)
        
        self.polygon_radio = tk.Radiobutton(self.annotation_type_frame, text="Polygon", variable=self.annotation_type, value="polygon", bg="Skyblue")
        self.polygon_radio.pack(side=tk.LEFT, padx=5)

        self.original_image = None  # Store the original image
        self.image_on_canvas = None  # Store the image displayed on the canvas
        self.annotations = []

        self.canvas.bind("<ButtonPress-1>", self.start_annotation)
        self.canvas.bind("<B1-Motion>", self.update_annotation)
        self.canvas.bind("<ButtonRelease-1>", self.end_annotation)

        self.start_x = None
        self.start_y = None
        self.temp_annotation = None

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif *.bmp")])
        if file_path:
            self.original_image = Image.open(file_path)
            self.original_image = self.original_image.resize((self.canvas.winfo_width(), self.canvas.winfo_height()))
            self.image_on_canvas = ImageTk.PhotoImage(self.original_image)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image_on_canvas)

    def start_annotation(self, event):
        self.start_x = event.x
        self.start_y = event.y

    def update_annotation(self, event):
        if self.start_x and self.start_y:
            if self.temp_annotation:
                self.canvas.delete(self.temp_annotation)
            x1, y1 = self.start_x, self.start_y
            x2, y2 = event.x, event.y
            annotation_type = self.annotation_type.get()
            if annotation_type == "bbox":
                self.temp_annotation = self.canvas.create_rectangle(x1, y1, x2, y2, outline="red")
            elif annotation_type == "obb":
                # You can implement oriented bounding box annotation here
                pass
            elif annotation_type == "polygon":
                # You can implement polygon annotation here
                pass

    def end_annotation(self, event):
        if self.start_x and self.start_y:
            x1, y1 = self.start_x, self.start_y
            x2, y2 = event.x, event.y
            label = self.label_entry.get()
            annotation_type = self.annotation_type.get()
            if annotation_type == "bbox":
                self.annotations.append({"type": "bbox", "x1": x1, "y1": y1, "x2": x2, "y2": y2, "label": label})
                self.canvas.delete(self.temp_annotation)
            elif annotation_type == "obb":
                # You can implement oriented bounding box annotation here
                pass
            elif annotation_type == "polygon":
                # You can implement polygon annotation here
                pass

    def annotate(self):
        if self.original_image:
            annotated_image = self.original_image.copy()
            draw = ImageDraw.Draw(annotated_image)
            for annotation in self.annotations:
                annotation_type = annotation["type"]
                label = annotation["label"]
                if annotation_type == "bbox":
                    x1, y1, x2, y2 = annotation["x1"], annotation["y1"], annotation["x2"], annotation["y2"]
                    draw.rectangle([x1, y1, x2, y2], outline="red")
                    draw.text((x1, y1 - 10), label, fill="red")
                elif annotation_type == "obb":
                    # You can implement oriented bounding box annotation here
                    pass
                elif annotation_type == "polygon":
                    # You can implement polygon annotation here
                    pass

            self.image_on_canvas = ImageTk.PhotoImage(annotated_image)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image_on_canvas)

    def save_annotations(self):
        if self.annotations:
            save_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
            if save_path:
                with open(save_path, "w") as json_file:
                    json.dump(self.annotations, json_file, indent=4)

if __name__ == "__main__":
    root = tk.Tk()
    app = BoundingBoxAnnotator(root)
    root.mainloop()
