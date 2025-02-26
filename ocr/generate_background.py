from PIL import Image, ImageDraw

# =========== Metadata ===========
# All size formats are (width, height)
page_size = (1668, 2157)    # Pixles are from 0-1667, 0-2156

top_margin = 150
left_margin = 150
right_margin = 150

block_width = 72            # For handwriting extraction
writing_width = 64          # For background generation, bounding space to actually write
buffer = (block_width-writing_width)/2 - 1
line_spacing = 2
# =================================


def get_writing_space(left, top):
    '''
    Takes the top left pixel location of a block,
    generate the bounding box to draw the writing area
    output format [(x0, y0), (x1, y1)]
    '''
    x0 = left + buffer
    x1 = x0 + writing_width + 1
    y0 = top + buffer
    y1 = y0 + writing_width + 1
    return [(x0, y0), (x1, y1)]

def get_n_blocks(left, top, n=4):
    '''
    Takes the top left pixel of a 4*1 horizontol block,
    generate a list of rectangles for each writing area
    '''
    rectangles = []
    for i in range(n):
        rectangles.append(get_writing_space(left + i*block_width, top))
    return rectangles

def get_line(left, top, m=4, n=4):
    '''
    Takes the top left pixel of a 16*1 horizontal block,
    generate a list of rectangles for each writing area
    '''
    rectangles = []
    for i in range(m):
        rectangles += get_n_blocks(
            left + i*n*block_width + i*block_width,
            top, n=n
        )
    return rectangles

def get_page(left, top, m=4, n=4, l=25):
    '''
    Take the top left pixel of a 16*25 block,
    generate the list of rectangles for each writing area
    '''
    rectangles = []
    for i in range(l):
        rectangles += get_line(
            left,
            top + i*block_width + i*line_spacing,
            m=m, n=n
        )
    return rectangles


if __name__ == '__main__':
    image = Image.new('RGB', page_size, 'white')
    draw = ImageDraw.Draw(image)

    rectangles = get_page(left_margin, top_margin)
    for r in rectangles:
        draw.rectangle(r, outline='black')
    draw.text([150,35], 'Date:', fill='black', font_size=60)


    image.save('ocr/images/background/background.bmp', 'BMP')