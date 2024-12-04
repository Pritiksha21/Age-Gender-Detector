# IMPORTING NECESSARY LIBRARIES
import tkinter as tk
from tkinter import filedialog
from tkinter import *
from PIL import Image, ImageTk
import numpy as np
from keras.models import load_model

# Loading the Model
model = load_model('Age_Sex_Detection (1).keras')

# Initializing the GUI
top = tk.Tk()
top.geometry('800x600')
top.title('Age & Gender Detector')
top.configure(background='#CDCDCD')

label1 = Label(top, background="#CDCDCD", font=('arial', 15, "bold"))
label2 = Label(top, background="#CDCDCD", font=('arial', 15, "bold"))
sign_image = Label(top)

# Defining Detect function which detects the age and gender of the person in image using the model
def Detect(file_path):
    global label_packed
    image = Image.open(file_path)
    image = image.resize((48, 48))  # Ensure proper resizing with a tuple (width, height)
    image = np.array(image)  # Convert image to numpy array
    image = np.expand_dims(image, axis=0)  # Expand dimensions to match model input
    image = image / 255.0  # Normalize the image
    print(image.shape)

    # Gender labels
    sex_f = ["Male", "Female"]
    
    # Make prediction
    pred = model.predict(image)
    
    # Ensure that pred has the correct format (assuming [gender, age] output)
    age = int(np.round(pred[1][0]))  # Assuming pred[1] contains the age
    sex = int(np.round(pred[0][0]))  # Assuming pred[0] contains the gender
    
    # Display results
    print(f"Predicted Age is {age}")
    print(f"Predicted Gender is {sex_f[sex]}")

    # Update the labels with predicted values
    label1.configure(text=f"Age: {age}", foreground="#011638")
    label2.configure(text=f"Gender: {sex_f[sex]}", foreground="#011638")

# Defining Show_detect button function
def show_Detect_button(file_path):
    Detect_b = Button(top, text="Detect Image", command=lambda: Detect(file_path), padx=10, pady=5)
    Detect_b.configure(background="#364156", foreground='white', font=('arial', 10, 'bold'))
    Detect_b.place(relx=0.79, rely=0.46)

# Defining Upload Image Function
def upload_image():
    try:
        file_path = filedialog.askopenfilename()  # Open file dialog to upload an image
        upload_image = Image.open(file_path)  # Open the uploaded image
        upload_image.thumbnail(((top.winfo_width() / 2.25), (top.winfo_height() / 2.25)))  # Resize the image
        im = ImageTk.PhotoImage(upload_image)  # Convert the image to PhotoImage for Tkinter

        sign_image.configure(image=im)  # Display the image
        sign_image.image = im  # Keep reference to the image object
        
        label1.configure(text='')  # Clear previous results
        label2.configure(text='')  # Clear previous results
        
        # Show the Detect button after image is uploaded
        show_Detect_button(file_path)

    except Exception as e:
        print(f"Error uploading image: {e}")

# Upload button to upload an image
upload = Button(top, text="Upload an Image", command=upload_image, padx=10, pady=5)
upload.configure(background="#364156", foreground='white', font=('arial', 10, 'bold'))
upload.pack(side='bottom', pady=50)

# Image display label
sign_image.pack(side='bottom', expand=True)

# Result labels
label1.pack(side="bottom", expand=True)
label2.pack(side="bottom", pady=50)

# Heading label
heading = Label(top, text="Age and Gender Detector", pady=20, font=('arial', 20, "bold"))
heading.configure(background="#CDCDCD", foreground="#364156")
heading.pack()

# Run the Tkinter event loop
top.mainloop()
