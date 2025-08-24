import os
import sys
from PIL import Image
from PIL.ExifTags import TAGS
import argparse

def remove_metadata_from_image(input_path, output_path=None, preserve_original=True):
    """
    Remove metadata from an image file.
    
    Args:
        input_path (str): Path to the input image
        output_path (str): Path for the output image (optional)
        preserve_original (bool): Whether to keep the original file
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Open the image
        img = Image.open(input_path)
        
        # Get original format
        original_format = img.format
        
        # Print original metadata info if verbose
        if hasattr(img, '_getexif') and img._getexif() is not None:
            exif_data = img._getexif()
            print(f"Original image has {len(exif_data)} EXIF tags")
        
        if img.info:
            print(f"Original image has {len(img.info)} info tags")
            # Show some metadata keys (for ComfyUI workflows)
            if 'workflow' in img.info:
                print("  - Contains ComfyUI workflow metadata")
            if 'prompt' in img.info:
                print("  - Contains ComfyUI prompt metadata")
        
        # Create a new image without metadata
        # Convert to RGB if necessary (for JPEG compatibility)
        if original_format in ['JPEG', 'JPG'] and img.mode in ['RGBA', 'LA', 'P']:
            # Create white background for transparency
            rgb_img = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            rgb_img.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            clean_img = rgb_img
        else:
            # Create new image with same data but no metadata
            clean_img = Image.new(img.mode, img.size)
            clean_img.putdata(list(img.getdata()))
        
        # Determine output path
        if output_path is None:
            if preserve_original:
                base_name, ext = os.path.splitext(input_path)
                output_path = f"{base_name}_no_metadata{ext}"
            else:
                output_path = input_path
        
        # Save the clean image
        # Remove any save parameters that might preserve metadata
        save_kwargs = {}
        if original_format in ['JPEG', 'JPG']:
            save_kwargs = {'quality': 95, 'optimize': True}
        elif original_format == 'PNG':
            save_kwargs = {'optimize': True}
        
        clean_img.save(output_path, format=original_format, **save_kwargs)
        
        print(f"Successfully removed metadata from: {input_path}")
        if output_path != input_path:
            print(f"Clean image saved as: {output_path}")
        
        return True
        
    except Exception as e:
        print(f"Error processing {input_path}: {e}")
        return False


def process_folder(folder_path, output_folder=None, preserve_original=True, recursive=True):
    """
    Process all images in a folder to remove metadata.
    
    Args:
        folder_path (str): Path to folder containing images
        output_folder (str): Optional output folder
        preserve_original (bool): Whether to keep original files
        recursive (bool): Whether to process subfolders
    """
    supported_formats = {'.jpg', '.jpeg', '.png', '.tiff', '.tif', '.bmp', '.webp'}
    processed_count = 0
    
    if output_folder and not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    walk_method = os.walk if recursive else lambda x: [(folder_path, [], [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))])]
    
    for root, dirs, files in walk_method(folder_path):
        for file in files:
            file_ext = os.path.splitext(file)[1].lower()
            if file_ext in supported_formats:
                input_path = os.path.join(root, file)
                
                if output_folder:
                    # Maintain folder structure in output
                    rel_path = os.path.relpath(root, folder_path)
                    output_dir = os.path.join(output_folder, rel_path)
                    if not os.path.exists(output_dir):
                        os.makedirs(output_dir)
                    output_path = os.path.join(output_dir, file)
                else:
                    output_path = None
                
                if remove_metadata_from_image(input_path, output_path, preserve_original):
                    processed_count += 1
    
    print(f"\nProcessed {processed_count} images total")


def main():
    parser = argparse.ArgumentParser(description="Remove metadata from images")
    parser.add_argument("input", help="Input image file or folder")
    parser.add_argument("-o", "--output", help="Output file or folder")
    parser.add_argument("--no-preserve", action="store_true", 
                       help="Overwrite original files instead of creating new ones")
    parser.add_argument("--no-recursive", action="store_true",
                       help="Don't process subfolders recursively")
    parser.add_argument("-v", "--verbose", action="store_true",
                       help="Verbose output")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input):
        print(f"Error: Input path '{args.input}' does not exist")
        sys.exit(1)
    
    preserve_original = not args.no_preserve
    recursive = not args.no_recursive
    
    if os.path.isfile(args.input):
        # Single file processing
        success = remove_metadata_from_image(args.input, args.output, preserve_original)
        sys.exit(0 if success else 1)
    
    elif os.path.isdir(args.input):
        # Folder processing
        process_folder(args.input, args.output, preserve_original, recursive)
    
    else:
        print(f"Error: '{args.input}' is not a valid file or directory")
        sys.exit(1)


if __name__ == "__main__":
    # If run without arguments, show example usage
    if len(sys.argv) == 1:
        print("Image Metadata Remover")
        print("=" * 50)
        print("Usage examples:")
        print("  python remove_metadata.py image.jpg")
        print("  python remove_metadata.py image.png -o clean_image.png")
        print("  python remove_metadata.py /path/to/folder")
        print("  python remove_metadata.py /path/to/folder -o /path/to/clean_folder")
        print("  python remove_metadata.py folder --no-preserve  # overwrite originals")
        print("\nFor full help: python remove_metadata.py --help")
        print("\nSupported formats: JPG, PNG, TIFF, BMP, WebP")
        sys.exit(0)
    
    main()
