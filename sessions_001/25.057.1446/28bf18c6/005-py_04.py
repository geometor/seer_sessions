import numpy as np

# Provided code (slightly modified for concise execution)
def find_pixels(grid, color):
    return np.array(np.where(grid == color)).T

def get_contiguous_blocks(pixels):    
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
    output_grid = np.zeros((3, 6), dtype=int)
    azure_pixels = find_pixels(input_grid, 8)
    blocks = get_contiguous_blocks(azure_pixels)
    output_row_offset = 0
    output_col_offset = 0

    for block in blocks:
        min_row = np.min(block[:, 0])
        min_col = np.min(block[:, 1])
        relative_positions = block - [min_row, min_col]
        for pos in relative_positions:
          target_row = output_row_offset + pos[0]
          target_col = output_col_offset + pos[1]
          if target_row < 3 and target_col < 6:
              output_grid[target_row, target_col] = 8
        max_block_width = max(relative_positions[:,1]) + 1
        output_col_offset += max_block_width
        if output_col_offset >= 6:
            output_col_offset = 0
            output_row_offset +=1
    return output_grid

# Example Data (from the ARC task)
train_inputs = [
    np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 8, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 8, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
    np.array([[0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 8, 8, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 8, 8, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0]]),
    np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 8, 8, 8, 8, 0, 0, 0, 0],
              [0, 8, 8, 8, 8, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0]]),
]
train_outputs = [
    np.array([[0, 0, 8, 0, 0, 0],
              [0, 0, 8, 0, 0, 0],
              [0, 0, 0, 0, 0, 0]]),
    np.array([[8, 8, 0, 8, 8, 0],
              [0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0]]),
    np.array([[8, 8, 8, 8, 0, 0],
              [8, 8, 8, 8, 0, 0],
              [0, 0, 0, 0, 0, 0]]),
]

# Execute and check
for i, (input_grid, expected_output) in enumerate(zip(train_inputs, train_outputs)):
    predicted_output = transform(input_grid)
    print(f"Example {i+1}:")
    print("Input:\n", input_grid)
    print("Predicted Output:\n", predicted_output)
    print("Expected Output:\n", expected_output)
    print("Match:", np.array_equal(predicted_output, expected_output))
    print("-" * 20)
