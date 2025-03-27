"""
Determine the most frequent color in the input grid; this is the background_color.
Identify all distinct contiguous objects formed by pixels that are not the background_color. 
Treat each contiguous block of a single non-background color as a separate object.
For each object found, record its color, the total count of its pixels, and the coordinates (row, column) of its top-most, left-most pixel.
Sort these objects based first on the row coordinate of their top-most, left-most pixel (ascending), and then by the column coordinate (ascending) as a tie-breaker.
Initialize an empty list to store the output colors.
Iterate through the sorted objects. For each object, append its color to the output list a number of times equal to its pixel count.
Create the final output grid as a single column containing the colors from the generated list, in order.
"""

import numpy as np
from collections import Counter, deque

def find_background_color(grid):
    """Finds the most frequent color in the grid."""
    flat_grid = grid.flatten()
    counts = Counter(flat_grid)
    # Assume the most frequent color is the background
    # Handle potential ties by just picking one (usually the first encountered)
    background_color = counts.most_common(1)[0][0]
    return background_color

def find_objects(grid, background_color):
    """Finds all contiguous foreground objects in the grid."""
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            # Check if it's a foreground pixel and not visited yet
            if color != background_color and not visited[r, c]:
                obj_color = color
                pixels = []
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, min_c = r, c # Track top-left pixel

                while q:
                    row, col = q.popleft()
                    pixels.append((row, col))
                    
                    # Update top-left pixel tracker
                    if row < min_r:
                        min_r, min_c = row, col
                    elif row == min_r and col < min_c:
                        min_c = col

                    # Explore neighbors (4-directional)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        # Check bounds, color match, and visited status
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           not visited[nr, nc] and grid[nr, nc] == obj_color:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                
                # Store object details
                objects.append({
                    'color': obj_color,
                    'pixel_count': len(pixels),
                    'top_left': (min_r, min_c)
                })
    
    return objects

def transform(input_grid):
    """
    Transforms the input grid by extracting foreground object pixels into a single column,
    ordered by the object's top-left position.
    """
    # Convert input list of lists to numpy array
    grid = np.array(input_grid, dtype=int)
    
    # 1. Determine the background_color.
    background_color = find_background_color(grid)
    
    # 2. Identify all distinct contiguous foreground objects.
    # 3. Record color, pixel count, and top-left pixel for each object.
    objects = find_objects(grid, background_color)
    
    # 4. Sort objects by top-left position (row first, then column).
    objects.sort(key=lambda obj: (obj['top_left'][0], obj['top_left'][1]))
    
    # 5. Initialize an empty list for output colors.
    output_colors = []
    
    # 6. Iterate through sorted objects and append colors.
    for obj in objects:
        output_colors.extend([obj['color']] * obj['pixel_count'])
        
    # 7. Create the final output grid (single column).
    # Check if any objects were found
    if not output_colors:
        # If no foreground objects, return an empty 0x1 grid or handle as needed
        # For ARC, maybe return an empty grid of appropriate shape if specified,
        # or maybe a 1x1 grid of background color? 
        # Based on examples, seems like if there are objects, output has rows.
        # If no objects, the output might be empty or 0x0. Let's return a 0x1 array.
        output_grid = np.empty((0, 1), dtype=int) 
    else:
        output_grid = np.array(output_colors, dtype=int).reshape(-1, 1)

    return output_grid.tolist() # Return as list of lists per ARC standard