import os, glob
from PIL import Image

magick = "ImageMagick\\magick.exe"  # path to your ImageMagic
source = "test.png"  # image you want to intelace
offset = 0.003  # use between 0.001 and 0.003 

with Image.open(source) as img:  # get size of the image
    width, height = img.size

offset = round(width * offset)  # calculate amount of pixels from percentage of width
if offset < 1:  # if the result is less than 1 force 1
    offset = 1

for i in range(0, height, 2):  # extract even lines
    percentage = round((i / height)*100, 2)
    print(f"{magick} {source} -crop x1+0+{i} even\\line_{str(i).zfill(4)}.png ({percentage}%)")
    os.system(f"{magick} {source} -crop x1+0+{i} even\\line_{str(i).zfill(4)}.png")

for i in range(1, height, 2):  # exctact odd lines
    percentage = round((i / height)*100, 2)
    print(f"{magick} {source} -crop x1+0+{i} all\\line_{str(i).zfill(4)}.png ({percentage}%)")
    os.system(f"{magick} {source} -crop x1+0+{i} all\\line_{str(i).zfill(4)}.png")

even_lines = glob.glob("even\\*.png")  # get a list of even lines

for i, line in enumerate(even_lines):  # offset even lines and crop them
    percentage = round((i / len(even_lines))*100, 2)
    print(f"{magick} {line} -background white -splice {offset}x0 +repage {line[:-4]}_shift.png ({percentage}%)")
    os.system(f"{magick} {line} -background white -splice {offset}x0 +repage {line[:-4]}_shift.png")
    print(f"{magick} {line[:-4]}_shift.png -crop {width}x1+0+0 {line[:-4]}_done.png")
    os.system(f"{magick} {line[:-4]}_shift.png -crop {width}x1+0+0 {line[:-4]}_done.png")

even_lines_done = glob.glob("even\\*_done.png")  # get a list of finalized even lines

for i, line in enumerate(even_lines_done):  # copy finalized even lines to all directory
    percentage = round((i / len(even_lines_done))*100, 2)
    print(f"copy {line} all\\{line[5:-9]}.png ({percentage}%)")
    os.system(f"copy {line} all\\{line[5:-9]}.png")

print(f"del even\\*.png")
os.system(f"del even\\*.png")  # deleting everything in the even folder, dangerous

all_lines = glob.glob("all\\*png")  # get a list of all lines

current_line = str(all_lines[0])[4:]  # get name of the first line and remove folder name from it

for i in range(1, len(all_lines)):  # append all of the pictures together
    percentage = round((i / len(all_lines))*100, 2)
    next_line = all_lines[i]

    result_image = f"temp_{str(i).zfill(4)}.png"

    print(f"{magick} all\\{current_line} {next_line} -append all\\{result_image} ({percentage}%)")
    os.system(f"{magick} all\\{current_line} {next_line} -append all\\{result_image}")

    current_line = result_image

print(f"copy all\\temp_{str(height-1).zfill(4)}.png {source[:-4]}_interlaced.png")
os.system(f"copy all\\temp_{str(height-1).zfill(4)}.png {source[:-4]}_interlaced.png")  # copy the final image next to the original

print(f"del all\\*.png")
os.system(f"del all\\*.png")  # deleting everything in the all folder, dangerous
