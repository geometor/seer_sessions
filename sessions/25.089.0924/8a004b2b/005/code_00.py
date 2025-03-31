import numpy as np
from collections import Counter

"""
Transformation Rule:
1. Identify the bounding box defined by yellow (4) pixels in the input grid.
2. Determine the output grid size based on the bounding box dimensions.
3. Find the most frequent non-background color present *outside* the bounding box in the input grid (shift_color). Ties are broken by the smallest color index.
4. Create the output grid, initially filled with the background color (0).
5. Copy the content strictly *inside* the input bounding box to the interior of the output grid (offset by 1 row and 1 column).
6. Identify distinct, contiguous objects (same-colored, non-background pixels) within the copied content area of the output grid.
7. For each pixel of each identified object, calculate potential shifted positions two columns to the left and two columns to the right.
8. If a shifted position is within the output grid bounds and currently contains the background color (0), mark it to be colored with the shift_color.
9. Color all marked shifted positions with the shift_color.
10. Set the four corner pixels of the output grid to yellow (4).
"""

def find_bounding_box(grid, color_value):
    """Finds the min/max row/col for pixels of a specific color."""
    coordinates = np.argwhere(grid == color_value)
    if coordinates.size == 0:
        return None # Indicate not found
    min_row = np.min(coordinates[:, 0])
    min_col = np.min(coordinates[:, 1])
    max_row = np.max(coordinates[:, 0])
    max_col = np.max(coordinates[:, 1])
    return min_row, min_col, max_row, max_col

def get_most_frequent_outside_color(grid, min_r, min_c, max_r, max_c):
    """
    Finds the most frequent non-background (non-0) color outside the bounding box.
    Handles ties by returning the smallest color index.
    Returns 0 if no non-background colors are found outside.
    """
    outside_colors = []
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            # Check if the pixel is outside the bounding box
            is_outside = r < min_r or r > max_r or c < min_c or c > max_c
            if is_outside and grid[r, c] != 0: # Exclude background
                outside_colors.append(grid[r, c])

    if not outside_colors:
        return 0 # Default or fallback color if none found

    # Count frequencies
    color_counts = Counter(outside_colors)

    # Find the max frequency
    max_freq = 0
    # Use items() which is generally preferred over iteritems() in Python 3
    for color, count in color_counts.items():
        if count > max_freq:
            max_freq = count

    # Find all colors with the max frequency
    most_frequent_colors = [color for color, count in color_counts.items() if count == max_freq]

    # Tie-breaking: return the smallest color index
    return min(most_frequent_colors) if most_frequent_colors else 0


def find_objects_in_region(grid, start_row, end_row, start_col, end_col):
    """
    Finds contiguous objects (4-connectivity) of the same color within a specified region.
    Returns a list of objects, where each object is a tuple: (color, set_of_coordinates).
    Skips background color (0).
    """
    objects = []
    if start_row >= end_row or start_col >= end_col: # Handle empty region
        return objects
        
    # Ensure region boundaries are within grid dimensions
    max_r_grid, max_c_grid = grid.shape
    actual_end_row = min(end_row, max_r_grid)
    actual_end_col = min(end_col, max_c_grid)
    
    # Create visited mask only for the relevant region to save memory/time
    visited = np.zeros((actual_end_row - start_row, actual_end_col - start_col), dtype=bool)

    for r_rel in range(actual_end_row - start_row):
        for c_rel in range(actual_end_col - start_col):
            r_abs, c_abs = r_rel + start_row, c_rel + start_col
            # Check if pixel is non-background and not visited *within the region's visited mask*
            if grid[r_abs, c_abs] != 0 and not visited[r_rel, c_rel]:
                color = grid[r_abs, c_abs]
                obj_coords = set()
                q = [(r_abs, c_abs)] # Queue stores absolute coordinates
                visited[r_rel, c_rel] = True

                while q:
                    row, col = q.pop(0)
                    obj_coords.add((row, col))

                    # Check neighbors (4-connectivity)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        # Check grid bounds, region bounds, color match, and not visited
                        if (start_row <= nr < actual_end_row and
                            start_col <= nc < actual_end_col):
                            
                            nr_rel, nc_rel = nr - start_row, nc - start_col # Convert to relative for visited check
                            
                            if (grid[nr, nc] == color and
                                not visited[nr_rel, nc_rel]):
                                
                                visited[nr_rel, nc_rel] = True
                                q.append((nr, nc))

                if obj_coords:
                    objects.append((color, obj_coords))

    return objects


