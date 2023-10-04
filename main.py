import tkinter as tk
from tkinter import filedialog
from PIL import Image
import sys

open_path = filedialog.askopenfilename(title="Select PNG file to convert", filetypes=[("PNG Files", "*.png")])
if not open_path.endswith(".png"):
    sys.exit(-1)
input_image = Image.open(open_path)
frame_size = input_image.width
if frame_size % 16 != 0:
    sys.exit(-1)
if input_image.height % frame_size != 0:
    sys.exit(-1)
num_frames = input_image.height // frame_size
frames = []

# Create the main tkinter window
root = tk.Tk()
root.geometry("400x200")
root.title("Parameter Input")

# Create labels for the parameters
label1 = tk.Label(root, text="frametime")

# Create entry widgets for the parameters
entry1 = tk.Entry(root)

# Create labels for the parameters
label2 = tk.Label(root, text="output res")

# Create entry widgets for the parameters
entry2 = tk.Entry(root)

entry1.insert(0, "2")
entry2.insert(0, "200")

# Create a checkbox
checkbox_var = tk.IntVar()  # Variable to store the checkbox state
checkbox = tk.Checkbutton(root, text="Transparent Background", variable=checkbox_var)

def submit_parameters(event=None):
    frametime = entry1.get()
    resolution = entry2.get()

    if frametime.isdigit() and int(frametime) > 0 and resolution.isdigit() and int(resolution) >= 16:
        delay = int(frametime) * 50

        for i in range(num_frames):
            # Define the cropping box for each frame
            box = (0, i * frame_size, frame_size, (i + 1) * frame_size)
            # Crop the frame from the input image
            frame = input_image.crop(box).convert("RGBA")

            resized_frame = frame.resize(
                (int(resolution), int(resolution)),
                resample=Image.NEAREST
            ).convert("RGBA")
            # Append the frame to the list of frames
            frames.append(resized_frame)

        save_path = filedialog.asksaveasfilename(title="Save gif file", defaultextension=".gif", filetypes=[("GIF Files", "*.gif"), ("All Files", "*.*")], initialfile="outputgif.gif")
        save_path = save_path if save_path.endswith(".gif") else save_path + ".gif"

        print(checkbox_var)

        if checkbox_var.get() == 1:
            frames[0].save(
                save_path,
                save_all=True,
                append_images=frames[1:],
                duration=int(delay),  # Set the frame duration (in milliseconds)
                loop=0,  # Set the loop count (0 means infinite loop)
                transparency=0
            )
        else:
            frames[0].save(
                save_path,
                save_all=True,
                append_images=frames[1:],
                duration=int(delay),  # Set the frame duration (in milliseconds)
                loop=0  # Set the loop count (0 means infinite loop)
            )
        root.quit()

# Create a submit button
submit_button = tk.Button(root, text="Submit", command=submit_parameters)
root.bind("<Return>", submit_parameters)

# Pack the labels, entry widgets, and submit button
label1.pack()
entry1.pack()
label2.pack()
entry2.pack()
checkbox.pack()
submit_button.pack()

# Start the tkinter main loop

def set_focus():
    root.focus_force()
    root.grab_set()
    root.focus()

root.after(100, set_focus)

root.mainloop()
