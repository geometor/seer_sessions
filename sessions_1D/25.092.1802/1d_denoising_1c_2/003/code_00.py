"""
Accepts a 2D NumPy array (input_grid).
Flattens the grid into a 1D sequence.
Identifies the unique non-zero foreground color (C).
Finds all contiguous blocks (runs) of color C in the flattened sequence.
Identifies the single longest contiguous block. If there's a tie in length, the block occurring earliest (smallest starting index) in the flattened sequence is chosen.
Creates a new 2D grid of the same dimensions as the input, initialized with the background color (0).
Copies the pixels corresponding to the identified longest block from their position in the flattened input sequence to the corresponding position in the new grid (after flattening and before reshaping).
All other pixels in the output grid remain the background color.
Returns the resulting 2D grid.
"""

import numpy as np

def find_contiguous_blocks_flat(flat_data, target_color):
    """
    Finds all contiguous blocks of a target color in a 1D numpy array.
    Returns a list of dictionaries, where each dictionary represents a block
    with 'start' index, 'end' index (exclusive), and 'length'.
    """
    blocks = []
    start_index = -1
    n = len(flat_data)
    for i, pixel in enumerate(flat_data):
        if pixel == target_color and start_index == -1:
            # Start of a new block
            start_index = i
        elif pixel != target_color and start_index != -1:
            # End of the current block (pixel at i is not part of it)
            blocks.append({'start': start_index, 'end': i, 'length': i - start_index})
            start_index = -1
            
    # Check if a block extends to the very end of the list
    if start_index != -1:
        blocks.append({'start': start_index, 'end': n, 'length': n - start_index})
        
    return blocks

def transform(input_grid):
    # 1. Record the shape (height, width) of the input grid.
    original_shape = input_grid.shape
    
    # 2. Flatten the input grid into a 1D sequence.
    flat_input = input_grid.flatten()
    grid_size = len(flat_input)
    background_color = 0

    # 3. Identify the unique foreground color C.
    foreground_color = -1 # Default if no foreground color found
    for pixel in flat_input:
        if pixel != background_color:
            foreground_color = pixel
            break 

    # 4. Handle case where input is entirely background or no foreground color found
    if foreground_color == -1:
        return np.zeros(original_shape, dtype=int)

    # 5 & 6. Find all contiguous blocks of color C in the 1D sequence.
    blocks = find_contiguous_blocks_flat(flat_input, foreground_color)

    # 7. Handle case where no blocks of the foreground color were found
    if not blocks:
        return np.zeros(original_shape, dtype=int)

    # 8. Find the block with the maximum length (earliest start index for ties).
    longest_block = None
    max_length = -1 
    # Find max length first
    for block in blocks:
         if block['length'] > max_length:
              max_length = block['length']
    
    # Find the first block matching the max length
    for block in blocks:
        if block['length'] == max_length:
            longest_block = block
            break # Stop at the first longest block encountered

    # 9. Create a new 1D array filled with the background color.
    output_flat = np.full(grid_size, background_color, dtype=int)

    # 10. Copy the longest block from flattened input to the new 1D array.
    if longest_block: # Should always be true if blocks were found, but check for safety
        start = longest_block['start']
        end = longest_block['end']
        output_flat[start:end] = flat_input[start:end] 

    # 11. Reshape the new 1D array back into the original 2D grid dimensions.
    output_grid = output_flat.reshape(original_shape)

    # 12. Return the resulting 2D grid.
    return output_grid