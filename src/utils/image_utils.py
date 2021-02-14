from PIL import Image
import os

class ImageSticher:

    def sticher(self, folder_path):
        directories = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path,f))]
        for directory in directories:
            self.image_sticher(os.path.join(folder_path,directory))

    def image_sticher(self, frame_folder):
        files = [f for f in os.listdir(frame_folder) if os.path.isfile(os.path.join(frame_folder, f))]
        files = [ os.path.join(frame_folder,x) for x in files ]

        final_image = Image.open(files[0])

        for image_file in files[1:]:
            image = Image.open(image_file)
            
            final_image.paste(image, None, image)

        output_dir, frame_number = os.path.split(frame_folder)
        output_dir = os.path.join(output_dir, 'merged')
        os.makedirs(output_dir, exist_ok=True)
        final_image.save(os.path.join(output_dir,frame_number+'_output.png'))