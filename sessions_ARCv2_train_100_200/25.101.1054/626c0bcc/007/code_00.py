import numpy as np

"""
Transforms an input grid containing white (0) and azure (8) pixels into an 
output grid of the same dimensions. White pixels remain unchanged. Azure pixels 
are recolored to blue (1), red (2), green (3), or yellow (4) based on a 
fixed mapping determined by the 2x2 neighborhood pattern starting at the 
azure pixel's location (r, c).

The 2x2 pattern includes the pixel at (r, c) as the top-left, and considers 
pixels at (r, c+1), (r+1, c), and (r+1, c+1). Pixels outside the grid 
boundaries are treated as white (0) when forming the pattern.

The specific mapping rules are:
- (8, 0, 0, 0) -> 1 (blue)
- (8, 8, 0, 0) -> 1 (blue)
- (8, 0, 8, 0) -> 2 (red)
- (8, 0, 0, 8) -> 1 (blue)
- (8, 8, 8, 0) -> 3 (green)
- (8, 8, 0, 8) -> 2 (red)
- (8, 0, 8, 8) -> 4 (yellow)
- (8, 8, 8, 8) -> 1 (blue)
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:  
    """
    Applies a 2x2 neighborhood pattern-based color transformation to azure pixels.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    # Convert input list of lists to a NumPy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    height, width = input_array.shape

    # Pad the input array with 0s (white) on the right and bottom edges by 1 cell.
    # This simplifies extracting 2x2 neighborhoods at the grid boundaries.
    padded_input = np.pad(input_array, ((0, 1), (0, 1)), mode='constant', constant_values=0)

    # Initialize the output grid with the same dimensions as the input, filled with 0s (white)
    output_array = np.zeros_like(input_array)

    # Define the mapping from 2x2 patterns (flattened tuple) to output colors.
    # This map was derived by analyzing all training examples and selecting the 
    # most frequent output color for each observed pattern.
    # The pattern tuple represents (top-left, top-right, bottom-left, bottom-right)
    pattern_map = {
        (8, 0, 0, 0): 1,  # blue
        (8, 8, 0, 0): 1,  # blue
        (8, 0, 8, 0): 2,  # red
        (8, 0, 0, 8): 1,  # blue
        (8, 8, 8, 0): 3,  # green
        (8, 8, 0, 8): 2,  # red
        (8, 0, 8, 8): 4,  # yellow
        (8, 8, 8, 8): 1,  # blue
    }

    # Iterate through each pixel of the original input grid
    for r in range(height):
        for c in range(width):
            # Check if the current pixel in the original input is azure (8)
            if input_array[r, c] == 8:
                # Extract the 2x2 neighborhood from the padded input array.
                # The top-left of the neighborhood in the padded array corresponds 
                # to the current pixel (r, c) in the original grid.
                neighborhood = padded_input[r:r+2, c:c+2]

                # Flatten the 2x2 neighborhood into a tuple to use as a key for the map.
                # Ensure elements are standard Python integers for dictionary lookup.
                pattern = tuple(int(x) for x in neighborhood.flatten())

                # Look up the corresponding output color from the pattern map.
                # Default to 0 (white) if the pattern is somehow not found (should not happen if input[r,c] is 8).
                output_color = pattern_map.get(pattern, 0) 

                # Assign the determined color to the output grid at the same position (r, c).
                output_array[r, c] = output_color
            else:
                # If the input pixel is not azure (i.e., it's white 0), 
                # keep it white in the output. The output is already initialized to 0.
                # Explicit assignment for clarity: output_array[r, c] = input_array[r, c]
                pass # output is already 0

    # Convert the output NumPy array back to a list of lists for the required return format
    output_grid = output_array.tolist()

    return output_grid