
Previous Code:
```python
import numpy as np
from collections import Counter

"""
Transforms the input grid based on color mapping rules derived from key blocks outside a gray frame.

The transformation logic involves several steps:
1. Identifying a rectangular frame made of a specific color (gray, value 5) in the input grid by finding the minimum and maximum row and column indices of pixels with this color.
2. Locating key-value color pairs outside this frame by examining adjacent pixels. The logic prioritizes horizontal (left->right) adjacency, then vertical (top->down) adjacency to establish a mapping rule (Color A -> Color B). The frame color and the determined background color are ignored when searching for these pairs.
3. Determining the background color that should remain invariant during the transformation. This is identified as the most frequent color found in the area outside the frame, excluding the frame color itself and any colors that become part of a mapping rule (either as a key or a value). Fallback mechanisms are included if this primary identification method is ambiguous or fails.
4. Cropping the input grid to the exact region defined by the frame's bounding box (inclusive).
5. Creating the output grid by applying the derived mapping rules to the pixels within this cropped region. Pixels matching a key color (Color A) are changed to the corresponding value color (Color B). The frame color (5) and the identified invariant background color are preserved in their original positions. Any other pixel colors within the frame that are not part of the mapping rules also remain unchanged.
"""

def find_frame_bbox(grid_np: np.ndarray, frame_color: int = 5) -> tuple[int, int, int, int] | None:
    """
    Finds the bounding box coordinates (min_row, min_col, max_row, max_col) 
    of the pixels matching the specified frame color using their minimum and maximum indices.
    Returns None if the frame color is not present in the grid.
    """
    # Find all coordinates where the grid matches the frame color
    coords = np.argwhere(grid_np == frame_color)
    
    # If no coordinates are found, the frame color doesn't exist; return None
    if coords.size == 0:
        return None 
        
    # Determine the minimum and maximum row and column indices from the coordinates
    r_min, c_min = coords.min(axis=0)
    r_max, c_max = coords.max(axis=0)
    
    # Return the bounding box coordinates
    return (r_min, c_min, r_max, c_max)


def find_mapping_rules_and_background(grid_np: np.ndarray, frame_bbox: tuple[int, int, int, int] | None, frame_color: int = 5) -> tuple[dict[int, int], int]:
    """
    Identifies color mapping rules (as a dictionary {key_color: value_color}) 
    and the invariant background color (as an integer) by analyzing the region 
    of the grid outside the provided frame bounding box.
    """
    rows, cols = grid_np.shape
    
    # If the frame bounding box is not provided, return default empty mappings and background color 0
    if frame_bbox is None:
         print("Warning: Frame bounding box is None in find_mapping_rules. Returning defaults.")
         return {}, 0 

    r_min, c_min, r_max, c_max = frame_bbox

    outside_colors_counter = Counter()
    outside_coords = []
    # Iterate through each cell of the grid
    for r in range(rows):
        for c in range(cols):
            # Determine if the current cell is outside the frame's bounding box
            is_outside = not (r >= r_min and r <= r_max and c >= c_min and c <= c_max)
            if is_outside:
                color = grid_np[r, c]
                # Count the frequency of non-frame colors outside the frame
                if color != frame_color:
                    outside_colors_counter[color] += 1
                # Store the coordinates of all cells outside the frame
                outside_coords.append((r, c))

    # --- Determine Potential Background Color ---
    potential_background = -1
    # Sort the counted outside colors by frequency (descending) and then by color value (ascending)
    sorted_colors = sorted(outside_colors_counter.items(), key=lambda item: (-item[1], item[0]))
    # The most frequent color is the initial candidate for the background
    if sorted_colors:
        potential_background = sorted_colors[0][0] 
    else:
        # If no non-frame colors were found outside, default the background to 0
        potential_background = 0 

    # --- Find Mapping Rules by Checking Adjacency ---
    mappings = {} # Dictionary to store color_a -> color_b mappings
    mapped_colors = set() # Set to track colors involved in any mapping (key or value)
    processed_pairs = set() # Set to track unique pairs (a,b) to avoid redundant checks

    # Iterate through the coordinates identified as being outside the frame
    for r, c in outside_coords:
        color_a = grid_np[r, c]
        # Skip if the color is the frame color, the potential background, or already a mapping key
        if color_a == frame_color or color_a == potential_background or color_a in mappings:
            continue

        # Check the neighbor to the right
        if c + 1 < cols:
             nr, nc = r, c + 1
             # Check if the right neighbor is also outside the frame
             is_neighbor_outside = not (nr >= r_min and nr <= r_max and nc >= c_min and nc <= c_max)
             if is_neighbor_outside:
                 color_b = grid_np[nr, nc]
                 # Check if color_b is a valid target for mapping (different from A, not frame, not background)
                 if color_b != color_a and color_b != frame_color and color_b != potential_background:
                     # Create a sorted tuple to uniquely identify the pair regardless of order
                     pair = tuple(sorted((color_a, color_b)))
                     # If this pair hasn't been processed and color_a hasn't been mapped yet
                     if pair not in processed_pairs and color_a not in mappings:
                         # Establish the mapping A -> B (horizontal priority)
                         mappings[color_a] = color_b
                         mapped_colors.add(color_a)
                         mapped_colors.add(color_b)
                         processed_pairs.add(pair)
                         # Once color_a is mapped, move to the next coordinate in outside_coords
                         continue 

        # If no horizontal mapping was found, check the neighbor below
        if r + 1 < rows:
             nr, nc = r + 1, c
             # Check if the bottom neighbor is also outside the frame
             is_neighbor_outside = not (nr >= r_min and nr <= r_max and nc >= c_min and nc <= c_max)
             if is_neighbor_outside:
                  color_b = grid_np[nr, nc]
                  # Check if color_b is a valid target for mapping
                  if color_b != color_a and color_b != frame_color and color_b != potential_background:
                      pair = tuple(sorted((color_a, color_b)))
                      # If this pair hasn't been processed and color_a hasn't been mapped yet
                      if pair not in processed_pairs and color_a not in mappings:
                           # Establish the mapping A -> B (vertical)
                           mappings[color_a] = color_b
                           mapped_colors.add(color_a)
                           mapped_colors.add(color_b)
                           processed_pairs.add(pair)
                           # Loop continues to the next coordinate

    # --- Finalize Background Color ---
    actual_background = potential_background
    # If the initial potential background color was used in a mapping
    if potential_background in mapped_colors:
        actual_background = -1 # Reset the background color
        # Find the next most frequent outside color that *wasn't* mapped
        for color, count in sorted_colors: 
            if color not in mapped_colors:
                actual_background = color
                break # Found a suitable background color

        # Fallback if all outside non-frame colors were involved in mappings
        if actual_background == -1:
            # Check inside the frame (excluding the border) for the most frequent color
            # that isn't the frame color and wasn't mapped.
            inside_counter = Counter()
            # Check if frame has an interior (width and height > 1 pixel excluding borders)
            if r_max > r_min and c_max > c_min: 
                 for r_in in range(r_min + 1, r_max):
                     for c_in in range(c_min + 1, c_max):
                         color = grid_np[r_in, c_in]
                         # Count frequency if not frame color and not already mapped
                         if color != frame_color and color not in mapped_colors:
                             inside_counter[color] += 1
            
            # Sort the inside colors by frequency
            sorted_inside = sorted(inside_counter.items(), key=lambda item: (-item[1], item[0]))
            if sorted_inside:
                 # The most frequent unmapped inside color becomes the background
                 actual_background = sorted_inside[0][0] 
            else:
                # If no suitable background found via any method, default to 0
                print("Warning: Could not determine a definitive background color. Defaulting to 0.")
                actual_background = 0 

    # Return the final mapping rules and the determined background color
    return mappings, actual_background


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid according to ARC task logic:
    1. Finds a gray (5) frame.
    2. Derives color mapping rules from adjacent color blocks outside the frame.
    3. Determines the invariant background color.
    4. Crops the grid to the frame's boundaries.
    5. Applies the mappings to the cropped area, preserving frame and background colors.
    """
    # Convert the input list of lists to a NumPy array for efficient operations
    input_np = np.array(input_grid, dtype=int)
    frame_color = 5 # Define the color designated as the frame

    # Step 1: Find the bounding box of the gray frame
    frame_bbox = find_frame_bbox(input_np, frame_color)

    # If no frame is detected, return the original input grid as per ARC convention
    if frame_bbox is None:
        # print("Warning: No frame (color 5) found. Returning input grid unchanged.")
        return input_grid

    r_min, c_min, r_max, c_max = frame_bbox

    # Step 2: Determine the color mapping rules and the invariant background color
    mappings, invariant_background = find_mapping_rules_and_background(input_np, frame_bbox, frame_color)

    # Step 3: Crop the input grid to the area defined by the frame's bounding box.
    # Create a copy to avoid modifying the original input array slice.
    output_np = input_np[r_min:r_max + 1, c_min:c_max + 1].copy()
    output_h, output_w = output_np.shape # Get dimensions of the output grid

    # Step 4: Apply the transformation rules to the cropped grid (output_np)
    for r_out in range(output_h):
        for c_out in range(output_w):
            current_color = output_np[r_out, c_out]

            # Check conditions and apply transformations:
            # If the color is the frame color, do nothing.
            if current_color == frame_color:
                continue 
            # If the color is the invariant background, do nothing.
            elif current_color == invariant_background:
                continue 
            # If the color is a key in the mappings dictionary, change it to the mapped value.
            elif current_color in mappings:
                output_np[r_out, c_out] = mappings[current_color]
            # Otherwise (color is not frame, not background, not a mapping key), it remains unchanged.
            
    # Convert the transformed NumPy array back to a standard Python list of lists
    output_grid = output_np.tolist()

    # Return the final transformed grid
    return output_grid
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
1 1 4 4 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
1 1 1 4 8 8 1 8 1 8 8 3 8 3 8 8 8 8 8 8 8 8 8 8
1 1 4 4 8 8 1 1 1 8 8 3 3 3 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 1 8 8 8 3 3 3 8 8 8 8 8 8 8 8 8 8
3 3 2 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
3 3 3 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
3 3 2 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 8 8
8 8 8 5 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 5 8 8
8 8 8 5 8 3 3 3 8 1 1 1 8 3 3 3 8 1 1 1 8 5 8 8
8 8 8 5 8 3 3 3 8 1 1 1 8 3 3 3 8 1 1 1 8 5 8 8
8 8 8 5 8 3 3 3 8 1 1 1 8 3 3 3 8 1 1 1 8 5 8 8
8 8 8 5 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 5 8 8
8 8 8 5 8 3 3 3 8 1 1 1 8 8 8 8 8 3 3 3 8 5 8 8
8 8 8 5 8 3 3 3 8 1 1 1 8 8 8 8 8 3 3 3 8 5 8 8
8 8 8 5 8 3 3 3 8 1 1 1 8 8 8 8 8 3 3 3 8 5 8 8
8 8 8 5 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 5 8 8
8 8 8 5 8 8 8 8 8 3 3 3 8 1 1 1 8 1 1 1 8 5 8 8
8 8 8 5 8 8 8 8 8 3 3 3 8 1 1 1 8 1 1 1 8 5 8 8
8 8 8 5 8 8 8 8 8 3 3 3 8 1 1 1 8 1 1 1 8 5 8 8
8 8 8 5 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 5 8 8
8 8 8 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 8 8
```
Expected Output:
```
5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5
5 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 5
5 8 2 8 2 8 4 8 4 8 2 8 2 8 4 8 4 8 5
5 8 2 2 2 8 4 4 4 8 2 2 2 8 4 4 4 8 5
5 8 2 2 2 8 8 4 8 8 2 2 2 8 8 4 8 8 5
5 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 5
5 8 2 8 2 8 4 8 4 8 8 8 8 8 2 8 2 8 5
5 8 2 2 2 8 4 4 4 8 8 8 8 8 2 2 2 8 5
5 8 2 2 2 8 8 4 8 8 8 8 8 8 2 2 2 8 5
5 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 5
5 8 8 8 8 8 2 8 2 8 4 8 4 8 4 8 4 8 5
5 8 8 8 8 8 2 2 2 8 4 4 4 8 4 4 4 8 5
5 8 8 8 8 8 2 2 2 8 8 4 8 8 8 4 8 8 5
5 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 5
5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5
```
Transformed Output:
```
5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5
5 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 5
5 8 2 2 2 8 4 4 4 8 2 2 2 8 4 4 4 8 5
5 8 2 2 2 8 4 4 4 8 2 2 2 8 4 4 4 8 5
5 8 2 2 2 8 4 4 4 8 2 2 2 8 4 4 4 8 5
5 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 5
5 8 2 2 2 8 4 4 4 8 8 8 8 8 2 2 2 8 5
5 8 2 2 2 8 4 4 4 8 8 8 8 8 2 2 2 8 5
5 8 2 2 2 8 4 4 4 8 8 8 8 8 2 2 2 8 5
5 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 5
5 8 8 8 8 8 2 2 2 8 4 4 4 8 4 4 4 8 5
5 8 8 8 8 8 2 2 2 8 4 4 4 8 4 4 4 8 5
5 8 8 8 8 8 2 2 2 8 4 4 4 8 4 4 4 8 5
5 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 5
5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5
```
Match: False
Pixels Off: 20
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 14.035087719298247

