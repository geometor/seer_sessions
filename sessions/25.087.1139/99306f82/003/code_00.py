import numpy as np
from collections import Counter

"""
Identifies a hollow rectangular frame in the input grid, finds non-white 'source' pixels outside this frame, sorts their colors by position (sum of row and column index), and fills the frame's white interior with concentric layers using the sorted colors. The innermost layers reuse the last available source color if the layer index exceeds the number of source colors.
"""

def find_frame_and_bounding_box(grid):
    """
    Finds the most likely frame object (largest hollow single-color rectangle)
    and its bounding box.
    Returns the frame color and its outer bounding box (min_r, min_c, max_r, max_c),
    or (None, None) if no suitable frame is found.

    Strategy:
    1. Identify all non-background pixels and their colors/locations.
    2. Count frequency of each non-background color.
    3. Prioritize finding hollow rectangles: Iterate through unique colors.
       For each color, find its bounding box. Check if the center is background.
       Select the color forming the largest hollow rectangle.
    4. If no hollow rectangle found, fallback: find the non-background object
       with the largest bounding box area, even if not hollow. Use its color/bbox.
    5. If still no object found, return None.
    """
    non_background_pixels = []
    colors_present = Counter()
    height, width = grid.shape
    for r in range(height):
        for c in range(width):
            color = grid[r, c]
            if color != 0:
                non_background_pixels.append({'color': color, 'r': r, 'c': c})
                colors_present[color] += 1

    if not colors_present:
        return None, None # No non-background pixels at all

    best_frame_color = -1
    best_bbox = None
    max_hollow_area = -1
    max_any_area = -1
    fallback_color = -1
    fallback_bbox = None

    unique_colors = list(colors_present.keys())

    for color in unique_colors:
        coords = [(p['r'], p['c']) for p in non_background_pixels if p['color'] == color]
        if not coords: continue

        min_r = min(r for r, c in coords)
        min_c = min(c for r, c in coords)
        max_r = max(r for r, c in coords)
        max_c = max(c for r, c in coords)
        bbox = (min_r, min_c, max_r, max_c)
        area = (max_r - min_r + 1) * (max_c - min_c + 1)

        # Check for hollowness: requires size > 1x1 and inner point is background
        is_hollow = False
        if max_r > min_r and max_c > min_c:
            # Check multiple interior points for robustness? For now, center.
            # A more robust check would be ensuring all frame pixels are present and interior is empty
            inner_r_start, inner_c_start = min_r + 1, min_c + 1
            inner_r_end, inner_c_end = max_r - 1, max_c - 1
            
            # Simplistic check: is the top-left inner pixel background?
            if grid[inner_r_start, inner_c_start] == 0:
                 is_hollow = True # Assume hollow based on one point for now

                 # More robust check (optional): Verify all interior points are background
                 # all_interior_bg = True
                 # for r_in in range(inner_r_start, inner_r_end + 1):
                 #     for c_in in range(inner_c_start, inner_c_end + 1):
                 #         if grid[r_in, c_in] != 0:
                 #             all_interior_bg = False
                 #             break
                 #     if not all_interior_bg:
                 #         break
                 # is_hollow = all_interior_bg


        if is_hollow:
            if area > max_hollow_area:
                max_hollow_area = area
                best_frame_color = color
                best_bbox = bbox
        elif area > max_any_area: # Track largest non-hollow as fallback
             max_any_area = area
             fallback_color = color
             fallback_bbox = bbox

    # Prefer hollow frame, otherwise take largest object
    if best_frame_color != -1:
        # Further validation: ensure the detected bbox actually forms a rectangle of 'color'
        is_valid_frame = True
        # Check horizontal lines
        for c in range(best_bbox[1], best_bbox[3] + 1):
            if grid[best_bbox[0], c] != best_frame_color or grid[best_bbox[2], c] != best_frame_color:
                is_valid_frame = False
                break
        # Check vertical lines
        if is_valid_frame:
            for r in range(best_bbox[0] + 1, best_bbox[2]):
                 if grid[r, best_bbox[1]] != best_frame_color or grid[r, best_bbox[3]] != best_frame_color:
                     is_valid_frame = False
                     break
        
        if is_valid_frame:
             return best_frame_color, best_bbox
        else:
             # Invalid frame structure detected, maybe fall back?
             # For now, if the largest hollow candidate isn't a proper frame,
             # we might need a more sophisticated detection or clear failure.
             # Let's try the non-hollow fallback if the hollow one was invalid.
             if fallback_color != -1:
                 # We might want to validate the fallback too, but skipping for now
                 return fallback_color, fallback_bbox
             else:
                 return None, None # No suitable frame found


    elif fallback_color != -1:
        # Use the largest non-hollow object if no hollow ones found
        # We might not want to fill if it's not hollow, depends on task rules
        # Based on examples, the task requires a hollow frame to fill.
        # So, if only a solid object is found, maybe return None for frame?
        # Re-evaluating: The original code assumed the most frequent color forms the frame.
        # Let's stick to the "largest hollow" priority first. If no hollow frame, fail.
         return None, None # No hollow frame found
        # return fallback_color, fallback_bbox # uncomment if solid objects can be 'frames'
    else:
        return None, None # No frame found

