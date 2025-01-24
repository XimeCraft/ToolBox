import cv2
import numpy as np
from PIL import Image, ImageColor
import os

def modify_image_colors(
    input_path,
    output_path,
    target_bg_color=(255, 255, 255),  # replace bg color (RGB)
    new_bg_color=None,                # new bg color (RGB, RGBA, or HEX, None means transparent)
    target_fg_color=None,             # replace fg color (RGB, None means not replace fg)
    new_fg_color=None,                # new fg color (RGB, RGBA, or HEX, None means not replace)
    change_all_fg=False,              # if True, change all non-background colors to new_fg_color
    invert_mask=False,                # if True, invert the color matching mask
    tolerance=40                      # color match tolerance
):
    
    # ===[1. parse color]===
    def parse_color(color):
        """
        Parse color to RGB array
        """
        if color is None:
            return None
        if isinstance(color, str):  # HEX
            color = ImageColor.getrgb(color)
        return np.array(color[:3])  # only RGB
    
    target_bg_color = parse_color(target_bg_color)
    new_bg_color = parse_color(new_bg_color)
    target_fg_color = parse_color(target_fg_color)
    new_fg_color = parse_color(new_fg_color)

    # ===[2. read image]===
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input image not found: {input_path}")
        
    if input_path.lower().endswith('.png'):
        # PNG may contain transparent channel, use PIL to read
        try:
            image = np.array(Image.open(input_path))
            if len(image.shape) == 2:  # grayscale
                image = np.dstack((image, image, image))
            if image.shape[2] == 3:  # if no Alpha channel
                image = np.dstack((image, np.full(image.shape[:2], 255)))
        except Exception as e:
            raise Exception(f"Failed to read PNG image: {e}")
    else:
        # JPG use OpenCV to read, need to convert BGR->RGB
        image = cv2.imread(input_path)
        if image is None:
            raise Exception(f"Failed to read image: {input_path}")
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = np.dstack((image, np.full(image.shape[:2], 255)))

    # ===[3. create bg and fg mask]===
    output_image = image.copy()
        
    # process bg
    if target_bg_color is not None:
        bg_diff = np.sqrt(np.sum((image[:, :, :3].astype(float) - target_bg_color) ** 2, axis=2))
        bg_mask = bg_diff < tolerance
        
        if invert_mask:
            bg_mask = ~bg_mask  # invert the mask for cases like gradient background
            
        if new_bg_color is None:  # set transparent
            output_image[bg_mask, 3] = 0
        else:  # replace to new color
            output_image[bg_mask, :3] = new_bg_color
            
        # if change_all_fg is True, change all non-background pixels to new_fg_color
        if change_all_fg and new_fg_color is not None:
            fg_mask = ~bg_mask  # inverse of bg_mask
            output_image[fg_mask, :3] = new_fg_color
    
    # process specific fg color if needed
    elif target_fg_color is not None and new_fg_color is not None:
        fg_diff = np.sqrt(np.sum((image[:, :, :3].astype(float) - target_fg_color) ** 2, axis=2))
        fg_mask = fg_diff < tolerance
        if invert_mask:
            fg_mask = ~fg_mask
        output_image[fg_mask, :3] = new_fg_color

    # ===[4. save image]===
    output_image = output_image.astype(np.uint8)
    Image.fromarray(output_image).save(output_path)
    print(f"image saved to {output_path}")

# example:
if __name__ == "__main__":
    # 1. only replace white bg to transparent
    modify_image_colors(
        "IconColorModify/images/5.jpg",
        "IconColorModify/images/outputs/output5.png",
        target_bg_color=(0, 0, 0),  # white bg
        new_bg_color=None                 # None means transparent
    )

    # 2. replace white bg to black and blue fg to black
    modify_image_colors(
        "IconColorModify/images/6.jpg",
        "IconColorModify/images/outputs/output6.png",
        target_bg_color=(255, 255, 255),
        new_bg_color=None,
        target_fg_color=(0, 0, 0),     
        new_fg_color=(0, 255, 0),
        tolerance=100
    )
    
    # 3. change all non-background colors to green
    modify_image_colors(
        "IconColorModify/images/7.jpg",
        "IconColorModify/images/outputs/output7.png",
        target_bg_color=(255, 255, 255),  # white background
        new_bg_color=None,                # transparent background
        new_fg_color=(0, 255, 0),         # change all non-background
        change_all_fg=True,               # enable change all foreground
        tolerance=40
    )
    
    # 4. handle gradient background by matching dark content
    modify_image_colors(
        "IconColorModify/images/4.jpg",
        "IconColorModify/images/outputs/output4.png",
        target_bg_color=(0, 0, 0),        # match black content
        new_bg_color=None,                # make it transparent
        tolerance=60,                      # higher tolerance for better matching
        invert_mask=True                  # invert mask to keep black content and remove background
    )