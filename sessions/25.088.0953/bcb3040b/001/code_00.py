import numpy as np
import math

# COLOR MAPPING (for reference, not used directly in logic)
# 0: white
# 1: blue
# 2: red
# 3: green
# ...

def find_pixels(grid, color):
    """
    Finds all coordinates (row, col) of pixels with a specific color in the grid.

    Args:
        grid (np.array): The input grid.
        color (int): The color value to search for.

    Returns:
        list: A list of tuples, where each tuple is the (row, col) coordinate.
    """
    points = []
    # Iterate through each cell of the grid
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            # If the cell color matches the target color, add its coordinates
            if grid[r, c] == color:
                points.append((r, c))
    return points

def get_line_pixels(p1, p2):
    """
    Generates integer coordinates for pixels on the straight line segment
    connecting p1 and p2 (inclusive).
    Handles horizontal, vertical, and diagonal lines (slope +/- 1).
    Assumes the line will be one of these three types based on ARC task nature.

    Args:
        p1 (tuple): The (row, col) coordinates of the first endpoint.
        p2 (tuple): The (row, col) coordinates of the second endpoint.

    Returns:
        list: A list of (row, col) tuples representing pixels on the line segment.
    """
    r1, c1 = p1
    r2, c2 = p2
    points = []

    # Determine the type of line and generate points accordingly
    if r1 == r2:  # Horizontal line
        # Iterate through columns from the minimum to maximum column index
        for c in range(min(c1, c2), max(c1, c2) + 1):
            points.append((r1, c))
    elif c1 == c2:  # Vertical line
        # Iterate through rows from the minimum to maximum row index
        for r in range(min(r1, r2), max(r1, r2) + 1):
            points.append((r, c1))
    elif abs(r1 - r2) == abs(c1 - c2):  # Diagonal line (slope is +/- 1)
        # Determine the step direction for row and column
        dr = np.sign(r2 - r1)
        dc = np.sign(c2 - c1)
        r, c = r1, c1
        # Step along the diagonal until the second endpoint is reached
        while True:
            points.append((r, c))
            if (r, c) == (r2, c2):
                break
            r += dr
            c += dc
    # else: # Optional: Handle cases where the line is not H, V, or D - assumed not to occur in this ARC task

    return points

def transform(input_grid):
    """
    Transforms the input grid based on the following rule:
    1. Find the two red (2) pixels in the input grid. These act as endpoints.
    2. Identify the straight line segment (horizontal, vertical, or diagonal with slope +/- 1) 
       connecting these two red pixels.
    3. Create a copy of the input grid for the output.
    4. Iterate through all pixels lying on the identified line segment (including endpoints).
    5. For each pixel on the line:
       - If the pixel's original color in the input grid is white (0), change its color 
         to red (2) in the output grid.
       - If the pixel's original color in the input grid is blue (1), change its color 
         to green (3) in the output grid.
       - If the pixel's color is anything else (including the original red endpoints), 
         keep its original color in the output grid.
    6. Return the modified grid.
    """
    # Convert input list of lists to numpy array for efficient processing
    input_np = np.array(input_grid, dtype=int)
    # Create a copy of the input grid to modify, ensuring the original is unchanged
    output_np = np.copy(input_np)

    # Define color constants for clarity
    RED = 2
    WHITE = 0
    BLUE = 1
    GREEN = 3

    # Step 1: Find the coordinates of the two red pixels
    red_pixels = find_pixels(input_np, RED)

    # Assumption based on training examples: there are exactly two red pixels.
    # If not, the behavior might be undefined or return the unchanged grid.
    if len(red_pixels) != 2:
        # In a robust implementation, might raise error or log warning.
        # For ARC, often assume test cases follow the observed pattern.
        return input_grid # Return original if assumption fails

    p1, p2 = red_pixels[0], red_pixels[1]

    # Step 2: Get all pixel coordinates on the line segment between the red pixels
    line_pixels = get_line_pixels(p1, p2)

    # Step 4 & 5: Iterate through the pixels on the line and apply transformations
    for r, c in line_pixels:
        # Get the original color of the pixel at (r, c) from the input grid
        original_color = input_np[r, c]
        
        # Apply the transformation rules based on the original color
        if original_color == WHITE:
            output_np[r, c] = RED  # Change white to red
        elif original_color == BLUE:
            output_np[r, c] = GREEN # Change blue to green
        # No action needed for other colors; they remain the same in the copied output grid.

    # Step 6: Convert the final numpy array back to a list of lists for ARC standard output
    return output_np.tolist()