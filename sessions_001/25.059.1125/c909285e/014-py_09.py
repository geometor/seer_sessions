"""
1. **Identify the Framing Object:** Find the largest contiguous object in the input grid that forms a "frame" around other pixels.  The frame's color is determined by the pixels forming a closed shape.
2. **Extract Interior:** Extract all pixels that are located *inside* the identified frame, recording their colors and positions relative to the frame.
3. **Create Output Grid:** Create output grid based on relative positions of enclosed pixels.
4. **Include Frame Pixel (Conditional):** If all enclosed pixels share the same color, find *one* pixel of the framing object that is directly adjacent (horizontally or vertically, not diagonally) to any of the enclosed pixels. Add this frame pixel to the output grid, maintaining its relative position as in the input.
"""

import numpy as np

def find_framing_object(grid):
    """
    Finds the largest contiguous object that encloses other pixels, prioritizing edge-connected shapes.
    """
    unique_colors = np.unique(grid)
    largest_object = None
    max_area = 0

    for color in unique_colors:
        rows, cols = np.where(grid == color)
        if rows.size == 0:
            continue

        min_row, max_row = np.min(rows), np.max(rows)
        min_col, max_col = np.min(cols), np.max(cols)

        # Check if there are other colors within this bounding box
        has_enclosed_pixels = False
        for r in range(min_row + 1, max_row):
            for c in range(min_col + 1, max_col):
                if grid[r,c] != color:
                    has_enclosed_pixels = True
                    break
            if has_enclosed_pixels:
                break

        if has_enclosed_pixels:
            # Calculate area and perimeter
            area = (max_row - min_row + 1) * (max_col - min_col + 1)
            perimeter = 2 * (max_row - min_row + 1 + max_col - min_col + 1)
            
            if area > max_area:
                max_area = area
                largest_object = (min_row, max_row, min_col, max_col, color)

    return largest_object

def get_enclosed_pixels(grid, frame_bbox):
    """Extracts pixels inside the frame, along with their coordinates relative to the frame's top-left corner."""
    min_row, max_row, min_col, max_col, frame_color = frame_bbox
    enclosed_pixels = []
    for r in range(min_row + 1, max_row):
        for c in range(min_col + 1, max_col):
            if grid[r, c] != frame_color:
                enclosed_pixels.append((r - min_row - 1, c - min_col - 1, grid[r, c]))  # Relative coordinates and color
    return enclosed_pixels

def find_adjacent_frame_pixel(grid, frame_bbox, enclosed_pixels):
    """Finds a frame pixel adjacent (horizontally/vertically) to the enclosed pixels."""
    min_row, max_row, min_col, max_col, frame_color = frame_bbox
    
    # Convert enclosed pixel coordinates to absolute coordinates
    enclosed_abs = [(r + min_row + 1, c + min_col + 1) for r, c, _ in enclosed_pixels]

    for r in range(min_row, max_row + 1):
        for c in range(min_col, max_col + 1):
            if grid[r, c] == frame_color:
                # Check for horizontal/vertical adjacency
                for er, ec in enclosed_abs:
                    if (abs(r - er) == 1 and c == ec) or (r == er and abs(c - ec) == 1):
                        return (r, c, frame_color)  # Return absolute coordinates and color
    return None

def get_output_grid_dimensions(enclosed_pixels, frame_pixel, frame_bbox):
    """
    Calculates output grid dimensions based on enclosed pixels and a potential frame pixel, relative to frame.
    """
    max_r = 0
    max_c = 0

    #adjust enclosed pixels for frame origin
    frame_min_row, _, frame_min_col, _, _ = frame_bbox

    for r, c, _ in enclosed_pixels:
      adj_r = r
      adj_c = c
      max_r = max(max_r, adj_r)
      max_c = max(max_c, adj_c)
        
    if frame_pixel:
        frame_r, frame_c, _ = frame_pixel
        adj_fr = frame_r - frame_min_row - 1
        adj_fc = frame_c - frame_min_col - 1

        max_r = max(max_r, adj_fr )
        max_c = max(max_c, adj_fc )
    
    return max_r + 1, max_c + 1

def transform(input_grid):
    # Convert input to numpy array
    input_grid = np.array(input_grid)

    # Find the framing object
    frame_bbox = find_framing_object(input_grid)
    if frame_bbox is None:
        return input_grid.tolist()  # Return original if no frame

    # Extract pixels inside the frame
    enclosed_pixels = get_enclosed_pixels(input_grid, frame_bbox)
    if not enclosed_pixels:
        return input_grid.tolist() #return original if the frame contains nothing

    # Check if all enclosed pixels have the same color
    all_same_color = all(color == enclosed_pixels[0][2] for _, _, color in enclosed_pixels)

    # Find an adjacent frame pixel
    frame_pixel = find_adjacent_frame_pixel(input_grid, frame_bbox, enclosed_pixels) if all_same_color else None
    
    # Determine output grid dimensions, relative to frame
    output_height, output_width = get_output_grid_dimensions(enclosed_pixels, frame_pixel, frame_bbox)

    # Initialize the output grid
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Fill the output grid with the enclosed pixels using relative coords
    frame_min_row, _, frame_min_col, _, _ = frame_bbox
    for r, c, color in enclosed_pixels:
        output_grid[r, c] = color

    # Add the frame pixel if found, position is already adjusted for output grid
    if frame_pixel:
        frame_r, frame_c, frame_color = frame_pixel
        adj_r = frame_r - frame_min_row - 1
        adj_c = frame_c - frame_min_col - 1
        output_grid[adj_r,adj_c] = frame_color
        

    return output_grid.tolist()