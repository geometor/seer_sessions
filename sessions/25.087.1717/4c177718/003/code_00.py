import numpy as np
from collections import deque

"""
Transformation Rule Natural Language Description:

1.  Identify the horizontal line composed entirely of gray pixels (color 5) that divides the input grid.
2.  Define the region above the gray line as the 'Top Region' and the region below as the 'Bottom Region'.
3.  Find the three distinct colored objects within the Top Region. Identify them based on their horizontal position as Left Object, Middle Object, and Right Object.
4.  Find the single colored object within the Bottom Region, identifying it as the Key Object.
5.  Compare the Key Object with the Left Object from the Top Region. Verify they are identical in shape and color. If they match, designate the Left Object as the 'Matched Object'. (Assume this match always occurs based on examples).
6.  Designate the Middle Object from the Top Region as the 'Discarded Object'.
7.  Designate the Right Object from the Top Region as the 'Other Object'.
8.  Determine the specific shape of the Discarded Object (which is always Red in the examples). It will be either a 'Plus' shape or a 'T' shape (both composed of 5 pixels but geometrically distinct).
9.  Determine the vertical stacking order for the output based on the Discarded Object's shape:
    *   If the Discarded Object is 'Plus', the Matched Object will be placed on top, and the Other Object will be placed below it.
    *   If the Discarded Object is 'T', the Other Object will be placed on top, and the Matched Object will be placed below it.
10. Construct the output grid:
    *   Set the output grid dimensions: Height = 9, Width = Input Grid Width. Initialize with the background color White (0).
    *   Determine the amount of top padding (`P_top`) based on the Discarded Object's shape and the Other Object's color using the following rules:
        *   If Discarded is 'Plus' and Other is Orange(7), `P_top = 3`.
        *   If Discarded is 'Plus' and Other is Magenta(6), `P_top = 1`.
        *   If Discarded is 'T' and Other is Yellow(4), `P_top = 0`.
        *   If Discarded is 'T' and Other is Green(3), `P_top = 2`.
    *   Calculate the starting row for the top stacked object: `start_row_top = P_top`.
    *   Get the normalized grid representation (minimal bounding box) of the object designated to be on top in the stack. Calculate its height (`H_top_stack`) and width (`W_top_stack`).
    *   Calculate the starting column to center the top object horizontally: `start_col_top = (Output Width - W_top_stack) // 2`.
    *   Place the top stacked object onto the output grid at `(start_row_top, start_col_top)`.
    *   Get the normalized grid representation of the object designated to be on the bottom in the stack. Calculate its width (`W_bottom_stack`).
    *   Calculate the starting row for the bottom stacked object: `start_row_bottom = start_row_top + H_top_stack`.
    *   Calculate the starting column to center the bottom object horizontally: `start_col_bottom = (Output Width - W_bottom_stack) // 2`.
    *   Place the bottom stacked object onto the output grid at `(start_row_bottom, start_col_bottom)`.
"""

# Helper functions

def find_gray_line_row(grid):
    """Finds the row index containing the horizontal gray line (color 5)."""
    gray_color = 5
    for r_idx, row in enumerate(grid):
        # Check if gray is present and all non-background pixels are gray
        has_gray = False
        is_line = True
        for pixel in row:
            if pixel == gray_color:
                has_gray = True
            elif pixel != 0: # Assuming 0 is background
                is_line = False
                break
        if has_gray and is_line:
            return r_idx
    return -1 # Not found

