
import numpy as np

def find_pixels(grid, color):
    # Find coordinates of pixels with the specified color.
    return np.array(np.where(grid == color)).T

def get_contiguous_blocks(pixels):
    # group pixels into contiguous sets, horizontally or vertically
    
    if len(pixels) == 0:
      return []

    blocks = []
    current_block = [pixels[0]]

    for i in range(1, len(pixels)):
        is_contiguous = False
        for prev_pixel in current_block:
            if (abs(pixels[i][0] - prev_pixel[0]) == 1 and pixels[i][1] == prev_pixel[1]) or \
               (abs(pixels[i][1] - prev_pixel[1]) == 1 and pixels[i][0] == prev_pixel[0]):
               is_contiguous = True
               break

        if is_contiguous:
          current_block.append(pixels[i])
        else:
            blocks.append(np.array(current_block))
            current_block = [pixels[i]]

    blocks.append(np.array(current_block))
    return blocks
    

def transform(input_grid):
    input_grid = np.array(input_grid)
    azure_pixels = find_pixels(input_grid, 8)
    print(f"Azure Pixels: {azure_pixels}")

    # Determine output dimensions and create an empty output grid.
    output_height = 3
    output_width = 6
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Group azure pixels into contiguous blocks
    blocks = get_contiguous_blocks(azure_pixels)
    print(f"Contiguous Blocks: {blocks}")

    # Identify rows that contribute
    row_map = {}
    for block in blocks:
        min_row = np.min(block[:, 0])
        max_row = np.max(block[:,0])

        top_row_pixels = block[block[:,0] == min_row]

        row_below = max_row + 1 if max_row + 1 < input_grid.shape[0] and np.any(input_grid[max_row+1,:]==8)  else None

        if min_row not in row_map:
          row_map[min_row] = {'output_row':0, 'pixels':top_row_pixels}
        else:
          #append the new pixels if rows are the same
          row_map[min_row]['pixels'] = np.vstack([row_map[min_row]['pixels'], top_row_pixels])
        
        if row_below is not None:
          row_pixels = block[block[:,0] == max_row]

          if row_below not in row_map:
              row_map[row_below] = {'output_row':2, 'pixels': row_pixels}
          else:
              row_map[row_below]['pixels'] = np.vstack([row_map[row_below]['pixels'], row_pixels])
    print(f"Row Map: {row_map}")

    # Fill the output grid.
    for input_row, data in row_map.items():
        output_row = data['output_row']
        pixels = data['pixels']
        for pixel in pixels:
          #if the pixel is on the edge - move it to the end
          adjusted_col = pixel[1]

          output_grid[output_row, adjusted_col] = 8
    
    #Find middle row elements by looking for isolated pixels not in a mapped row
    middle_row_pixels = []
    for block in blocks:
        for pixel in block:
            if pixel[0] not in row_map:
                middle_row_pixels.append(pixel)
    
    for pixel in middle_row_pixels:
        output_grid[1, pixel[1]] = 8 #add them

    print(f"Output Grid:\n{output_grid}")
    return output_grid

# Provided training data (replace with actual data loading)
train = [
    {
        "input": [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 8, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 8, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 8, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 8, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 8, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 8, 0, 0, 0, 0, 0],
        ],
        "output": [
            [8, 8, 8, 8, 8, 8],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
        ],
    },
    {
        "input": [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 8, 8, 8, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ],
        "output": [
            [0, 0, 8, 8, 8, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
        ],
    },
    {
        "input": [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 8, 8, 0, 0, 0, 0, 0],
            [0, 0, 0, 8, 8, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ],
        "output": [
            [0, 0, 0, 8, 8, 0],
            [0, 0, 0, 8, 8, 0],
            [0, 0, 0, 0, 0, 0],
        ],
    },
        {
        "input": [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 8, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 8, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 8, 0, 0, 0, 0, 0, 8, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 8, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ],
        "output": [
            [0, 8, 0, 0, 0, 0],
            [0, 8, 0, 0, 8, 0],
            [0, 8, 0, 0, 8, 0],
        ],
    },

]

for i, example in enumerate(train):
    print(f"\nExample {i+1}:")
    predicted_output = transform(example["input"])
    print(f"Correct Output:\n{np.array(example['output'])}")
    print(f"Match: {np.array_equal(predicted_output, np.array(example['output']))}")
