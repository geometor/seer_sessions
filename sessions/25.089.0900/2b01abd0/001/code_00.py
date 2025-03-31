import numpy as np

"""
The transformation reflects non-white (0) and non-blue (1) pixels across a
horizontal blue line (color 1) while swapping specific pairs of colors.

1. Find the row index of the horizontal blue line.
2. Initialize an output grid of the same dimensions as the input, filled with white (0).
3. Copy the blue line from the input to the output grid.
4. Define the color swap pairs: Azure(8) <-> Yellow(4), Red(2) <-> Green(3), Gray(5) <-> Magenta(6).
5. Iterate through each pixel of the input grid.
6. If a pixel is neither white (0) nor blue (1):
   a. Calculate its vertical distance from the blue line.
   b. Determine the reflected row index by mirroring the distance across the blue line.
   c. Determine the swapped color based on the original color using the defined pairs.
   d. Place the swapped color at the reflected position (same column, reflected row) in the output grid.
7. Return the output grid.
"""

# Define the color swapping pairs
COLOR_SWAP_MAP = {
    8: 4,  # Azure -> Yellow
    4: 8,  # Yellow -> Azure
    2: 3,  # Red -> Green
    3: 2,  # Green -> Red
    5: 6,  # Gray -> Magenta
    6: 5,  # Magenta -> Gray
    # Add other colors here if needed, mapping them to themselves if they don't swap
    0: 0,  # White maps to White (background)
    1: 1,  # Blue maps to Blue (reflection line)
    7: 7,  # Orange maps to Orange (example not seen, but logical)
    9: 9   # Maroon maps to Maroon (example not seen, but logical)
}

def find_blue_line_row(grid):
    """Finds the row index of the first horizontal line of blue pixels (1)."""
    for r in range(grid.shape[0]):
        if np.all(grid[r, :] == 1):
            return r
        # Check if at least one blue pixel exists in the row (might be sufficient for some ARC tasks)
        # More robust check might be needed depending on variations,
        # but examples show full blue lines.
        if 1 in grid[r,:]:
             # Check if the entire row is either blue (1) or white (0)
             # This handles cases where the line doesn't span the whole grid width
             is_line = True
             for c in range(grid.shape[1]):
                 if grid[r, c] != 1 and grid[r,c] != 0:
                    is_line = False
                    break
             if is_line and np.any(grid[r,:] == 1): # Ensure there's at least one blue pixel
                 return r


    # Check columns if no horizontal line found (less likely based on description)
    # for c in range(grid.shape[1]):
    #     if np.all(grid[:, c] == 1):
    #         # Handle vertical line case if necessary
    #         pass # Not needed for this specific task description

    return -1 # Indicate not found

def transform(input_grid):
    """
    Applies the reflection and color swap transformation based on a horizontal blue line.
    """
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape

    # Initialize output grid with background color (white, 0)
    output_np = np.zeros_like(input_np)

    # Find the row index of the blue line
    blue_line_row = find_blue_line_row(input_np)

    if blue_line_row == -1:
        # Handle error: Blue line not found. Maybe return input or raise error.
        # For ARC, often returning the input or an empty grid might be expected.
        # Based on examples, assume it's always present.
        print("Error: Blue line not found!")
        return input_grid # Or handle differently

    # Copy the blue line itself to the output grid
    # We only copy the blue pixels, preserving the white background where the input might have 0s on the line row
    for c in range(width):
        if input_np[blue_line_row, c] == 1:
             output_np[blue_line_row, c] = 1


    # Iterate through each pixel of the input grid
    for r in range(height):
        for c in range(width):
            original_color = input_np[r, c]

            # Skip background (white) and the blue line itself
            if original_color == 0 or r == blue_line_row:
                continue

            # Calculate distance from the blue line
            # Positive distance means below the line, negative means above
            dist = r - blue_line_row

            # Calculate the reflected row index
            reflected_r = blue_line_row - dist

            # Check if the reflected row is within grid bounds
            if 0 <= reflected_r < height:
                # Get the swapped color
                swapped_color = COLOR_SWAP_MAP.get(original_color, original_color) # Default to original if not in map

                # Place the swapped color at the reflected position in the output grid
                # Important: Only place if the target cell is currently background (0)
                # or if this is the intended behavior based on potential overlaps.
                # The examples suggest overwriting is fine.
                output_np[reflected_r, c] = swapped_color

    # Convert back to list of lists if required by the ARC environment
    return output_np.tolist()