def transform(input_grid):
    """
    Transforms the input grid by extracting content within a yellow bounding box,
    copying it to an output grid, adding shifted "echoes" of the content using
    the most frequent outside color, and placing yellow markers at the corners.
    """
    input_np = np.array(input_grid, dtype=int)
    rows_in, cols_in = input_np.shape

    # 1. Find bounding box using yellow pixels
    bbox = find_bounding_box(input_np, 4)
    if bbox is None:
         # If no yellow markers, pattern doesn't match, return original grid or empty?
         # Based on examples, they always exist. Let's return an empty grid matching expected style.
         return [] 
    min_r, min_c, max_r, max_c = bbox

    # 2. Calculate output grid dimensions
    height = max_r - min_r + 1
    width = max_c - min_c + 1

    # Ensure valid dimensions
    if height <= 0 or width <= 0:
        # Should not happen if bbox found, but safety check.
        return [] 

    # 3. Create output grid initialized with 0s
    output_np = np.zeros((height, width), dtype=int)

    # 4. Find the most frequent color outside the bounding box
    shift_color = get_most_frequent_outside_color(input_np, min_r, min_c, max_r, max_c)

    # 5. Copy inner content if the box is large enough
    # Inner content region in input: rows min_r+1 to max_r-1, cols min_c+1 to max_c-1
    # Target region in output: rows 1 to height-2, cols 1 to width-2
    inner_content_exists = (max_r > min_r + 1) and (max_c > min_c + 1)
    inner_h, inner_w = 0, 0
    if inner_content_exists:
        inner_content = input_np[min_r + 1 : max_r, min_c + 1 : max_c]
        inner_h, inner_w = inner_content.shape
        # Place content starting at [1, 1] in the output grid
        if inner_h > 0 and inner_w > 0:
            # Ensure target region doesn't exceed output bounds (it shouldn't by definition)
             output_np[1 : 1 + inner_h, 1 : 1 + inner_w] = inner_content

    # 6. Identify objects within the copied inner content area of the output grid
    # The search region in output_np is [1, 1+inner_h) x [1, 1+inner_w)
    # Note: end indices are exclusive for slicing/range but inclusive for find_objects_in_region
    objects = find_objects_in_region(output_np, 1, 1 + inner_h, 1, 1 + inner_w)

    # 7. & 8. Determine positions for shifted pixels
    pixels_to_color = {} # Use dict {(r, c): color} to handle potential overlaps (last write wins, which is fine here)
    
    if shift_color != 0: # Only shift if a valid shift color was found
        for _, coords in objects:
            if not coords: continue
            
            for r, c in coords:
                # Calculate shift target coordinates
                targets = [
                    (r, c + 2), # Right shift
                    (r, c - 2)  # Left shift
                ]

                for tr, tc in targets:
                    # Check if target is within output bounds
                    if 0 <= tr < height and 0 <= tc < width:
                        # Check if target pixel is currently background (0)
                        # Also ensure the target is not one of the corners we'll set later
                        is_corner = (tr == 0 and tc == 0) or \
                                    (tr == 0 and tc == width - 1) or \
                                    (tr == height - 1 and tc == 0) or \
                                    (tr == height - 1 and tc == width - 1)
                                    
                        if output_np[tr, tc] == 0 and not is_corner:
                             # Store the target coordinate and the color to paint it
                             pixels_to_color[(tr, tc)] = shift_color


    # 9. Apply the shifts by coloring the marked pixels
    for (r, c), color in pixels_to_color.items():
        output_np[r, c] = color

    # 10. Set the four corners to yellow (4)
    output_np[0, 0] = 4
    if width > 1:
        output_np[0, width - 1] = 4
    if height > 1:
        output_np[height - 1, 0] = 4
    if height > 1 and width > 1:
        output_np[height - 1, width - 1] = 4
        
    # Convert back to list of lists for the required output format
    output_grid = output_np.tolist()

    return output_grid