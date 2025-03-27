```python
import numpy as np

def _find_unique_pixel(grid_np, background_color=8):
    """
    Finds the color and coordinates (row, column) of the unique pixel 
    in the grid that does not match the background color.

    Args:
        grid_np (np.ndarray): The input grid as a NumPy array.
        background_color (int): The color value considered as background.

    Returns:
        tuple: (color, row, column) of the unique pixel. 
               Returns (None, -1, -1) if no unique non-background pixel is found 
               or if more than one is found.
    """
    coords = np.where(grid_np != background_color)
    num_unique = len(coords[0])

    if num_unique == 1:
        r, c = coords[0][0], coords[1][0]
        color = grid_np[r, c]
        return color, r, c
    elif num_unique > 1:
        # According to the task description, there should only be one unique pixel.
        # Handle this case defensively, though it might indicate a misunderstanding
        # or unexpected input. Returning the first one found.
        # print(f"Warning: Found {num_unique} non-background pixels. Using the first one.")
        r, c = coords[0][0], coords[1][0]
        color = grid_np[r, c]
        return color, r, c
    else:
        # No non-background pixel found
        return None, -1, -1

def transform(input_grid):
    """
    Transforms the input grid based on the position of a single unique pixel.
    Finds the unique non-background pixel in the input grid. Calculates the areas
    of the four quadrants defined by this pixel's location (relative to the pixel itself).
    Identifies the quadrant with the smallest area. Creates an output grid of the 
    same size filled with the background color (azure/8), and draws a solid rectangle 
    in the corner corresponding to the smallest quadrant, using the unique pixel's color 
    and the quadrant's dimensions. In case of ties in area, the priority for choosing 
    the corner is Top-Left > Top-Right > Bottom-Left > Bottom-Right.
    """
    # Convert input list of lists to a NumPy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    H, W = input_np.shape  # Grid Height and Width
    background_color = 8   # Azure color is the background

    # Step 1: Find the unique pixel's color and location (R, C)
    source_color, R, C = _find_unique_pixel(input_np, background_color)

    # If no unique pixel found, return a grid filled with background color
    if source_color is None:
        return np.full((H, W), background_color, dtype=int).tolist()

    # Step 2: Initialize the output grid with the background color
    output_np = np.full((H, W), background_color, dtype=int)

    # Step 3: Calculate dimensions and areas of the four quadrants
    # Quadrant dimensions are inclusive of the pixel's row/column
    h_tl, w_tl = R + 1, C + 1  # Top-Left height, width
    area_tl = h_tl * w_tl      # Top-Left area

    h_tr, w_tr = R + 1, W - C  # Top-Right height, width
    area_tr = h_tr * w_tr      # Top-Right area

    h_bl, w_bl = H - R, C + 1  # Bottom-Left height, width
    area_bl = h_bl * w_bl      # Bottom-Left area

    h_br, w_br = H - R, W - C  # Bottom-Right height, width
    area_br = h_br * w_br      # Bottom-Right area

    # Step 4: Store quadrant info with priority (TL > TR > BL > BR)
    # This order ensures correct selection during tie-breaking
    quadrants = [
        {'label': 'TL', 'area': area_tl, 'h': h_tl, 'w': w_tl},
        {'label': 'TR', 'area': area_tr, 'h': h_tr, 'w': w_tr},
        {'label': 'BL', 'area': area_bl, 'h': h_bl, 'w': w_bl},
        {'label': 'BR', 'area': area_br, 'h': h_br, 'w': w_br},
    ]

    # Step 5: Find the minimum area among the quadrants
    min_area_value = min(q['area'] for q in quadrants)
    
    # Step 6: Select the quadrant corresponding to the minimum area, respecting priority
    chosen_quadrant = None
    for quad in quadrants:
        if quad['area'] == min_area_value:
            chosen_quadrant = quad
            break  # Stop at the first match (highest priority due to list order)

    # Should always find a quadrant if input was valid
    if chosen_quadrant is None:
        # Fallback: return background grid if something went wrong
        return output_np.tolist() 

    target_h = chosen_quadrant['h']
    target_w = chosen_quadrant['w']
    corner_label = chosen_quadrant['label']

    # Step 7: Fill the determined corner region in the output grid
    # Check for positive dimensions before slicing to avoid errors/empty operations
    if target_h > 0 and target_w > 0:
        if corner_label == 'TL':
            # Fill top-left corner: rows 0 to target_h, columns 0 to target_w
            output_np[0:target_h, 0:target_w] = source_color
        elif corner_label == 'TR':
            # Fill top-right corner: rows 0 to target_h, columns W-target_w to W
            output_np[0:target_h, W-target_w:W] = source_color
        elif corner_label == 'BL':
            # Fill bottom-left corner: rows H-target_h to H, columns 0 to target_w
            output_np[H-target_h:H, 0:target_w] = source_color
        elif corner_label == 'BR':
            # Fill bottom-right corner: rows H-target_h to H, columns W-target_w to W
            output_np[H-target_h:H, W-target_w:W] = source_color

    # Convert the output NumPy array back to a list of lists before returning
    output_grid = output_np.tolist()

    return output_grid
```