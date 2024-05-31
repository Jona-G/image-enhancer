import os
from PIL import Image, ImageEnhance, ImageDraw, ImageFilter

SUPPORTED_FORMATS = ('.png', '.jpeg', '.jpg', '.bmp')

def enhance_image(image, saturation_factor, contrast_factor):
    """
    Enhance the saturation and contrast of an image.
    
    Parameters:
        image (PIL.Image): The image to enhance.
        saturation_factor (float): The factor to enhance saturation by.
        contrast_factor (float): The factor to enhance contrast by.
        
    Returns:
        PIL.Image: The enhanced image.
    """
    enhancer = ImageEnhance.Color(image)
    image = enhancer.enhance(saturation_factor)

    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(contrast_factor)
    
    return image

def add_vignette(image, vignette_intensity):
    """
    Add a vignette effect to an image.
    
    Parameters:
        image (PIL.Image): The image to apply the vignette effect to.
        vignette_intensity (float): The intensity of the vignette effect.
        
    Returns:
        PIL.Image: The image with the vignette effect applied.
    """
    width, height = image.size
    mask = Image.new('L', (width, height), 0)
    draw = ImageDraw.Draw(mask)

    radius = int(min(width, height) * vignette_intensity)
    draw.ellipse((width / 2 - radius, height / 2 - radius, width / 2 + radius, height / 2 + radius), fill=255)
    
    mask = mask.filter(ImageFilter.GaussianBlur(radius / 4))
    vignetted_img = Image.composite(image, Image.new('RGB', image.size, (0, 0, 0)), mask)

    return vignetted_img

def process_image(image_path, saturation_factor, contrast_factor, vignette_intensity):
    """
    Process an image by enhancing its properties and adding a vignette effect.
    
    Parameters:
        image_path (str): The path to the image file.
        saturation_factor (float): The factor to enhance saturation by.
        contrast_factor (float): The factor to enhance contrast by.
        vignette_intensity (float): The intensity of the vignette effect.
        
    Returns:
        PIL.Image: The processed image.
    """
    try:
        image = Image.open(image_path)
        image = enhance_image(image, saturation_factor, contrast_factor)
        image = add_vignette(image, vignette_intensity)
        return image
    except Exception as e:
        print(f"Error processing image {image_path}: {e}")
        return None

def show_comparison(original_image, enhanced_image):
    """
    Show a side-by-side comparison of the original and enhanced images.
    
    Parameters:
        original_image (PIL.Image): The original image.
        enhanced_image (PIL.Image): The enhanced image.
    """
    width, height = original_image.size
    comparison = Image.new('RGB', (width * 2, height))
    comparison.paste(original_image, (0, 0))
    comparison.paste(enhanced_image, (width, 0))
    comparison.show()

def process_images_in_directory(directory, saturation_factor, contrast_factor, vignette_intensity):
    """
    Process all supported images in a directory.
    
    Parameters:
        directory (str): The path to the directory containing images.
        saturation_factor (float): The factor to enhance saturation by.
        contrast_factor (float): The factor to enhance contrast by.
        vignette_intensity (float): The intensity of the vignette effect.
    """
    for filename in os.listdir(directory):
        if filename.lower().endswith(SUPPORTED_FORMATS):
            image_path = os.path.join(directory, filename)
            enhanced_img = process_image(image_path, saturation_factor, contrast_factor, vignette_intensity)
            if enhanced_img:
                name, ext = os.path.splitext(filename)
                output_path = os.path.join(directory, f"{name}_enhanced{ext}")
                enhanced_img.save(output_path)
                print(f"Processed and saved: {output_path}")
            else:
                print(f"Failed to process: {image_path}")

def process_images_one_by_one(directory):
    """
    Process each image one by one, asking user for each image.
    
    Parameters:
        directory (str): The path to the directory containing images.
    """
    for filename in os.listdir(directory):
        if filename.lower().endswith(SUPPORTED_FORMATS):
            image_path = os.path.join(directory, filename)
            image = Image.open(image_path)

            while True:
                try:
                    saturation_factor = float(input("Enter saturation factor (e.g. 1.3): "))
                    contrast_factor = float(input("Enter contrast factor (e.g. 1.1): "))
                    vignette_intensity = float(input("Enter vignette intensity (e.g. 0.8): "))
                except ValueError:
                    print("Invalid input. Please enter numeric values.")
                    continue

                enhanced_img = process_image(image_path, saturation_factor, contrast_factor, vignette_intensity)
                if enhanced_img:
                    show_comparison(image, enhanced_img)

                    confirm = input(f"Do you want to save the enhanced image {filename}? (y/n): ").strip().lower()
                    if confirm == 'y':
                        name, ext = os.path.splitext(filename)
                        output_path = os.path.join(directory, f"{name}_enhanced{ext}")
                        enhanced_img.save(output_path)
                        print(f"Processed and saved: {output_path}")
                        break
                    elif confirm == 'n':
                        print("Let's try again.")
                    else:
                        print("Invalid input. Let's try again.")
                else:
                    print(f"Failed to process: {image_path}")
                    break

def main():
    """
    Main function to process images in the current directory.
    """
    current_dir = os.getcwd()

    apply_to_all = input("Apply effects to all images? (y/n): ").strip().lower()
    if apply_to_all == 'y':
        try:
            saturation_factor = float(input("Enter saturation factor (e.g. 1.3): "))
            contrast_factor = float(input("Enter contrast factor (e.g. 1.1): "))
            vignette_intensity = float(input("Enter vignette intensity (e.g. 0.8): "))
        except ValueError:
            print("Invalid input. Please enter numeric values.")
            return

        process_images_in_directory(current_dir, saturation_factor, contrast_factor, vignette_intensity)
    else:
        process_images_one_by_one(current_dir)

if __name__ == "__main__":
    main()