def find_source_pixels(grid, frame_bbox):
    """
    Finds non-white pixels outside the frame's bounding box.
    Returns a list of dictionaries, each containing color, r, c, and sort_key (r+c).
    """
    source_pixels = []
    if frame_bbox is None:
        # If no frame, consider all non-white pixels as sources?
        # Or return empty list as per original logic? Let's stick to original.
        return []

    frame_min_r, frame_min_c, frame_max_r, frame_max_c = frame_bbox
    height, width = grid.shape

    for r in range(height):
        for c in range(width):
            # Check if pixel is outside the frame's bounding box
            is_outside = (r < frame_min_r or r > frame_max_r or
                          c < frame_min_c or c > frame_max_c)

            if is_outside and grid[r, c] != 0:
                source_pixels.append({
                    'color': grid[r, c],
                    'r': r,
                    'c': c,
                    'sort_key': r + c # Manhattan distance from origin (0,0)
                })
    return source_pixels

def transform(input_grid):
    # Convert input to numpy array for easier manipulation
    grid = np.array(input_grid, dtype=int)
    # Initialize output grid as a copy of the input
    output_grid = grid.copy()

    # 1. Identify the Frame
    # Find the hollow rectangular frame object and determine its color and bounding box.
    frame_color, frame_bbox = find_frame_and_bounding_box(grid)

    # If no frame is found, return the input grid unchanged.
    if frame_bbox is None:
        return output_grid.tolist()

    frame_min_r, frame_min_c, frame_max_r, frame_max_c = frame_bbox

    # 2. Find Source Pixels
    # Identify all non-white pixels located outside the frame's bounding box.
    source_pixels = find_source_pixels(grid, frame_bbox)

    # 3. Order Source Colors
    # Create an ordered list of colors from the source pixels, sorted by their position (ascending r + c).
    source_pixels.sort(key=lambda p: p['sort_key'])
    sorted_colors = [p['color'] for p in source_pixels]

    # If there are no source pixels, return the input grid unchanged (no colors to fill with).
    if not sorted_colors:
        return output_grid.tolist()

    # 4. Prepare Output Grid (already done by copying input)

    # 5. Define the interior bounding box (pixels inside the frame walls)
    inner_min_r = frame_min_r + 1
    inner_min_c = frame_min_c + 1
    inner_max_r = frame_max_r - 1
    inner_max_c = frame_max_c - 1

    # Check if there is an actual interior to fill
    if inner_min_r > inner_max_r or inner_min_c > inner_max_c:
        return output_grid.tolist() # Frame is too thin, no interior

    # 6-9. Fill Interior
    # Iterate through each pixel location (r, c) within the inner area.
    for r in range(inner_min_r, inner_max_r + 1):
        for c in range(inner_min_c, inner_max_c + 1):
            # Check if the pixel was originally background (white) in the input.
            if grid[r, c] == 0:
                # Calculate its 'layer index': minimum distance to the inner boundary.
                dist_r_min = r - inner_min_r
                dist_r_max = inner_max_r - r
                dist_c_min = c - inner_min_c
                dist_c_max = inner_max_c - c
                layer_index = min(dist_r_min, dist_r_max, dist_c_min, dist_c_max)

                # Determine the color index, clamping to the available colors.
                # Use the last color if layer_index >= number of colors.
                color_index = min(layer_index, len(sorted_colors) - 1)

                # Get the fill color from the sorted list.
                fill_color = sorted_colors[color_index]

                # Update the output grid with the fill color.
                output_grid[r, c] = fill_color

    # 10. Return Result
    # Convert the result back to a list of lists.
    return output_grid.tolist()