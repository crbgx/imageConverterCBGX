from PIL import Image
from datetime import datetime

# This program has been made to convert from .png to .coe
# The .coe file is used to initialize the memory of the FPGA
# The .coe block memory depth is: ImageWidth * ImageHeight
# The .coe width is: 3 (the RGB values)
# Useful for projects 4 & 5 in VLSI Design at LTH

globalPath = '/home/cbgx/Desktop/Images/'
imageName = '0'
fileType = '.png'

im = Image.open(f'{globalPath}{imageName}{fileType}')
pix = im.load()

if im.mode != 'RGB' and im.mode != 'RGBA':
    print(f'Mode is {im.mode}')
    print('Please convert to RGB or RGBA')
    exit()

memoryBlockDepth = im.size[0] * im.size[1]
rgbArray = []

# Get the RGB values of each pixel (R,G,B,O)
for y in range(0,im.size[1]):
    for x in range(0,im.size[0]):
        # Removing O information
        if im.mode == 'RGBA':
            tempList = list(pix[x,y][:-1])
        else:
            tempList = list(pix[x,y])

        # Normalizing to 0 or 1
        for i in range(0, len(tempList)):
            tempList[i] = 0 if tempList[i]/255 < 0.5 else 1

        # Making it all a joined string
        tempString = ''.join(str(e) for e in tempList)
        rgbArray.append(tempString)


# Write into the .coe file
with open(f'{globalPath}{imageName}_{im.size[0]}x{im.size[1]}.coe', 'w') as f:
    f.write(f'; Xilinx block memory configuration file (.COE) generated by Image Converter CBGX {datetime.today().isoformat(timespec="minutes")}\n')
    f.write(f'; This .COE file specifies the contents for a block memory of depth = {memoryBlockDepth}, and width = 3.\n')
    f.write(f'memory_initialization_radix=2;\n')
    f.write(f'memory_initialization_vector=\n')
    for index, x in enumerate(rgbArray):
        if index == memoryBlockDepth-1:
            f.write(f'{x};\n')
        else:
            f.write(f'{x},\n')

print(f'Image {imageName}{fileType} was converted to {imageName}_{im.size[0]}x{im.size[1]}.coe')