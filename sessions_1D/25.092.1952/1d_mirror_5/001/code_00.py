"""
Transforms a 1D array by relocating a contiguous block of color relative to a fixed marker pixel (maroon, 9).

The transformation identifies a single maroon pixel (9) and a single contiguous block of another color (not white '0' or maroon '9'). The block, which initially appears before the maroon pixel, is moved to appear after the maroon pixel. The number of white pixels (0) separating the block and the marker remains the same, but the block is now on the other side of the marker.
"""

import numpy as np

def find_marker(grid, marker_color=9):
    """Finds the index of the first occurrence of the marker color."""
    for i, pixel in enumerate(grid):
        if pixel == marker_color:
            return i
    return -1 # Should not happen based on task description

def find_colored_block(grid, background_color=0, marker_color=9):
    """Finds the color, start index, and end index of the colored block."""
    block_color = -1
    start_index = -1
    end_index = -1
    in_block = False

    for i, pixel in enumerate(grid):
        if pixel != background_color and pixel != marker_color:
            if not in_block:
                # Start of a new block
                block_color = pixel
                start_index = i
                in_block = True
            # Update end_index as long as we are in the block
            end_index = i
        elif in_block:
            # End of the block found
            break # Since there's only one block expected

    if block_color != -1:
        return block_color, start_index, end_index
    else:
        return None, -1, -1 # Should not happen if block always exists


def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list): A list of integers representing the 1D input grid.

    Returns:
        list: A list of integers representing the transformed 1D output grid.
    """
    # Convert input list to numpy array for easier handling
    input_array = np.array(input_grid)
    grid_size = len(input_array)
    background_color = 0
    marker_color = 9

    # Initialize output_grid with the background color
    output_array = np.full(grid_size, background_color, dtype=int)

    # 1. Identify the single maroon pixel (9) and its index
    marker_index = find_marker(input_array, marker_color)
    if marker_index == -1:
         # Handle error or unexpected input: If no marker, return input? Or empty?
         # For now, assuming marker always exists per task description.
         # Let's place the marker if found, even if block logic fails later.
         print("Warning: Marker not found!") # Or raise an error
         return input_grid # Or some error state

    # 2. Place the maroon pixel (9) at its original index in the output array
    output_array[marker_index] = marker_color

    # 3. Identify the colored block: color, start, end index
    block_color, block_start_index, block_end_index = find_colored_block(
        input_array, background_color, marker_color
    )

    if block_color is None:
        # Handle error or unexpected input: If no block, return current output?
        print("Warning: Colored block not found!") # Or raise an error
        # Return the output with just the marker placed, or the original input?
        # Based on examples, a block always exists. If not, returning current state seems reasonable.
        return output_array.tolist()

    # 4. Calculate block length
    block_length = block_end_index - block_start_index + 1

    # 5. Calculate the distance D (number of background pixels) between the block and the marker
    # D = marker_index - block_end_index - 1
    distance_d = marker_index - block_end_index - 1

    # 6. Calculate the new starting index for the block in the output array
    # new_start_index = marker_index + 1 + D
    new_start_index = marker_index + 1 + distance_d

    # 7. Place the colored block into the output array at the new position
    new_end_index = new_start_index + block_length
    if new_end_index <= grid_size: # Ensure it fits within bounds
        output_array[new_start_index:new_end_index] = block_color
    else:
        # Handle error: block doesn't fit in the new position
        print(f"Error: Calculated new block position [{new_start_index}:{new_end_index}] exceeds grid size {grid_size}.")
        # Decide error handling: return partially filled, original, or raise error.
        # For now, returning the array with marker placed but block missing.
        pass # Block placement is skipped

    # Convert numpy array back to list for the final output
    return output_array.tolist()