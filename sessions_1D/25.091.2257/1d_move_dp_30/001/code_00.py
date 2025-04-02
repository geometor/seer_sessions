import numpy as np

"""
Identifies a contiguous block of a non-white (0), non-gray (5) color and a single gray (5) pixel in a 1D input grid.
Calculates the number of white (0) pixels separating the right edge of the color block and the gray pixel.
Shifts the color block to the right by this number of white pixels, making it adjacent to the gray pixel.
The gray pixel's position remains unchanged. All other pixels become white (0).

Workflow:
1. Convert the input list to a numpy array for easier indexing.
2. Find the index (column position) of the gray pixel (5).
3. Find the contiguous block of the primary color (not 0 or 5), recording its color, start index, and end index.
4. Count the white pixels (0) between the end of the color block and the gray pixel.
5. Create an output grid of the same size, initialized to white (0).
6. Place the gray pixel (5) in the output grid at its original index.
7. Calculate the new starting position for the color block by adding the count of separating white pixels to its original start index.
8. Place the color block (using its identified color and length) into the output grid at the new calculated position.
9. Return the resulting output grid.
"""

def find_pixel_index(grid_1d, color):
    """Finds the index of the first occurrence of a specific color in a 1D numpy array."""
    indices = np.where(grid_1d == color)[0]
    if len(indices) > 0:
        return indices[0]
    return -1 # Not found

def find_color_block(grid_1d):
    """Finds the contiguous block of non-white, non-gray color."""
    block_color = -1
    block_start = -1
    block_end = -1
    in_block = False
    for i, pixel in enumerate(grid_1d):
        # Check if the pixel is the start of a potential block
        if pixel != 0 and pixel != 5 and not in_block:
            block_color = pixel
            block_start = i
            block_end = i # Initialize end index
            in_block = True
        # Check if we are continuing the block
        elif in_block and pixel == block_color:
            block_end = i # Update end index
        # Check if we just exited the block
        elif in_block and pixel != block_color:
            break # Block ended
            
    if block_start != -1:
        return block_color, block_start, block_end
    else:
        # Should not happen based on task description, but handle gracefully
        return None, -1, -1


def transform(input_grid):
    """
    Shifts a color block rightwards to be adjacent to a stationary gray pixel.
    """
    # Convert input to numpy array for easier processing
    # Assuming input_grid is a single list representing the row
    input_np = np.array(input_grid, dtype=int)
    grid_width = len(input_np)

    # Initialize output grid with white (0)
    output_np = np.zeros(grid_width, dtype=int)

    # Find the gray pixel's index
    gray_idx = find_pixel_index(input_np, 5)
    if gray_idx == -1:
        # Handle error: Gray pixel not found (shouldn't happen per examples)
        return input_grid # Or raise an error

    # Find the color block details
    block_color, block_start, block_end = find_color_block(input_np)
    if block_color is None:
        # Handle error: Color block not found (shouldn't happen per examples)
        # If no block, maybe just return the grid with only the gray pixel?
        # For now, just place gray and return zeros elsewhere
        output_np[gray_idx] = 5
        return output_np.tolist() # Convert back to list format if needed

    # Count the number of white pixels between the block and the gray pixel
    separation_count = 0
    if block_end < gray_idx -1: # Check if there's space between them
       for i in range(block_end + 1, gray_idx):
           if input_np[i] == 0:
               separation_count += 1

    # Calculate the new starting position for the block
    new_block_start = block_start + separation_count
    block_length = block_end - block_start + 1

    # Place the gray pixel in the output
    output_np[gray_idx] = 5

    # Place the color block in the output at its new position
    # Ensure the block doesn't overwrite the gray pixel or go out of bounds
    # (Though the logic implies it ends right before the gray pixel)
    new_block_end = new_block_start + block_length -1
    if new_block_end < gray_idx: # Check if new position is valid
        output_np[new_block_start : new_block_start + block_length] = block_color
    else:
        # Handle potential collision or unexpected state if logic is flawed
        # For now, assume the logic holds and this else won't be needed
        # Based on examples, block should end exactly at gray_idx - 1
        output_np[new_block_start : new_block_start + block_length] = block_color


    # Convert numpy array back to list for the final output
    return output_np.tolist()