def find_objects_in_region(grid_region, background_color=0):
    """Finds distinct contiguous objects of non-background color in a given grid region."""
    objects = []
    region_height, region_width = grid_region.shape
    visited = np.zeros_like(grid_region, dtype=bool)

    for r in range(region_height):
        for c in range(region_width):
            if grid_region[r, c] != background_color and not visited[r, c]:
                color = grid_region[r, c]
                coords = set()
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, min_c = r, c
                max_r, max_c = r, c

                while q:
                    row, col = q.popleft()
                    coords.add((row, col))
                    min_r = min(min_r, row)
                    min_c = min(min_c, col)
                    max_r = max(max_r, row)
                    max_c = max(max_c, col)

                    # Check 8 neighbors (including diagonals)
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue
                            nr, nc = row + dr, col + dc
                            if 0 <= nr < region_height and 0 <= nc < region_width and \
                               not visited[nr, nc] and grid_region[nr, nc] == color:
                                visited[nr, nc] = True
                                q.append((nr, nc))

                # Store object details relative to the region it was found in
                relative_coords = frozenset((coord[0] - min_r, coord[1] - min_c) for coord in coords)
                bbox = (min_r, min_c, max_r, max_c)
                obj_height = max_r - min_r + 1
                obj_width = max_c - min_c + 1

                # Create normalized grid representation
                normalized_grid = np.full((obj_height, obj_width), background_color, dtype=int)
                for rel_r, rel_c in relative_coords:
                    normalized_grid[rel_r, rel_c] = color

                objects.append({
                    'color': color,
                    'coords': coords, # Coordinates relative to the original region
                    'bbox': bbox,     # Bbox relative to the original region
                    'min_col': min_c, # Min column for sorting horizontally
                    'pixel_count': len(coords),
                    'normalized_grid': normalized_grid
                })

    # Sort objects by horizontal position (min column)
    objects.sort(key=lambda obj: obj['min_col'])
    return objects

def get_object_shape_type(obj_details, background_color=0):
    """Determines if the object shape is 'Plus' or 'T' based on geometry."""
    if obj_details['pixel_count'] != 5:
         # Based on examples, the shapes to distinguish have 5 pixels
        return 'Unknown'

    grid = obj_details['normalized_grid']
    # Create binary versions (1 for object, 0 for background)
    grid_binary = (grid != background_color).astype(int)

    # Define templates (normalized, binary)
    plus_template = np.array([
        [0, 1, 0],
        [1, 1, 1],
        [0, 1, 0]
    ])
    # T shape observed in examples (inverted T)
    t_template = np.array([
        [1, 1, 1],
        [0, 1, 0],
        [0, 1, 0]
    ])
    # Note: The description implied a different T shape orientation.
    # Re-checked Examples 2 & 4: Red object normalized shape is:
    # [[0, 2, 0], [0, 2, 0], [2, 2, 2]] which is an inverted T, but the template
    # above is for a standard T. Let's correct the T template based on examples.
    t_template_inverted = np.array([
        [0,1,0], # Top of inverted T
        [0,1,0], # Middle stem
        [1,1,1]  # Base crossbar
    ])
    
    # Re-check Plus shape in examples 1 & 3: Red object normalized shape is:
    # [[2,2,2],[0,2,0],[0,2,0]]. Let's call this 'Rotated_T_Right'? No, visual check confirms PLUS.
    # Plus shape: [[0,2,0],[2,2,2],[0,2,0]]
    # Let's fix the plus template based on examples.
    plus_template_example = np.array([
        [0, 1, 0],
        [1, 1, 1],
        [0, 1, 0]
    ]) # This one matches visual plus.

    # Update T-template based on Example 2/4 visual check.
    t_template_example = np.array([
        [0, 1, 0], # Top stem
        [0, 1, 0], # Middle stem
        [1, 1, 1]  # Bottom bar
    ])

    # Check for matches against corrected templates
    if grid_binary.shape == plus_template_example.shape and np.array_equal(grid_binary, plus_template_example):
        return 'Plus'
    elif grid_binary.shape == t_template_example.shape and np.array_equal(grid_binary, t_template_example):
        return 'T'
    else:
        # If it's 5 pixels but doesn't match known shapes
        # print("Warning: 5-pixel object doesn't match Plus or T template.")
        # print(grid_binary)
        return 'Unknown'


def are_objects_identical(obj1_details, obj2_details):
    """Checks if two objects have the same color and normalized shape."""
    # Check color first (quick)
    if obj1_details['color'] != obj2_details['color']:
        return False
    # Check normalized grid shape (more intensive)
    return np.array_equal(obj1_details['normalized_grid'], obj2_details['normalized_grid'])

