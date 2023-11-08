from PIL import Image,ImageFilter,ImageEnhance
from rembg import remove
from io import BytesIO
import numpy as np

def white_to_transparency(img):
    x = np.asarray(img.convert('RGBA')).copy()
    x[:, :, 3] &= (255 * (x[:, :, :3] != 255).any(axis=2)).astype(np.uint8)  # Small modification: &= is used instead of = (in the original code).
    return Image.fromarray(x)

def remove_bg(img_path):
    with open(img_path, 'rb') as img_file:
        img_data = img_file.read()
    output_img = remove(img_data)
    img_no_bg = Image.open(BytesIO(output_img))
    return img_no_bg

def get_shadow(alpha, img):
    width, height = alpha.size
    shape = Image.new('RGBA', (width, height), (250, 250, 250, 150))
    shape.putalpha(alpha)
    shape = shape.resize((int(img.width*1.5), int(img.height*1.5)), Image.NEAREST)
    shape = ImageEnhance.Brightness(shape).enhance(0.7)   # reduce the brightness
    shape = shape.filter(ImageFilter.GaussianBlur(20)) # Blur the image
    return shape

def compose_image(img_bg, img_no_bg):
    alpha = img_no_bg.split()[-1]
    alpha = alpha.filter(ImageFilter.MinFilter(3))
    width, height = alpha.size
    img_no_bg=img_no_bg.resize((img_bg.size[0]//2, img_bg.size[0]//2*height//width),Image.NEAREST)
    shadow = get_shadow(alpha, img_no_bg)
    shadow_data = shadow.getdata()
    new_data = []
    for item in shadow_data:
        # change all non-transparent 
        # pixels to have half transparency
        if item[3] > 0:
            new_data.append((item[0], item[1], item[2], 150))  # changing item[3] (alpha value)
        else:
            new_data.append(item)
    shadow.putdata(new_data)
    img_bg.paste(shadow, ((img_bg.width - shadow.width)//2, img_bg.height - shadow.height),shadow)
    img_bg.paste(img_no_bg, ((img_bg.width - img_no_bg.width)//2, img_bg.height - img_no_bg.height), img_no_bg)
    return img_bg
    

def main():
    img_no_bg = remove_bg('assets/handsome.png')
    img_bg = Image.open('assets/bg.jpg')
    img = compose_image(img_bg, img_no_bg)
    img.show()

# call this main function
if __name__ == '__main__':
    main()