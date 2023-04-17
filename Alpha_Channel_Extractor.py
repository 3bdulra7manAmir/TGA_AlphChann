import os
import time
from PIL import Image

def Operation():
    source_directory = input("Enter source Path Please: ")  # Get all files inside this directory
    #target_directory = input("Enter targeted Path Please: ")  # Save all files to this directory

    for filename in os.listdir(source_directory):
        # Check if file is a TGA image
        if filename.endswith(".tga"):
            # Check if filename contains "spc" or "sp"
            if ("spc" in filename) or ("sp" in filename):
                # Open the TGA image and extract the alpha channel
                filepath = os.path.join(source_directory, filename)
                image = Image.open(filepath)
                alpha_channel = image.split()[-1]

                # Construct new filename with "Ncos" instead of "spc" or "sp",
                # and remove any instances of "~", "&", or numbers
                new_filename = filename.replace("spc", "Ncos").replace("sp", "Ncos").replace("~", "").replace("&", "").translate(str.maketrans("", "", "0123456789"))

                # Save the alpha channel as a separate image in the target directory
                target_file = os.path.join(source_directory, new_filename)
                alpha_channel.save(target_file)

                # Rename the original file with any numbers, "&", and "~" symbols removed
                os.rename(os.path.join(source_directory, filename), os.path.join(source_directory, filename.translate(str.maketrans("", "", "0123456789&~"))))

                # Do something with the extracted alpha channel
                print("Extracted alpha channel from", filename, "and saved it as", target_file)
            else:
                # Do something with non-matching files
                print(filename, "does not contain 'spc' or 'sp'")

    print("\n\n")
    print("Extracting Finished Successfully")
    time.sleep(1)
    again = input("\nDo you want to Extract Again?: y/n")
    if again == "y":
        Operation()
    else:
        os._exit()

Operation()