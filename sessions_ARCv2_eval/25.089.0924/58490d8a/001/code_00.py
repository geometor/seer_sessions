import numpy as np
import sys

# Increase recursion depth for potentially deep searches in helper functions, although not strictly needed for this specific solution.
# sys.setrecursionlimit(2000) 

"""
Identify the unique, contiguous rectangular region within the input grid that consists entirely of white (0) pixels. Determine its top-left corner coordinates, height, and width. Create a new output grid with the same height and width as the identified white rectangle, initialized to white (0). Iterate through each pixel within the bounds of the white rectangle in the input grid. For each pixel examined, if its color is not white (0), copy its color to the corresponding relative position in the output grid. The relative position is calculated by subtracting the top-left corner coordinates of the white rectangle from the pixel's absolute coordinates in the input grid. The final output grid contains the non-white content of the input's white rectangle, preserving relative positions, on a white background.
"""

def find_largest_white_rectangle(grid):
    """
    Finds the largest rectangular area composed entirely of white (0) pixels.

    Args:
        grid (np.array): The input grid.

    Returns:
        tuple: (min_row, max_row, min_col, max_col) coordinates of the largest 
               white rectangle, or None if no white pixel is found. Returns coordinates inclusive.
    """
    rows, cols = grid.shape
    if rows == 0 or cols == 0:
        return None

    # Precompute heights of consecutive white cells ending at (r, c) looking upwards.
    heights = np.zeros((rows, cols), dtype=int)
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == 0:
                heights[r, c] = heights[r - 1, c] + 1 if r > 0 else 1
            else:
                heights[r, c] = 0

    max_area = 0
    best_rect = None # (min_row, max_row, min_col, max_col)

    # For each row, treat it as the bottom row of potential rectangles
    # and compute the largest rectangle using the histogram approach.
    for r in range(rows):
        stack = [] # Stores indices of columns (potential left boundaries)
        for c in range(cols + 1): # Iterate through columns + one extra to flush stack
            h = heights[r, c] if c < cols else 0 # Current height
            
            while stack and heights[r, stack[-1]] >= h:
                height = heights[r, stack.pop()]
                width = c if not stack else c - stack[-1] - 1
                area = height * width
                
                if area > max_area:
                    max_area = area
                    min_c = stack[-1] + 1 if stack else 0
                    max_c = c - 1
                    min_r = r - height + 1
                    max_r = r
                    best_rect = (min_r, max_r, min_c, max_c)
                    
            stack.append(c)

    return best_rect


def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input grid by extracting the non-white content from the largest 
    all-white rectangular area.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the output grid.
    """
    
    # Find the largest rectangle composed entirely of white pixels (0)
    rect_coords = find_largest_white_rectangle(input_grid)

    if rect_coords is None:
        # Handle edge case where no white rectangle is found (though examples suggest one exists)
        # Returning an empty grid might be appropriate, or based on problem constraints.
        # Let's assume based on examples, a rectangle will always be found.
        # If this assumption is wrong, error handling or returning input_grid might be needed.
         print("Warning: No white rectangle found.") 
         # Return 1x1 white grid as a fallback
         return np.zeros((1, 1), dtype=int)


    min_row, max_row, min_col, max_col = rect_coords
    
    # Calculate the dimensions of the rectangle
    rect_height = max_row - min_row + 1
    rect_width = max_col - min_col + 1

    # Initialize the output grid with the dimensions of the rectangle, filled with white (0)
    output_grid = np.zeros((rect_height, rect_width), dtype=int)

    # Iterate through the found rectangle in the input grid
    for r in range(rect_height):
        for c in range(rect_width):
            # Get the corresponding coordinates in the input grid
            input_r = min_row + r
            input_c = min_col + c
            
            # Get the pixel value from the input grid within the rectangle
            pixel_value = input_grid[input_r, input_c]
            
            # If the pixel is not white (0), copy it to the output grid
            # Note: The problem statement focuses on copying NON-white pixels from the 
            # WHITE rectangle area. So, even if the rectangle definition found includes 
            # non-white pixels (which it shouldn't by definition of find_largest_white_rectangle),
            # we only copy non-white ones.
            if pixel_value != 0:
                output_grid[r, c] = pixel_value
                
    return output_grid