import os, glob, time, subprocess
from PIL import Image

start = time.time()

magick = "ImageMagick\\magick.exe"  # path to your ImageMagic
source = "test6.png"  # image you want to intelace
offset = 0.01  # use between 0.001 and 0.003 

with Image.open(source) as img:  # get size of the image
    width, height = img.size

offset = round(width * offset)  # calculate amount of pixels from percentage of width
if offset < 1:  # if the result is less than 1 force 1
    offset = 1

for i in range(0, height, 2):  # extract even lines
    percentage = round((i / height)*100, 2)
    print(f"{magick} {source} -crop x1+0+{i} even\\line_{str(i).zfill(4)}.png ({percentage}%)")
    subprocess.Popen([magick, source, "-crop", f"x1+0+{i}", f"even\\line_{str(i).zfill(4)}.png"])

for i in range(1, height, 2):  # exctact odd lines
    percentage = round((i / height)*100, 2)
    print(f"{magick} {source} -crop x1+0+{i} all\\line_{str(i).zfill(4)}.png ({percentage}%)")
    subprocess.Popen([magick, source, "-crop", f"x1+0+{i}", f"all\\line_{str(i).zfill(4)}.png"])

even_lines = glob.glob("even\\*.png")  # get a list of even lines

for i, line in enumerate(even_lines):  # offset even lines and crop them
    percentage = round((i / len(even_lines))*100, 2)
    print(f"{magick} {line} -background white -splice {offset}x0 +repage -crop {width}x1+0+0 all\\{line[4:]}")
    subprocess.Popen([magick, line, "-background", "white", "-splice", f"{offset}x0", "+repage", "-crop", f"{width}x1+0+0", f"all\\{line[4:]}"])

print(f"del even\\*.png")
os.system(f"del even\\*.png")  # deleting everything in the even folder, dangerous

all_lines = glob.glob("all\\*png")  # get a list of all lines

# Function to split the list into chunks of 10
def chunk_lines(arr, size=10):
    return [arr[i:i + size] for i in range(0, len(arr), size)]

# Split all lines into chunks of 10 images
all_lines_chunks = chunk_lines(all_lines, 750)

# Process each chunk in parallel
for i in range(len(all_lines_chunks)):  # append all of the pictures together

    next_line = all_lines_chunks[i]

    result_image = f"all\\temp_{str(i).zfill(4)}.png"

    print(i)

    if i == 0:
        command = [magick] + next_line + ["-append", result_image]
    else:
        command = [magick, current_line] + next_line + ["-append", result_image]
    
    # Print the command for debugging
    print(command)
    
    # Run the command in the background
    subprocess.run(command)

    current_line = result_image

print(f"copy {result_image} {source[:-4]}_interlaced.png")
os.system(f"copy {result_image} {source[:-4]}_interlaced.png")

print(f"del all\\*.png")
os.system(f"del all\\*.png")  # deleting everything in the all folder, dangerous

end = time.time()
result = end - start
print(f"started {start}, ended {end}, took {result}")
