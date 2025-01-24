以下是你的 `README.md` 文件，它概述了 `modify_image_colors.py` 的功能、用法和示例。  

---

### **README.md**

# **Image Color Modifier**
This script modifies the background and foreground colors of an image, supporting transparent backgrounds and selective color replacement.

## **Features**
- Replace the background color with a new color or make it transparent.
- Replace specific foreground colors.
- Convert all non-background colors to a new foreground color.
- Support for JPG and PNG images.
- Adjustable color matching tolerance.

## **Requirements**
Install the dependencies before running the script:
```bash
pip install numpy opencv-python pillow
```

## **Usage**
The script can be executed directly from Python with various options:

### **1. Replace white background with transparency**
```python
modify_image_colors(
    "input.jpg",
    "output.png",
    target_bg_color=(255, 255, 255),  # White background
    new_bg_color=None                 # Transparent background
)
```

### **2. Replace white background with black and change black foreground to green**
```python
modify_image_colors(
    "input.jpg",
    "output.png",
    target_bg_color=(255, 255, 255),  # White background
    new_bg_color=(0, 0, 0),           # Black background
    target_fg_color=(0, 0, 255),      # Blue foreground
    new_fg_color=(0, 255, 0),         # Change to green
    tolerance=100
)
```

### **3. Change all non-background colors to green**
```python
modify_image_colors(
    "input.jpg",
    "output.png",
    target_bg_color=(255, 255, 255),  # White background
    new_bg_color=None,                # Transparent background
    new_fg_color=(0, 255, 0),         # Convert all non-background to green
    change_all_fg=True,
    tolerance=40
)
```

## **Parameters**
| Parameter | Type | Description |
|-----------|------|-------------|
| `input_path` | `str` | Path to the input image. |
| `output_path` | `str` | Path to save the modified image. |
| `target_bg_color` | `tuple` or `str` | Background color to replace (RGB or HEX). Default: `(255, 255, 255)` (white). |
| `new_bg_color` | `tuple` or `str` | New background color (RGB, RGBA, HEX). `None` makes it transparent. |
| `target_fg_color` | `tuple` | Foreground color to replace (RGB). `None` means no change. |
| `new_fg_color` | `tuple` | New foreground color (RGB, RGBA, HEX). `None` means no change. |
| `change_all_fg` | `bool` | If `True`, change all non-background pixels to `new_fg_color`. Default: `False`. |
| `tolerance` | `int` | Color matching tolerance (higher = more flexible matching). Default: `40`. |

## **Notes**
- PNG images retain transparency support.
- JPG images do not support transparency but can have their backgrounds replaced.
- Increasing `tolerance` helps match similar colors more flexibly.
- `change_all_fg=True` overrides `target_fg_color` and modifies all non-background pixels.

## **License**
This script is open-source. Feel free to modify and distribute it.