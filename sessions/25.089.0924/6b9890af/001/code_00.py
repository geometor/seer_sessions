"""
Transformation Rule:
1. Identify two non-background objects in the input grid: a hollow red (2) rectangle (the "Frame") and another distinct colored object (the "Inner Shape").
2. Determine the bounding box of the Frame. The output grid will have the same dimensions as the Frame's bounding box.
3. Initialize the output grid with the background color (0).
4. Draw the Frame onto the output grid by copying the red pixels relative to the Frame's bounding box.
5. Determine the bounding box and color of the Inner Shape. Extract the pattern of the Inner Shape relative to its bounding box.
6. Calculate the dimensions of the hollow space inside the Frame (Frame height - 2, Frame width - 2).
7. Calculate the integer scaling factor by dividing the inner dimensions of the Frame by the dimensions of the Inner Shape pattern (using integer division, taking the minimum of height and width scaling factors).
8. Scale the Inner Shape pattern by the calculated scaling factor.
9. Center the scaled Inner Shape pattern within the hollow space of the Frame in the output grid.
10. Fill the corresponding pixels in the output grid with the Inner Shape's color, replacing the background color (0). Pixels belonging to the Frame remain unchanged.
"""

import numpy as np
from collections import deque

def find_objects(grid, exclude_colors=[0]):
    """
    Finds contiguous objects of the same color in a grid.

    Args:
        grid (np.array): The input grid.
        exclude_colors (list): List of colors to ignore (usually background).

    Returns:
        list: A list of dictionaries, each representing an object with
              'color', 'coords' (list of (r, c) tuples), and
              'bbox' (min_r, min_c, max_r, max_c).
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    q = deque()

    for r in range(rows):
        for c in range(cols):
            # Check if the cell is not visited and not an excluded color
            if not visited[r, c] and grid[r, c] not in exclude_colors:
                color = grid[r, c]
                coords = []
                q.append((r, c))
                visited[r, c] = True
                min_r, min_c = r, c
                max_r, max_c = r, c

                # Start Breadth-First Search (BFS)
                while q:
                    row, col = q.popleft()
                    coords.append((row, col))
                    # Update bounding box
                    min_r = min(min_r, row)
                    min_c = min(min_c, col)
                    max_r = max(max_r, row)
                    max_c = max(max_c, col)

                    # Explore neighbors (4-connectivity: up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        # Check bounds, visited status, and color match
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))

                # Store the found object
                objects.append({
                    'color': color,
                    'coords': coords,
                    'bbox': (min_r, min_c, max_r, max_c)
                })
    return objects

def transform(input_grid):
    """
    Applies the frame-and-scale transformation to the input grid.
    """
    # Convert input list of lists to a NumPy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    rows, cols = input_np.shape

    # Find all non-background objects in the grid
    objects = find_objects(input_np, exclude_colors=[0])

    # Identify the Frame (color 2) and the Inner Shape (other non-zero color)
    frame_obj = None
    inner_shape_obj = None
    for obj in objects:
        if obj['color'] == 2:
            frame_obj = obj
        elif obj['color'] != 0: # Find the first non-zero, non-frame object
            inner_shape_obj = obj
        # Stop if both objects are found
        if frame_obj and inner_shape_obj:
            break

    # Handle cases where expected objects are not found
    if frame_obj is None:
        # If no frame is found, return an empty grid or the input?
        # Let's return an empty grid for now, as output size is undefined.
        print("Error: Frame object (color 2) not found.")
        return []
    if inner_shape_obj is None:
        # If only frame found, return just the frame cropped? Let's return empty.
        print("Error: Inner shape object (non-zero, non-2 color) not found.")
        return []


    # --- Extract Frame details ---
    frame_color = frame_obj['color']
    frame_coords = frame_obj['coords']
    frame_r_min, frame_c_min, frame_r_max, frame_c_max = frame_obj['bbox']
    # Calculate frame dimensions based on bounding box
    frame_h = frame_r_max - frame_r_min + 1
    frame_w = frame_c_max - frame_c_min + 1

    # --- Extract Inner Shape details ---
    inner_shape_color = inner_shape_obj['color']
    inner_shape_coords = inner_shape_obj['coords']
    inner_shape_r_min, inner_shape_c_min, inner_shape_r_max, inner_shape_c_max = inner_shape_obj['bbox']
    # Calculate inner shape dimensions based on bounding box
    inner_shape_h = inner_shape_r_max - inner_shape_r_min + 1
    inner_shape_w = inner_shape_c_max - inner_shape_c_min + 1

    # --- Create the Inner Shape pattern grid ---
    # This grid represents the shape relative to its own bounding box
    inner_shape_pattern = np.zeros((inner_shape_h, inner_shape_w), dtype=int)
    for r, c in inner_shape_coords:
        rel_r = r - inner_shape_r_min # Row relative to pattern top
        rel_c = c - inner_shape_c_min # Col relative to pattern left
        inner_shape_pattern[rel_r, rel_c] = inner_shape_color

    # --- Initialize Output Grid ---
    # Output grid size is determined by the frame's bounding box size
    output_h = frame_h
    output_w = frame_w
    output_grid = np.zeros((output_h, output_w), dtype=int) # Fill with background (0)

    # --- Draw the Frame onto the Output Grid ---
    # Iterate through the coordinates of the frame object
    for r, c in frame_coords:
        # Calculate position relative to the top-left of the frame's bounding box
        out_r = r - frame_r_min
        out_c = c - frame_c_min
        # Ensure the calculated position is within the output grid bounds
        if 0 <= out_r < output_h and 0 <= out_c < output_w:
             output_grid[out_r, out_c] = frame_color

    # --- Calculate Scaling Factor ---
    # Determine the dimensions of the hollow area inside the frame
    # Assumes a 1-pixel thick border for the frame
    inner_frame_h = frame_h - 2
    inner_frame_w = frame_w - 2

    # Check if the inner area is valid (positive dimensions)
    if inner_frame_h <= 0 or inner_frame_w <= 0:
         # If no inner space, return the grid with just the frame
         return output_grid.tolist()

    # Avoid division by zero if inner shape has zero height or width
    if inner_shape_h == 0 or inner_shape_w == 0:
        # This shouldn't happen if a valid object was found, but handle defensively
        return output_grid.tolist()

    # Calculate how many times the inner shape fits into the inner frame area
    scale_h = inner_frame_h // inner_shape_h
    scale_w = inner_frame_w // inner_shape_w
    # Use the minimum of the two scales to ensure the scaled shape fits entirely
    scale = min(scale_h, scale_w)

    # If the inner shape is too large to fit even once (scale = 0), return just the frame
    if scale == 0:
        return output_grid.tolist()

    # --- Calculate Placement for Scaled Inner Shape ---
    # Calculate the dimensions of the pattern after scaling
    scaled_pattern_h = inner_shape_h * scale
    scaled_pattern_w = inner_shape_w * scale

    # Calculate the offset needed to center the scaled pattern within the inner frame area
    offset_r = (inner_frame_h - scaled_pattern_h) // 2
    offset_c = (inner_frame_w - scaled_pattern_w) // 2

    # Calculate the top-left starting position of the scaled pattern in the *full* output grid
    # Add 1 because the inner area starts at index (1, 1) due to the frame border
    start_r = 1 + offset_r
    start_c = 1 + offset_c

    # --- Scale and Draw the Inner Shape onto the Output Grid ---
    # Iterate through each pixel of the original inner shape pattern
    for pr in range(inner_shape_h): # Pattern row
        for pc in range(inner_shape_w): # Pattern column
            # If the pattern pixel is part of the shape (not background)
            if inner_shape_pattern[pr, pc] == inner_shape_color:
                # Calculate the top-left corner of the scaled block in the output grid
                block_start_r = start_r + pr * scale
                block_start_c = start_c + pc * scale
                # Fill the scale x scale block in the output grid
                for r_offset in range(scale):
                    for c_offset in range(scale):
                        out_r = block_start_r + r_offset
                        out_c = block_start_c + c_offset
                        # Check bounds again for safety
                        if 0 <= out_r < output_h and 0 <= out_c < output_w:
                            # Only draw the inner shape color if the target pixel is currently background (0)
                            # This prevents overwriting the frame itself.
                            if output_grid[out_r, out_c] == 0:
                                output_grid[out_r, out_c] = inner_shape_color

    # Convert the final NumPy array back to a standard list of lists format
    return output_grid.tolist()