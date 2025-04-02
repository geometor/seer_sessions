import numpy as np

"""
Transformation Rule:
Initialize the output grid as a copy of the input grid.
The input grid is divided into four quadrants by a central vertical blue line (column 13) and a central horizontal blue line (row 13).
Objects (pixels not matching the background yellow color 4) in each quadrant are reflected into another quadrant according to specific rules:
1. Top-Left (TL) objects are reflected horizontally across the vertical line into the Top-Right (TR) quadrant.
2. Top-Right (TR) objects are reflected vertically across the horizontal line into the Bottom-Right (BR) quadrant.
3. Bottom-Left (BL) objects are reflected horizontally across the vertical line into the Bottom-Right (BR) quadrant.
4. Bottom-Right (BR) objects are reflected vertically across the horizontal line into the Top-Right (TR) quadrant.
These reflections are additive; the original objects remain, and the reflected pixels are added to the output grid. The separator lines and background remain unchanged.
"""

def transform(input_grid):
    """
    Applies reflection rules across quadrant separators to the input grid.
    """
    # Convert input list of lists to a numpy array for easier slicing and indexing
    input_np = np.array(input_grid, dtype=int)
    
    # Initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_np)
    
    # Get grid dimensions
    height, width = input_np.shape
    
    # Define separator lines (assuming they are always central for this task based on examples)
    # Note: ARC grid indices are 0-based.
    # If grid dims are odd, the center row/col index is floor(dim / 2)
    # Examples are 27x27, so center row/col is 13.
    separator_row = height // 2
    separator_col = width // 2
    
    # Define the background color to ignore during reflection
    background_color = 4

    # Iterate through each pixel of the input grid
    for r in range(height):
        for c in range(width):
            pixel_color = input_np[r, c]

            # Skip background color and separator lines
            if pixel_color == background_color or r == separator_row or c == separator_col:
                continue

            # Determine the quadrant and apply the corresponding reflection rule
            
            # Top-Left Quadrant (TL) -> Reflect Horizontally to Top-Right (TR)
            if r < separator_row and c < separator_col:
                reflected_c = separator_col + (separator_col - c)
                # Check bounds just in case, though reflection logic should keep it within grid for symmetric separators
                if 0 <= r < height and 0 <= reflected_c < width:
                     output_grid[r, reflected_c] = pixel_color

            # Top-Right Quadrant (TR) -> Reflect Vertically to Bottom-Right (BR)
            elif r < separator_row and c > separator_col:
                reflected_r = separator_row + (separator_row - r)
                if 0 <= reflected_r < height and 0 <= c < width:
                    output_grid[reflected_r, c] = pixel_color

            # Bottom-Left Quadrant (BL) -> Reflect Horizontally to Bottom-Right (BR)
            elif r > separator_row and c < separator_col:
                reflected_c = separator_col + (separator_col - c)
                if 0 <= r < height and 0 <= reflected_c < width:
                     output_grid[r, reflected_c] = pixel_color

            # Bottom-Right Quadrant (BR) -> Reflect Vertically to Top-Right (TR)
            elif r > separator_row and c > separator_col:
                reflected_r = separator_row + (separator_row - r)
                if 0 <= reflected_r < height and 0 <= c < width:
                    output_grid[reflected_r, c] = pixel_color

    # Convert the numpy array back to a list of lists for the final output format
    return output_grid.tolist()