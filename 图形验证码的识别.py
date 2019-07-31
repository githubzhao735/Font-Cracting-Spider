from PIL import Image
import pytesseract


img = Image.open("./price_img.png")
img = img.convert("L")
s = pytesseract.image_to_string(img)

print(s,type(s))




