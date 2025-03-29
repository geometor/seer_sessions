```python
import numpy as np

"""
Transformation Rule Description:

1.  **Identify the Background Template:** Find the largest contiguous rectangular block in the input grid composed of a single, non-white (non-zero) color. This block determines the output grid's dimensions and background color.
2.  **Create the Output Canvas:** Initialize a new grid with the dimensions derived from the background template rectangle, filling it entirely with the template's color.
3.  **Identify the Foreground Pattern:** Locate all pixels in the *input* grid that have the color Azure (8).
4.  **Overlay the Pattern:** For each Azure (8) pixel found in the input grid at coordinates (row, column), place an Azure (8) pixel at the *same* coordinates (row, column) in the output canvas, provided these coordinates fall within the bounds of the output canvas.
"""

def find_largest_solid_rectangle(grid):
    """
    Finds the largest solid rectangle of a single non-white color in the grid.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        tuple: (color, (height, width)) of the largest rectangle, or (-1, (0, 0)) if none found.
    """
    rows, cols = grid.shape
    max_area = 0
    best_color = -1
    best_dims = (0, 0)
    
    # Iterate through all possible top-left corners
    for r1 in range(rows):
        for c1 in range(cols):
            color = grid[r1, c1]
            # Skip white background pixels
            if color == 0:
                continue

            # Check rectangles expanding from this corner
            max_possible_c2 = cols
            for r2 in range(r1, rows):
                 # Check if the starting color continues in this row
                 if grid[r2, c1] != color:
                     break # Cannot expand downwards anymore with this color
                 
                 for c2 in range(c1, max_possible_c2):
                     # Check if the pixel maintains the color
                     if grid[r2, c2] != color:
                         # If the color breaks, this column is the max for subsequent rows starting from r1,c1
                         max_possible_c2 = c2 
                         break 
                         
                     # Check if the rectangle formed so far is solid
                     is_solid = True
                     # Optimization: only need to check the new row/column being added if prior checks passed
                     # Check the new column from r1 to r2
                     for i in range(r1, r2 + 1):
                          if grid[i, c2] != color:
                              is_solid = False
                              break
                     if not is_solid:
                          max_possible_c2 = c2 # Cannot expand further right with this color at this height
                          break
                     # Check the new row from c1 to c2 (already partially checked above)
                     # This check might be redundant given the outer loops structure, but safer?
                     # Re-evaluating logic - the inner loops ensure solidity as they expand.

                     # Calculate area if solid
                     height = r2 - r1 + 1
                     width = c2 - c1 + 1
                     area = height * width

                     if area > max_area:
                         max_area = area
                         best_color = color
                         best_dims = (height, width)
                 # Need to handle the case where the inner loop completed without break
                 # This means we reached max_possible_c2 = cols


    # --- Alternative, potentially simpler approach ---
    # Find unique non-white colors
    unique_colors = np.unique(grid[grid != 0])
    max_area_alt = 0
    best_color_alt = -1
    best_dims_alt = (0, 0)
    
    for color in unique_colors:
        # Create a mask for the current color
        mask = (grid == color)
        
        # Find largest rectangle in the boolean mask (standard algorithm)
        # Using a histogram-based approach for finding the largest rectangle in a binary matrix
        heights = np.zeros(cols, dtype=int)
        for r in range(rows):
            for c in range(cols):
                heights[c] = heights[c] + 1 if mask[r, c] else 0
            
            # Calculate largest rectangle ending at this row using histogram method
            stack = [-1]
            for c, h in enumerate(heights):
                while stack[-1] != -1 and heights[stack[-1]] >= h:
                    height = heights[stack.pop()]
                    width = c - stack[-1] - 1
                    area = height * width
                    if area > max_area_alt:
                        max_area_alt = area
                        best_color_alt = color
                        # Dimensions are trickier here, need to store them with the area
                        # This standard algorithm gives area, not explicit dims easily.
                        # Let's stick to the first method which finds dimensions directly.
                        
            while stack[-1] != -1:
                height = heights[stack.pop()]
                width = cols - stack[-1] - 1
                area = height * width
                if area > max_area_alt:
                    max_area_alt = area
                    best_color_alt = color
                    # Again, dims are hard to track directly this way.

    # Reverting to the first, more direct (though potentially slower) approach
    # Need to ensure the first approach correctly identifies the largest rectangle
    # Let's refine the first approach slightly for clarity/correctness.

    max_area_final = 0
    best_color_final = -1
    best_dims_final = (0, 0)

    for r1 in range(rows):
        for c1 in range(cols):
            color = grid[r1, c1]
            if color == 0:
                continue
            
            # Max width possible for rows starting from r1
            max_w = cols - c1 
            for r2 in range(r1, rows):
                # Check if the first column pixel still matches
                if grid[r2, c1] != color:
                    break # Cannot extend height further

                # Check pixels in the current row r2 from c1 onwards
                for c2 in range(c1, c1 + max_w):
                    if grid[r2, c2] != color:
                         max_w = c2 - c1 # Update max width possible for subsequent rows
                         break
                
                # Now we know the rectangle is solid up to height (r2-r1+1) and width max_w
                current_h = r2 - r1 + 1
                current_w = max_w 
                area = current_h * current_w
                
                if area > max_area_final:
                    max_area_final = area
                    best_color_final = color
                    best_dims_final = (current_h, current_w)

                if max_w == 0: # Optimization: if width became 0, no point checking further rows
                     break

    return best_color_final, best_dims_final


def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    grid_np = np.array(input_grid, dtype=int)
    rows, cols = grid_np.shape

    # 1. Identify the Background Template
    bg_color, (output_height, output_width) = find_largest_solid_rectangle(grid_np)

    if bg_color == -1 or output_height == 0 or output_width == 0:
        # Handle cases where no suitable background is found (e.g., all white input)
        # Based on examples, this shouldn't happen, but good practice.
        # Return empty or based on specific error handling if needed.
        # For now, let's assume a valid background is always found.
        # If the task demands a specific output for failure, adjust here.
        # Perhaps return the input grid or an empty grid? Let's assume valid input.
         print("Warning: Could not find a valid background rectangle.")
         # Fallback to input dimensions and white background? Or fail?
         # Based on ARC, valid inputs usually exist. Let's proceed assuming success.
         # If needed, could return np.array([[]]).tolist()
         pass # Continue assuming bg_color, output_height, output_width are valid


    # 2. Create the Output Canvas
    output_grid = np.full((output_height, output_width), bg_color, dtype=int)

    # 3. Identify the Foreground Pattern (Azure pixels)
    azure_pixels = np.argwhere(grid_np == 8) # Returns list of [row, col]

    # 4. Overlay the Pattern
    for r, c in azure_pixels:
        # Check if the coordinate is within the bounds of the output grid
        if r < output_height and c < output_width:
            output_grid[r, c] = 8 # Set pixel to Azure

    # Convert the final NumPy array back to a list of lists
    return output_grid.tolist()

```