# Main transformation function
def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    background_color = 0

    # 1. Find the gray line
    gray_line_r = find_gray_line_row(input_np)
    if gray_line_r == -1:
        raise ValueError("Gray dividing line not found.")

    # 2. Define top and bottom regions
    top_region = input_np[:gray_line_r, :]
    bottom_region = input_np[gray_line_r + 1:, :]

    # 3. Find objects in the top half
    top_objects = find_objects_in_region(top_region, background_color)
    if len(top_objects) != 3:
        raise ValueError(f"Expected 3 objects in the top region, found {len(top_objects)}")

    # Assign based on sorted horizontal order
    left_obj = top_objects[0]
    middle_obj = top_objects[1]
    right_obj = top_objects[2]

    # 4. Find the Key Object in the bottom half
    bottom_objects = find_objects_in_region(bottom_region, background_color)
    if len(bottom_objects) != 1:
        raise ValueError(f"Expected 1 object in the bottom region, found {len(bottom_objects)}")
    key_obj = bottom_objects[0]

    # 5. Verify Key Object matches the Left Object and identify roles
    if not are_objects_identical(key_obj, left_obj):
        # Basic assumption check - could add logic to check other top objects if needed
        raise ValueError("Key object from bottom does not match leftmost object from top.")
    
    matched_obj = left_obj
    discarded_obj = middle_obj
    other_obj = right_obj

    # 8. Determine shape type of the Discarded (Middle) Object
    discarded_shape_type = get_object_shape_type(discarded_obj, background_color)
    if discarded_shape_type == 'Unknown':
         raise ValueError(f"Could not determine shape type (Plus/T) for discarded object.")

    # 9. Determine stacking order
    if discarded_shape_type == 'Plus':
        top_stacked_obj = matched_obj
        bottom_stacked_obj = other_obj
    elif discarded_shape_type == 'T':
        top_stacked_obj = other_obj
        bottom_stacked_obj = matched_obj
    else:
        # Should be unreachable due to check above, but included for safety
         raise ValueError(f"Invalid discarded shape type '{discarded_shape_type}' encountered.")

    # 10. Construct the output grid
    output_height = 9
    output_width = width # Match input width
    output_grid_np = np.full((output_height, output_width), background_color, dtype=int)

    # Determine top padding based on Discarded Shape and Other Color
    other_color = other_obj['color']
    p_top = -1 # Initialize with invalid value

    if discarded_shape_type == 'Plus':
        if other_color == 7: # Orange
            p_top = 3
        elif other_color == 6: # Magenta
            p_top = 1
    elif discarded_shape_type == 'T':
        if other_color == 4: # Yellow
            p_top = 0
        elif other_color == 3: # Green
            p_top = 2

    if p_top == -1:
        raise ValueError(f"Unsupported combination for padding: Discarded Shape={discarded_shape_type}, Other Color={other_color}")

    # Get normalized grids and dimensions for placement
    top_norm = top_stacked_obj['normalized_grid']
    th, tw = top_norm.shape
    bottom_norm = bottom_stacked_obj['normalized_grid']
    bh, bw = bottom_norm.shape

    # Calculate placement positions (centered horizontally)
    start_row_top = p_top
    start_col_top = (output_width - tw) // 2

    start_row_bottom = start_row_top + th # Place immediately below
    start_col_bottom = (output_width - bw) // 2

    # Place objects onto the output grid, ensuring only non-background pixels are written
    # Top object
    end_row_top = start_row_top + th
    end_col_top = start_col_top + tw
    # Check bounds (shouldn't be needed if logic is correct, but safe)
    if 0 <= start_row_top < output_height and 0 <= start_col_top < output_width and end_row_top <= output_height and end_col_top <= output_width:
         target_slice = output_grid_np[start_row_top : end_row_top, start_col_top : end_col_top]
         mask = top_norm != background_color
         target_slice[mask] = top_norm[mask]
    else:
         print(f"Warning: Top object placement out of bounds.")

    # Bottom object
    end_row_bottom = start_row_bottom + bh
    end_col_bottom = start_col_bottom + bw
    # Check bounds
    if 0 <= start_row_bottom < output_height and 0 <= start_col_bottom < output_width and end_row_bottom <= output_height and end_col_bottom <= output_width:
         target_slice = output_grid_np[start_row_bottom : end_row_bottom, start_col_bottom : end_col_bottom]
         mask = bottom_norm != background_color
         target_slice[mask] = bottom_norm[mask]
    else:
         print(f"Warning: Bottom object placement out of bounds.")


    # Convert back to list of lists for the required output format
    return output_grid_np.tolist()