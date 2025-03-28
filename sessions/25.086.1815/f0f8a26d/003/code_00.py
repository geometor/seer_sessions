"""
Transforms the input grid based on the following rules:
1. Identify the background color (most frequent color in the grid).
2. Identify all foreground pixels (pixels not matching the background color). Assume only one foreground color exists.
3. Find all contiguous objects of the foreground color using 8-way connectivity.
4. For each object:
    a. Determine its bounding box.
    b. Calculate its width and height.
    c. Classify the object based on its dimensions:
        - Point: width=1 and height=1
        - Vertical Line (V-Line): width=1 and height > 1
        - Horizontal Line (H-Line): width > 1 and height=1
        - Other: width > 1 and height > 1 (Assume this case doesn't occur based on examples, or handle as error/ignore).
    d. Calculate the center coordinates (cr, cc) and length (L) of the object.
        - For V-Line: cr = (min_row + max_row) // 2, cc = column, L = height
        - For H-Line: cr = row, cc = (min_col + max_col) // 2, L = width
        - For Point: cr = row, cc = col, L = 1
5. Create an output grid initialized with the background color.
6. Draw the transformed shape onto the output grid for each input object:
    - Point: Draw a point at the same location (cr, cc).
    - V-Line: Draw an H-Line in the output grid. The H-Line has row = cr, length = L, and is centered horizontally at column = cc.
    - H-Line: Draw a V-Line in the output grid. The V-Line has column = cc, length = L, and is centered vertically at row = cr.
7. Ensure drawing stays within the grid boundaries.
"""

import numpy as np
from collections import Counter
from scipy.ndimage import label

def find_background_color(grid):
    """Finds the most frequent color in the grid."""
    counts = Counter(grid.flatten())
    if not counts:
        return 0 # Default white
    # Handle ties by picking the smaller color index? Or assume one clear background.
    return counts.most_common(1)[0][0]

def find_foreground_color(grid, background_color):
    """Finds the first color that is not the background color."""
    for row in grid:
        for cell in row:
            if cell != background_color:
                return cell
    return None # No foreground color found

def transform(input_grid):
    """
    Applies the object-based H<->V line swap transformation.
    """
    input_grid_np = np.array(input_grid, dtype=int)
    height, width = input_grid_np.shape

    # 1. Identify background color
    background_color = find_background_color(input_grid_np)
    
    # Find foreground color (assuming one)
    foreground_color = find_foreground_color(input_grid_np, background_color)
    if foreground_color is None:
        # If no foreground color, return the input grid or background-filled grid
        return input_grid 

    # 2. Initialize output grid with background color
    output_grid = np.full((height, width), background_color, dtype=int)

    # 3. Find foreground objects
    foreground_mask = input_grid_np == foreground_color
    # Use 8-way connectivity (structure=np.ones((3,3)))
    labeled_array, num_features = label(foreground_mask, structure=np.ones((3,3), dtype=bool))

    # 4. Process each object
    for i in range(1, num_features + 1):
        # Find pixels belonging to this object
        object_pixels = np.argwhere(labeled_array == i)
        if object_pixels.size == 0:
            continue
        
        # a. Determine bounding box
        min_row = np.min(object_pixels[:, 0])
        max_row = np.max(object_pixels[:, 0])
        min_col = np.min(object_pixels[:, 1])
        max_col = np.max(object_pixels[:, 1])

        # b. Calculate width and height
        obj_height = max_row - min_row + 1
        obj_width = max_col - min_col + 1

        # c/d. Classify object and calculate center/length
        is_point = (obj_width == 1 and obj_height == 1)
        is_vline = (obj_width == 1 and obj_height > 1)
        is_hline = (obj_width > 1 and obj_height == 1)
        
        center_row = -1
        center_col = -1
        length = -1
        
        if is_point:
            center_row = min_row
            center_col = min_col
            length = 1
        elif is_vline:
            center_row = (min_row + max_row) // 2
            center_col = min_col # or max_col, they are the same
            length = obj_height
        elif is_hline:
            center_row = min_row # or max_row, they are the same
            center_col = (min_col + max_col) // 2
            length = obj_width
        else:
            # Handle 'Other' case if necessary - for now, ignore
            # print(f"Warning: Found non-line/point object {i} - ignoring.")
            continue
            
        # 6. Draw transformed shape onto output grid
        if is_point:
            # Draw point directly
            if 0 <= center_row < height and 0 <= center_col < width:
                output_grid[center_row, center_col] = foreground_color
        
        elif is_vline:
            # Input V-Line -> Output H-Line
            # Output line is at row = center_row
            # Output line has length = length
            # Output line is centered at col = center_col
            out_row = center_row
            start_col = center_col - (length - 1) // 2
            end_col = center_col + length // 2
            
            # Draw the horizontal line within bounds
            for c in range(start_col, end_col + 1):
                if 0 <= out_row < height and 0 <= c < width:
                    output_grid[out_row, c] = foreground_color
                    
        elif is_hline:
            # Input H-Line -> Output V-Line
            # Output line is at col = center_col
            # Output line has length = length
            # Output line is centered at row = center_row
            out_col = center_col
            start_row = center_row - (length - 1) // 2
            end_row = center_row + length // 2
            
            # Draw the vertical line within bounds
            for r in range(start_row, end_row + 1):
                 if 0 <= r < height and 0 <= out_col < width:
                    output_grid[r, out_col] = foreground_color

    # Convert back to list of lists for consistency if needed
    return output_grid.tolist()