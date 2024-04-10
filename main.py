import os

from PIL import Image, ImageEnhance, ImageDraw, ImageFilter


def enhance_image(image_path, saturation_factor, contrast_factor, vignette_intensity):
    img = Image.open(image_path)

    enhancer = ImageEnhance.Color(img)
    img = enhancer.enhance(saturation_factor)

    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(contrast_factor)

    img = add_vignette(img, vignette_intensity)

    return img


def add_vignette(image, vignette_intensity):
    # Create a circular mask for vignette effect
    width, height = image.size
    mask = Image.new('L', (width, height), 0)
    draw = ImageDraw.Draw(mask)

    # Calculate radius based on vignette intensity
    radius = int(min(width, height) * vignette_intensity)

    # Draw a black ellipse centered on the image
    draw.ellipse((width / 2 - radius, height / 2 - radius, width / 2 + radius, height / 2 + radius), fill=255)

    # Blur the mask to soften the edges
    mask = mask.filter(ImageFilter.GaussianBlur(radius / 4))

    # Apply vignette effect
    vignetted_img = Image.composite(image, Image.new('RGB', image.size, (0, 0, 0)), mask)

    return vignetted_img


def process_images_in_directory(directory, saturation_factor, contrast_factor, vignette_intensity):
    for filename in os.listdir(directory):
        if filename.lower().endswith('.jpg'):
            image_path = os.path.join(directory, filename)
            enhanced_img = enhance_image(image_path, saturation_factor, contrast_factor, vignette_intensity)
            output_path = os.path.join(directory, f"enhanced_{filename}")
            enhanced_img.save(output_path)


def main():
    current_dir = os.getcwd()

    # Hardcoded values (TODO: console program to specify these values)
    saturation_factor = 1.3
    contrast_factor = 1.1
    vignette_intensity = 0.8

    # Process all .jpg files in the current directory
    process_images_in_directory(current_dir, saturation_factor, contrast_factor, vignette_intensity)

if __name__ == "__main__":
    main()
