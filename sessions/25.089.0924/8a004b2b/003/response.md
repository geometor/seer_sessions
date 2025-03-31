```python
import numpy as np
from collections import Counter

"""
Identify the bounding box defined by yellow (4) pixels in the input grid.
Create an output grid based on the bounding box size.
Copy the content strictly inside the input bounding box to the interior of the output grid (offset by 1 row and 1 column).
Find the most frequent non-background color present *outside* the bounding box in the input grid.
Identify distinct objects within the copied content in the output grid.
For each object, create copies shifted two columns to the left and two columns to the right, using the determined most frequent outside color. These shifted copies only overwrite background (0) pixels in the output grid.
Set the four corners of the output grid to yellow (4).
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
    Finds the most frequent non-background color outside the bounding box.
    Returns the color value or 0 if no non-background colors are outside.
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
    for color, count in color_counts.items():
        if count > max_freq:
            max_freq = count

    # Find all colors with the max frequency
    most_frequent_colors = [color for color, count in color_counts.items() if count == max_freq]

    # Tie-breaking: return the smallest color index
    return min(most_frequent_colors)


def find_objects_in_region(grid, start_row, end_row, start_col, end_col):
    """
    Finds contiguous objects of the same color within a specified region.
    Returns a list of objects, where each object is a tuple: (color, set_of_coordinates).
    """
    objects = []
    visited = np.zeros_like(grid, dtype=bool)
    rows, cols = grid.shape

    for r in range(start_row, end_row):
        for c in range(start_col, end_col):
            if grid[r, c] != 0 and not visited[r, c]:
                color = grid[r, c]
                obj_coords = set()
                q = [(r, c)]
                visited[r, c] = True
                
                while q:
                    row, col = q.pop(0)
                    # Check if still within the specified search region
                    if not (start_row <= row < end_row and start_col <= col < end_col):
                        continue # Should not happen if starting point is valid, but good check

                    obj_coords.add((row, col))

                    # Check neighbors (4-connectivity)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        # Check bounds, region, color match, and not visited
                        if (start_row <= nr < end_row and
                            start_col <= nc < end_col and
                            grid[nr, nc] == color and
                            not visited[nr, nc]):
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            
                if obj_coords:
                     objects.append((color, obj_coords))
                     
    return objects


def transform(input_grid):
    input_np = np.array(input_grid, dtype=int)
    rows_in, cols_in = input_np.shape

    # 1. Find bounding box using yellow pixels
    bbox = find_bounding_box(input_np, 4)
    if bbox is None:
         # If no yellow markers, maybe return original grid or handle error
         return input_grid 
    min_r, min_c, max_r, max_c = bbox

    # 2. Calculate output grid dimensions
    height = max_r - min_r + 1
    width = max_c - min_c + 1

    # Ensure valid dimensions
    if height <= 0 or width <= 0:
        return [] # Or raise error

    # 3. Create output grid initialized with 0s
    output_np = np.zeros((height, width), dtype=int)

    # 4. Copy inner content if the box is large enough
    inner_content_exists = (max_r > min_r + 1) and (max_c > min_c + 1)
    if inner_content_exists:
        inner_content = input_np[min_r + 1 : max_r, min_c + 1 : max_c]
        inner_h, inner_w = inner_content.shape
        # Place content starting at [1, 1] in the output grid
        if inner_h > 0 and inner_w > 0:
            output_np[1 : 1 + inner_h, 1 : 1 + inner_w] = inner_content

    # 5 & 6. Find the most frequent color outside the bounding box
    shift_color = get_most_frequent_outside_color(input_np, min_r, min_c, max_r, max_c)
    
    # 7. Find objects within the copied inner content area of the output grid
    # The search region in output_np is [1, height-1) x [1, width-1)
    objects = find_objects_in_region(output_np, 1, height - 1, 1, width - 1)

    # 8. For each object, attempt left and right shifts using shift_color
    for _, coords in objects:
        if not coords: continue
        # Find top-left corner of the object's bounding box for relative calculations
        obj_min_r = min(r for r, c in coords)
        obj_min_c = min(c for r, c in coords)

        # Iterate through each pixel of the object
        for r, c in coords:
            rel_r = r - obj_min_r
            rel_c = c - obj_min_c

            # Calculate shift target coordinates
            targets = [
                (obj_min_r + rel_r, obj_min_c + rel_c + 2), # Right shift
                (obj_min_r + rel_r, obj_min_c + rel_c - 2)  # Left shift
            ]

            for tr, tc in targets:
                # Check if target is within output bounds
                if 0 <= tr < height and 0 <= tc < width:
                    # Check if target pixel is currently background (0)
                    if output_np[tr, tc] == 0:
                        output_np[tr, tc] = shift_color

    # 9. Set the four corners to yellow (4)
    output_np[0, 0] = 4
    if width > 1:
        output_np[0, width - 1] = 4
    if height > 1:
        output_np[height - 1, 0] = 4
    if height > 1 and width > 1:
        output_np[height - 1, width - 1] = 4
        
    # Convert back to list of lists
    output_grid = output_np.tolist()

    return output_grid
```