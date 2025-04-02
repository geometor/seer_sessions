```python
import copy

"""
Shift a contiguous block of color rightward towards a stationary marker pixel (azure, 8).
The distance of the shift is determined by the number of background pixels (white, 0)
located strictly between the right end of the block and the marker pixel in the input.
"""

def find_marker_index(grid, marker_color=8):
    """Finds the index of the first occurrence of the marker color."""
    for i, pixel in enumerate(grid):
        if pixel == marker_color:
            return i
    return -1 # Should not happen based on task description

def find_main_block(grid, background_color=0, marker_color=8):
    """Finds the contiguous block of non-background, non-marker color."""
    block_color = -1
    start_index = -1
    end_index = -1
    in_block = False

    for i, pixel in enumerate(grid):
        is_main_color = (pixel != background_color and pixel != marker_color)

        if is_main_color and not in_block:
            # Start of a potential block
            block_color = pixel
            start_index = i
            in_block = True
        elif in_block and pixel != block_color:
            # End of the block
            end_index = i - 1
            in_block = False
            break # Assume only one block
        elif is_main_color and in_block and i == len(grid) - 1:
             # Block ends at the end of the grid
             end_index = i

    # If the loop finished while still in_block (block goes to the end)
    if in_block and end_index == -1:
        end_index = len(grid) - 1

    if start_index != -1 and end_index != -1:
         return block_color, start_index, end_index
    else:
        # Handle cases where no block is found, though unlikely given examples
        return -1, -1, -1


def calculate_shift_distance(grid, block_end_index, marker_index, background_color=0):
    """Calculates the number of background pixels between the block end and marker."""
    count = 0
    # Iterate strictly between block_end + 1 and marker_index - 1
    for i in range(block_end_index + 1, marker_index):
        if grid[i] == background_color:
            count += 1
    return count

def transform(input_grid):
    """
    Applies the shifting transformation to the input grid.

    Args:
        input_grid: A list of integers representing the input grid pixels.

    Returns:
        A list of integers representing the transformed output grid pixels.
    """
    # Initialize output_grid as a copy of the input
    output_grid = list(input_grid) # Use list() for shallow copy if input is list
    
    background_color = 0
    marker_color = 8

    # 1. Find the position (index) of the marker pixel (8).
    marker_idx = find_marker_index(output_grid, marker_color)
    if marker_idx == -1:
        # Handle error: marker not found (though problem implies it exists)
        return output_grid # Or raise error

    # 2. Find the main block's color, start index, and end index.
    block_color, start_idx, end_idx = find_main_block(output_grid, background_color, marker_color)
    if block_color == -1:
         # Handle error: main block not found
         return output_grid # Or raise error

    # 3. Count background pixels between block end and marker.
    shift_distance = calculate_shift_distance(output_grid, end_idx, marker_idx, background_color)

    # 4. Perform the shift if distance > 0
    if shift_distance > 0:
        # Iterate shift_distance times to update the grid
        # We shift elements from left to right within the block's original span
        # and fill the new positions to the right.
        for i in range(shift_distance):
            # Set the leftmost pixel of the original block location to background
            output_grid[start_idx + i] = background_color
            # Set the pixel just after the original block end location to block color
            # Note: end_idx + 1 is the first position *after* the original block
            output_grid[end_idx + 1 + i] = block_color

    # 5. Return the modified grid
    return output_grid
```