## Example 2:
Input:
```
2 2 4 4 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
2 2 2 4 1 1 2 2 2 2 1 3 3 3 3 1 1 6 6 6 6 1 1
2 2 4 4 1 1 2 2 2 2 1 1 3 3 1 1 1 6 6 1 1 1 1
1 1 1 1 1 1 2 1 2 2 1 3 3 3 3 1 1 6 6 1 1 1 1
3 3 8 8 1 1 2 1 2 2 1 3 1 1 3 1 1 6 6 6 6 1 1
3 3 3 8 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
3 3 8 8 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
6 6 7 7 1 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5
6 6 6 7 1 5 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 5
6 6 7 7 1 5 1 2 2 2 2 1 6 6 6 6 1 3 3 3 3 1 5
1 1 1 1 1 5 1 2 2 2 2 1 6 6 6 6 1 3 3 3 3 1 5
1 1 1 1 1 5 1 2 2 2 2 1 6 6 6 6 1 3 3 3 3 1 5
1 1 1 1 1 5 1 2 2 2 2 1 6 6 6 6 1 3 3 3 3 1 5
1 1 1 1 1 5 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 5
1 1 1 1 1 5 1 3 3 3 3 1 2 2 2 2 1 6 6 6 6 1 5
1 1 1 1 1 5 1 3 3 3 3 1 2 2 2 2 1 6 6 6 6 1 5
1 1 1 1 1 5 1 3 3 3 3 1 2 2 2 2 1 6 6 6 6 1 5
1 1 1 1 1 5 1 3 3 3 3 1 2 2 2 2 1 6 6 6 6 1 5
1 1 1 1 1 5 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 5
1 1 1 1 1 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
```
Expected Output:
```
5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5
5 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 5
5 1 4 4 4 4 1 7 7 7 7 1 8 8 8 8 1 5
5 1 4 4 4 4 1 7 7 1 1 1 1 8 8 1 1 5
5 1 4 1 4 4 1 7 7 1 1 1 8 8 8 8 1 5
5 1 4 1 4 4 1 7 7 7 7 1 8 1 1 8 1 5
5 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 5
5 1 8 8 8 8 1 4 4 4 4 1 7 7 7 7 1 5
5 1 1 8 8 1 1 4 4 4 4 1 7 7 1 1 1 5
5 1 8 8 8 8 1 4 1 4 4 1 7 7 1 1 1 5
5 1 8 1 1 8 1 4 1 4 4 1 7 7 7 7 1 5
5 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 5
5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5
```
Transformed Output:
```
5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5
5 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 5
5 1 4 4 4 4 1 7 7 7 7 1 8 8 8 8 1 5
5 1 4 4 4 4 1 7 7 7 7 1 8 8 8 8 1 5
5 1 4 4 4 4 1 7 7 7 7 1 8 8 8 8 1 5
5 1 4 4 4 4 1 7 7 7 7 1 8 8 8 8 1 5
5 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 5
5 1 8 8 8 8 1 4 4 4 4 1 7 7 7 7 1 5
5 1 8 8 8 8 1 4 4 4 4 1 7 7 7 7 1 5
5 1 8 8 8 8 1 4 4 4 4 1 7 7 7 7 1 5
5 1 8 8 8 8 1 4 4 4 4 1 7 7 7 7 1 5
5 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 5
5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5
```
Match: False
Pixels Off: 20
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 17.09401709401709
