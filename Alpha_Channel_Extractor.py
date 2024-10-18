import os
from PIL import Image


def construct_new_filename(filename):
    """Construct a new filename by replacing certain substrings and removing unwanted characters."""
    new_filename = (
        filename.replace("spc", "Ncos")
        .replace("sp", "Ncos")
        .replace("~", "")
        .replace("&", "")
        .translate(str.maketrans("", "", "0123456789"))
    )
    return new_filename


class ImageProcessor:
    def __init__(self, source_directory):
        self.source_directory = source_directory

    def process_images(self):
        """Process the images in the specified directory."""
        for filename in os.listdir(self.source_directory):
            if filename.endswith(".tga"):
                self.handle_tga_file(filename)

        print("\nExtracting Finished Successfully")
        self.ask_to_repeat()

    def handle_tga_file(self, filename):
        """Handle the TGA file by extracting the alpha channel and renaming files."""
        if "spc" in filename or "sp" in filename:
            filepath = os.path.join(self.source_directory, filename)
            image = Image.open(filepath)
            alpha_channel = image.split()[-1]

            # Construct new filename
            new_filename = construct_new_filename(filename)

            # Save the alpha channel as a separate image
            target_file = os.path.join(self.source_directory, new_filename)
            alpha_channel.save(target_file)

            # Rename the original file
            self.rename_original_file(filename)

            print(f"Extracted alpha channel from {filename} and saved it as {target_file}\n")
        else:
            print(f"{filename} does not contain 'spc' or 'sp'")

    def rename_original_file(self, filename):
        """Rename the original file by removing unwanted characters."""
        new_name = filename.translate(str.maketrans("", "", "0123456789&~"))
        os.rename(os.path.join(self.source_directory, filename), os.path.join(self.source_directory, new_name))

    def ask_to_repeat(self):
        """Prompt the user to repeat the extraction process."""
        again = input("\nDo you want to Extract Again? (y/n): ")
        if again.lower() == "y":
            new_source_directory = input("Enter source Path Please: ")
            self.source_directory = new_source_directory
            self.process_images()
        else:
            exit()


def main():
    source_directory = input("Enter source Path Please: ")
    processor = ImageProcessor(source_directory)
    processor.process_images()


if __name__ == "__main__":
    main()
