import os
from PIL import Image


def construct_new_filename(filename):
    return (
        filename.replace("spc", "Ncos")
        .replace("sp", "Ncos")
        .replace("~", "")
        .replace("&", "")
        .translate(str.maketrans("", "", "0123456789"))
    )


class ImageProcessor:
    def __init__(self, source_directory):
        self.source_directory = source_directory

    def validate_directory(self):
        if not os.path.isdir(self.source_directory):
            raise FileNotFoundError(f"Directory '{self.source_directory}' does not exist.")

    def process_images(self):
        self.validate_directory()
        files_processed = 0

        for filename in os.listdir(self.source_directory):
            if filename.endswith(".tga"):
                try:
                    self.handle_tga_file(filename)
                    files_processed += 1
                except Exception as e:
                    self.log_error(f"Error processing {filename}: {e}")

        print(f"\nProcessed {files_processed} TGA files successfully.")
        self.ask_to_repeat()

    def handle_tga_file(self, filename):
        filepath = os.path.join(self.source_directory, filename)
        new_filename = construct_new_filename(filename)

        # Extract alpha channel and save it
        with Image.open(filepath) as image:
            alpha_channel = image.split()[-1]
            target_file = os.path.join(self.source_directory, new_filename)
            alpha_channel.save(target_file)

        # Rename original file
        new_original_name = self.cleanup_filename(filename)
        os.rename(filepath, os.path.join(self.source_directory, new_original_name))

        print(f"Extracted alpha channel from '{filename}' and saved as '{new_filename}'.")
        print(f"Renamed original file to '{new_original_name}'.")

    def cleanup_filename(self, filename):
        return filename.translate(str.maketrans("", "", "0123456789&~"))

    def ask_to_repeat(self):
        again = input("\nDo you want to process another directory? (y/n): ").strip().lower()
        if again == "y":
            new_source_directory = input("Enter new source directory: ").strip()
            self.source_directory = new_source_directory
            self.process_images()
        else:
            print("Exiting the program. Thank you!")
            exit()

    def log_error(self, message):
        log_file = "image_processing_errors.log"
        with open(log_file, "a") as log:
            log.write(message + "\n")


def main():
    source_directory = input("Enter the source directory path:  ").strip()

    try:
        processor = ImageProcessor(source_directory)
        processor.process_images()
    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
