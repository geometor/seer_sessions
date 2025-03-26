import numpy as np
from typing import List

def find_last_non_white_pixel(row: List[int]):
    """
    Finds the color and index of the last non-white pixel in a row.
    Assumes there is at least one non-white pixel starting from the left.
    """
    color = 0
    last_index = -1
    for i, pixel in enumerate(row):
        if pixel != 0:
            color = pixel
            last_index = i
        else:
            # Stop searching once the first white pixel after a non-white block is found
            if last_index != -1:
                break
    # If the entire row is non-white
    if last_index == len(row) - 1 and color != 0:
         return color, last_index
    # If only non-white pixels exist at the beginning
    elif last_index != -1:
        return color, last_index
    # Handle case where the row might start with white (shouldn't happen based on examples)
    # or is all white (also shouldn't happen)
    # Let's assume the examples cover the expected structure: non-white block then white
    # If first pixel is non-white and rest are white:
    if last_index == 0 and row[0] != 0:
         return row[0], 0

    # Fallback/Error case (or maybe row is all white?) - based on examples, this path shouldn't be hit
    # If row is all white:
    if last_index == -1:
        # Find the first non-zero if it exists, assumes non-white must start at index 0 based on examples.
        for i, pixel in enumerate(row):
            if pixel != 0:
                return pixel, i # Should be 0 based on examples
        return 0, -1 # Indicate all white or error


    return color, last_index


def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Transforms the input grid based on the observed pattern.

    The input is a single row containing a block of a non-white color followed by white pixels.
    The output grid has a height equal to half the width of the input row.
    The first row of the output is identical to the input row.
    Each subsequent row copies the row above it and extends the non-white block by one pixel to the right,
    replacing the adjacent white pixel, until the final row is generated.
    """
    # Convert input list of lists to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)

    # Input is expected to be 1 row
    if input_np.shape[0] != 1:
        raise ValueError("Input grid must have exactly one row.")

    input_row = input_np[0]
    width = len(input_row)

    # Determine the output height based on the pattern observed (M = N / 2)
    # Assuming width is always even based on examples
    height = width // 2

    # Find the color and index of the last non-white pixel in the input row
    non_white_color, last_non_white_idx = find_last_non_white_pixel(input_row.tolist())

    if last_non_white_idx == -1:
         # Handle case where input is all white (return input?) or doesn't match expected pattern
         # Based on examples, we assume a non-white block exists.
         # Let's return the input as is if no non-white color is found, although this contradicts examples.
         print("Warning: No non-white starting block found. Returning input as is.")
         return input_grid


    # Initialize the output grid with zeros
    output_np = np.zeros((height, width), dtype=int)

    # Set the first row of the output grid
    output_np[0, :] = input_row

    # Generate subsequent rows
    for r in range(1, height):
        # Copy the previous row
        output_np[r, :] = output_np[r - 1, :]

        # Calculate the index of the pixel to change in the current row
        # This is the position immediately after the end of the block in the *previous* row.
        # The block length in row `r-1` is `last_non_white_idx + 1 + (r - 1)`.
        # The index to change in row `r` is `last_non_white_idx + 1 + (r - 1) = last_non_white_idx + r`.
        idx_to_change = last_non_white_idx + r

        # Ensure the index is within the grid bounds
        if idx_to_change < width:
            # Change the pixel at the calculated index to the non-white color
            output_np[r, idx_to_change] = non_white_color

    # Convert the final numpy array back to a list of lists
    output_grid = output_np.tolist()

    return output_grid