#!/usr/bin/env python3
"""
Image optimization script for portfolio website
Converts images larger than 1MB to optimized formats using PIL
"""

import os
import sys
from pathlib import Path

try:
    from PIL import Image, ImageOps
    print("✓ PIL found")
except ImportError:
    print("✗ PIL not found. Install with: pip install Pillow")
    sys.exit(1)

def check_dependencies():
    """Check if required libraries are available"""
    return True

def get_file_size_mb(filepath):
    """Get file size in MB"""
    return os.path.getsize(filepath) / (1024 * 1024)

def optimize_image(input_path, quality=85, max_dimension=1920):
    """
    Optimize image using PIL
    - Keep original with _original suffix
    - Replace original with optimized version (same format)
    - Reduce quality and dimensions for large images
    """
    input_path = Path(input_path)
    stem = input_path.stem
    suffix = input_path.suffix.lower()
    original_path = input_path.parent / f"{stem}_original{suffix}"
    
    original_size = get_file_size_mb(input_path)
    
    # Create backup with _original suffix
    if not original_path.exists():
        import shutil
        shutil.copy2(input_path, original_path)
        print(f"📁 Original saved: {original_path.name}")
    
    try:
        # Open and optimize image
        with Image.open(input_path) as img:
            # Convert RGBA to RGB for JPEG
            if suffix in ['.jpg', '.jpeg'] and img.mode in ['RGBA', 'LA', 'P']:
                # Create white background
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            
            # Resize if too large
            if max(img.size) > max_dimension:
                img.thumbnail((max_dimension, max_dimension), Image.Resampling.LANCZOS)
            
            # Remove EXIF data
            img = ImageOps.exif_transpose(img)
            
            # Save optimized version
            save_kwargs = {'optimize': True}
            if suffix in ['.jpg', '.jpeg']:
                save_kwargs['quality'] = quality
                save_kwargs['progressive'] = True
            elif suffix == '.png':
                save_kwargs['optimize'] = True
                # Convert to palette if possible for smaller file size
                colors = img.getcolors(maxcolors=256)
                if img.mode == 'RGBA' and colors and len(colors) <= 256:
                    img = img.quantize(colors=256, method=Image.Quantize.MEDIANCUT)
            
            img.save(input_path, **save_kwargs)
        
        final_size = get_file_size_mb(input_path)
        reduction = (1 - final_size/original_size) * 100
        
        if reduction > 10:  # Only consider successful if >10% reduction
            print(f"✓ {input_path.name}: {original_size:.1f}MB → {final_size:.1f}MB ({reduction:.1f}% reduction)")
            return True
        else:
            # Restore original if no significant improvement
            import shutil
            shutil.copy2(original_path, input_path)
            os.remove(original_path)
            print(f"⚠ {input_path.name}: No significant improvement, keeping original")
            return False
            
    except Exception as e:
        print(f"✗ Failed to optimize {input_path.name}: {e}")
        # Restore original if optimization failed
        if original_path.exists():
            import shutil
            shutil.copy2(original_path, input_path)
            os.remove(original_path)
        return False

def main():
    if not check_dependencies():
        sys.exit(1)
    
    # Find all images larger than 1MB
    docs_path = Path('docs/artifacts')
    large_images = []
    
    for ext in ['*.jpg', '*.jpeg', '*.png']:
        for img_path in docs_path.rglob(ext):
            if get_file_size_mb(img_path) > 1.0:
                large_images.append(img_path)
    
    if not large_images:
        print("No images larger than 1MB found.")
        return
    
    print(f"Found {len(large_images)} images larger than 1MB")
    print("Starting optimization...\n")
    
    optimized_count = 0
    total_original_size = 0
    total_final_size = 0
    
    for img_path in large_images:
        original_size = get_file_size_mb(img_path)
        total_original_size += original_size
        
        if optimize_image(img_path):
            optimized_count += 1
        
        total_final_size += get_file_size_mb(img_path)
    
    # Summary
    total_reduction = (1 - total_final_size/total_original_size) * 100
    print(f"\n📊 Optimization Summary:")
    print(f"   Images processed: {len(large_images)}")
    print(f"   Images optimized: {optimized_count}")
    print(f"   Total size reduction: {total_original_size:.1f}MB → {total_final_size:.1f}MB ({total_reduction:.1f}%)")
    print(f"   Space saved: {total_original_size - total_final_size:.1f}MB")

if __name__ == '__main__':
    main()