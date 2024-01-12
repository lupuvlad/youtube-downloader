from pytube import YouTube
from pytube.exceptions import *
import customtkinter as ctk

# Set the colors for the app
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# Create the app
app = ctk.CTk()
app.title("YouTube Downloader")
app.geometry("720x480")

# Set up the grid
app.columnconfigure((0, 1, 2), weight=1)
app.rowconfigure((0, 1, 2), weight=1)


# Main download function
def download_video():
    """Downloads a video based on the chosen resolution."""
    url = link_entry.get()
    resolution = resolution_var.get()

    try:
        yt = YouTube(url, on_progress_callback=on_progress)
        stream = yt.streams.filter(res=resolution, progressive=True).first()
        stream.download()
    except AgeRestrictedError:
        status_label.configure(text=f"The video has an age restriction! You need to be authenticated to download it!",
                               text_color="red", font=("Arial", 18))
    except LiveStreamError:
        status_label.configure(text="Video is a live stream.", text_color="red", font=("Arial", 18))
    except RegexMatchError:
        status_label.configure(text=f"The url: {url} is unavailable!", text_color="red", font=("Arial", 18))
    except VideoUnavailable:
        status_label.configure(text=f"The video is unavailable!", text_color="red", font=("Arial", 18))
    else:
        status_label.configure(text=f"Download completed!", text_color="green", font=("Arial", 18))


def on_progress(stream, chunk, bytes_remaining):
    """Make the progress bar functional."""
    # Extract the total file size of the video.
    file_size = stream.filesize
    # Calculate the downloaded bytes.
    # bytes_remaining (int) – The delta between the total file size in bytes and amount already downloaded.
    downloaded_bytes = file_size - bytes_remaining
    # Calculate the completed percentage, multiplying by 100 to use this variable for configuring the progress label.
    percentage = (downloaded_bytes / file_size) * 100

    # Configure progress and status label.
    progress_label.configure(text=f"{(int(percentage))}%")
    progress_label.update()

    status_label.configure(text="Downloading...", font=("Arial", 18))

    progress_bar.set(float(percentage / 100))  # set method only accepts float values between 0 and 1,
    # so there should be float values


def change_download_button_text(choice):
    """Change the text of the download button."""
    download_button.configure(text=f"Download at {choice}")


# Widgets
# ..........
# First row
title_label = ctk.CTkLabel(master=app, text="URL:", font=("Arial", 16))
title_label.grid(row=0, column=0, padx=10, pady=10, sticky="ne")

link_entry = ctk.CTkEntry(master=app, placeholder_text="Insert a YouTube link:")
link_entry.grid(row=0, column=1, pady=(10, 0), sticky="nwe")

combobox_label = ctk.CTkLabel(master=app, text="Choose the resolution:", font=("Arial", 20))
combobox_label.grid(row=0, column=1, pady=0, sticky="ew")

# Create Combobox
resolutions = ["720p", "360p", "240p"]
resolution_var = ctk.StringVar()
format_combobox = ctk.CTkComboBox(master=app, values=resolutions, variable=resolution_var,
                                  command=change_download_button_text, width=200, height=50, justify="center",
                                  font=("Arial", 16))
format_combobox.grid(row=0, column=1, sticky="s")

# Second row
download_button = ctk.CTkButton(master=app, text="Download", command=download_video)
download_button.grid(row=1, column=1, pady=(30, 0), sticky="n")

progress_label = ctk.CTkLabel(master=app, text="0%", font=("Arial", 16))
progress_label.grid(row=1, column=1, pady=(10, 0), sticky="ew")

progress_bar = ctk.CTkProgressBar(master=app, progress_color="#9E9E9E", fg_color="#1f538d")
progress_bar.grid(row=1, column=1, pady=(0, 40), sticky="s")
progress_bar.set(0)

status_label = ctk.CTkLabel(master=app, text="")
status_label.grid(row=1, column=1, sticky="s")

# Run the app
app.mainloop()
