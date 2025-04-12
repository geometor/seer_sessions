import numpy as np
from math import floor

"""
Transformation Rule:
1. Identify two distinct non-white objects in the input grid: an 'azure frame' (a hollow rectangle composed solely of color 8) and a 'pattern object' (composed of other non-white, non-azure colors).
2. Determine the bounding box of the pattern object.
3. Determine the bounding box of the hollow white space inside the azure frame. This assumes the frame is a single-pixel thick border.
4. Calculate the top-left coordinates required to place the pattern object such that it appears centered within the hollow space.
5. Create an output grid, initially identical to the input grid.
6. Iterate through each pixel belonging to the identified pattern object in the input grid.
7. For each pattern pixel, copy its color to the corresponding position in the output grid, offset by the calculated centering coordinates within the hollow space. The original pattern object and the frame remain in their initial positions.
"""

def find_objects(grid_np: np.ndarray) -> list[dict]:
    """
    Finds contiguous non-background (non-zero) objects in the grid.
    Uses Breadth-First Search (BFS) to find connected components of non-zero pixels,
    considering pixels connected horizontally, vertically, and diagonally.
    Returns a list of dictionaries, each describing an object with:
    - 'pixels': A set of (row, col) tuples belonging to the object.
    - 'bbox': A dictionary {'min_r', 'max_r', 'min_c', 'max_c'} for the bounding box.
    - 'colors': A set of unique color values present in the object.
    """
    height, width = grid_np.shape
    visited = np.zeros_like(grid_np, dtype=bool)
    objects = []

    for r in range(height):
        for c in range(width):
            # Start BFS if a non-zero pixel is found that hasn't been visited
            if grid_np[r, c] != 0 and not visited[r, c]:
                current_object_pixels = set()
                q = [(r, c)] # Queue for BFS
                visited[r, c] = True
                min_r, min_c = r, c
                max_r, max_c = r, c
                colors_in_object = set()

                while q:
                    row, col = q.pop(0)

                    # Ensure coordinates are valid (should be, due to checks before adding to queue)
                    if not (0 <= row < height and 0 <= col < width):
                        continue

                    # Should not happen if starting point is non-zero and we only add non-zero neighbors
                    # if grid_np[row, col] == 0:
                    #     continue
                        
                    # Add pixel to current object
                    current_object_pixels.add((row, col))
                    colors_in_object.add(grid_np[row, col])
                    min_r = min(min_r, row)
                    min_c = min(min_c, col)
                    max_r = max(max_r, row)
                    max_c = max(max_c, col)

                    # Explore 8 neighbors (Moore neighborhood)
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue # Skip self
                            
                            nr, nc = row + dr, col + dc

                            # Check neighbor bounds and if it's non-zero and not visited
                            if 0 <= nr < height and 0 <= nc < width and \
                               grid_np[nr, nc] != 0 and not visited[nr, nc]:
                                visited[nr, nc] = True
                                q.append((nr, nc))

                # Store the found object if it contains any pixels
                if current_object_pixels: 
                    objects.append({
                        'pixels': current_object_pixels,
                        'bbox': {'min_r': min_r, 'max_r': max_r, 'min_c': min_c, 'max_c': max_c},
                        'colors': colors_in_object
                    })
    return objects

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Identifies a pattern object and a frame object (hollow azure rectangle)
    in the input grid, and copies the pattern object into the center of the
    hollow space within the frame.
    """
    # Convert input to numpy array for easier processing
    grid_np = np.array(input_grid, dtype=int)
    height, width = grid_np.shape
    
    # Create a deep copy for the output grid using list comprehension
    output_grid = [row[:] for row in input_grid]

    # --- Identify Objects ---
    # Find all distinct non-background objects using BFS
    all_objects = find_objects(grid_np)

    # Distinguish the frame object (contains only color 8) and the pattern object
    frame_object = None
    pattern_object = None

    for obj in all_objects:
        # The frame object must contain *only* the color azure (8)
        if obj['colors'] == {8}:
            frame_object = obj
        # The pattern object is any other object that doesn't contain white (0)
        # and isn't the frame object. This handles patterns with single or multiple colors.
        elif 0 not in obj['colors']:
             pattern_object = obj

    # --- Validate Objects ---
    # Proceed only if both a unique frame and a unique pattern object are found
    if frame_object is None or pattern_object is None:
        # This might happen if the input doesn't match the expected structure
        # (e.g., missing frame, missing pattern, multiple patterns, etc.)
        # Returning the original grid is a safe default.
        # print("Warning: Could not uniquely identify frame and pattern objects.")
        return input_grid 

    # --- Calculate Pattern Object Properties ---
    p_bbox = pattern_object['bbox']
    p_min_r, p_min_c = p_bbox['min_r'], p_bbox['min_c']
    p_max_r, p_max_c = p_bbox['max_r'], p_bbox['max_c']
    # Dimensions based on bounding box
    pattern_height = p_max_r - p_min_r + 1
    pattern_width = p_max_c - p_min_c + 1

    # --- Calculate Frame and Hollow Space Properties ---
    f_bbox = frame_object['bbox']
    f_min_r, f_min_c = f_bbox['min_r'], f_bbox['min_c']
    f_max_r, f_max_c = f_bbox['max_r'], f_bbox['max_c']

    # Determine the hollow space based on the frame's bounding box,
    # assuming the frame border is 1 pixel thick.
    hollow_top = f_min_r + 1
    hollow_left = f_min_c + 1
    hollow_bottom = f_max_r - 1
    hollow_right = f_max_c - 1
    hollow_height = hollow_bottom - hollow_top + 1
    hollow_width = hollow_right - hollow_left + 1

    # Basic validation for the hollow space dimensions
    if hollow_height <= 0 or hollow_width <= 0:
        # This could happen if the identified frame object isn't actually hollow
        # or doesn't fit the expected rectangular frame structure.
        # print("Warning: Frame object does not appear to have a valid hollow space.")
        return input_grid

    # --- Calculate Centered Placement Position ---
    # Calculate the offset needed to center the pattern's bounding box within the hollow space.
    # Integer division (floor) handles centering appropriately for odd/even differences.
    target_row_offset = floor((hollow_height - pattern_height) / 2)
    target_col_offset = floor((hollow_width - pattern_width) / 2)

    # Calculate the absolute top-left starting coordinate in the output grid for placing the pattern
    target_start_row = hollow_top + target_row_offset
    target_start_col = hollow_left + target_col_offset

    # --- Copy Pattern Pixels to Output Grid ---
    # Iterate through only the pixels identified as belonging to the pattern object
    for r, c in pattern_object['pixels']:
        # Calculate the pixel's position relative to the top-left corner of its *own* bounding box
        relative_r = r - p_min_r
        relative_c = c - p_min_c

        # Calculate the target coordinate in the output grid by adding the relative position
        # to the calculated starting position (which includes centering offsets).
        target_r = target_start_row + relative_r
        target_c = target_start_col + relative_c

        # Get the color of the pattern pixel from the input grid
        pixel_color = grid_np[r, c]

        # Place the pixel in the output grid, ensuring the target coordinate is within grid bounds.
        if 0 <= target_r < height and 0 <= target_c < width:
            # Modify the list-based output_grid
            output_grid[target_r][target_c] = pixel_color
        else:
            # This case indicates an issue, e.g., pattern too large for hollow space or calculation error.
            # print(f"Warning: Target coordinate ({target_r}, {target_c}) for pixel ({r},{c}) is out of bounds.")
            pass # Continue processing other pixels if possible

    # Return the modified grid as a list of lists
    return output_grid