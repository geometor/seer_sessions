```python
import numpy as np
from collections import Counter

"""
Identifies a primary background color, a single dominant horizontal or vertical separator line, and one or more 'target' shapes of a distinct color.
Based on the separator's orientation:
- If vertical: Fills the rectangular area between each target shape and the separator line (on the side facing the separator) with the separator's color. The fill occurs within the row span of the target shape. Only pixels matching the original background color are changed.
- If horizontal: Fills the rectangular area above the separator line, within the column span of each target shape, with the target shapes' color. Fills the rectangular area below the separator line but above the target shape, within the column span of the target shape, with the separator's color. Only pixels matching the original background color are changed.
"""

def find_background_color(grid):
    """Finds the most frequent color in the grid."""
    counts = Counter(grid.flatten())
    # Handle empty grid case if necessary, though ARC constraints likely prevent it
    if not counts:
        return 0 # Default to black/white if grid is empty
    # Find the color with the maximum count
    background_color = counts.most_common(1)[0][0]
    return background_color

def find_separator(grid, background_color):
    """
    Finds a dominant horizontal or vertical line that is not the background color.
    Returns (orientation, index, color) or None.
    """
    height, width = grid.shape
    separator = None

    # Check for horizontal lines
    for r in range(height):
        row = grid[r, :]
        counts = Counter(c for c in row if c != background_color)
        if len(counts) == 1:
            line_color = list(counts.keys())[0]
            line_count = counts[line_color]
            # Heuristic: Line covers most of the width
            if line_count > width * 0.7: # Threshold for dominance
                 # Prioritize longer lines if multiple candidates exist
                if separator is None or line_count > separator[3]:
                     separator = ('horizontal', r, line_color, line_count)


    # Check for vertical lines
    for c in range(width):
        col = grid[:, c]
        counts = Counter(r for r in col if r != background_color)
        if len(counts) == 1:
            line_color = list(counts.keys())[0]
            line_count = counts[line_color]
            # Heuristic: Line covers most of the height
            if line_count > height * 0.7: # Threshold for dominance
                 # Prioritize longer lines, consider vertical preference if lengths equal?
                 # If a horizontal separator was already found, compare lengths
                 if separator is None or line_count > separator[3] or (line_count == separator[3] and separator[0] == 'horizontal'):
                    separator = ('vertical', c, line_color, line_count)

    return separator[:3] if separator else None

def find_objects(grid, target_color):
    """
    Finds all contiguous objects of a specific color using BFS.
    Returns a list of bounding boxes [(min_r, max_r, min_c, max_c), ...].
    """
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects_bboxes = []
    
    for r in range(height):
        for c in range(width):
            if grid[r, c] == target_color and not visited[r, c]:
                # Start BFS for a new object
                q = [(r, c)]
                visited[r, c] = True
                object_pixels = []
                min_r, max_r, min_c, max_c = r, r, c, c
                
                head = 0
                while head < len(q):
                    row, col = q[head]
                    head += 1
                    object_pixels.append((row, col))
                    min_r = min(min_r, row)
                    max_r = max(max_r, row)
                    min_c = min(min_c, col)
                    max_c = max(max_c, col)
                    
                    # Check 4 neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < height and 0 <= nc < width and \
                           grid[nr, nc] == target_color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            
                if object_pixels: # Should always be true here
                    objects_bboxes.append((min_r, max_r, min_c, max_c))
                    
    return objects_bboxes

def transform(input_grid):
    """
    Applies the transformation rule based on separator and target shapes.
    """
    input_grid_np = np.array(input_grid, dtype=int)
    output_grid = np.copy(input_grid_np)
    height, width = input_grid_np.shape

    # 1. Identify background color
    background_color = find_background_color(input_grid_np)

    # 2. Locate the separator line
    separator_info = find_separator(input_grid_np, background_color)
    if not separator_info:
        # If no clear separator found, return the original grid
        return output_grid.tolist() 
    
    orientation, separator_index, separator_color = separator_info

    # 3. Identify target color and target objects
    target_color = -1 # Placeholder
    potential_target_colors = set(input_grid_np.flatten()) - {background_color, separator_color}
    if not potential_target_colors:
         # No target colors found, return original
         return output_grid.tolist()
    # Assume the first non-background, non-separator color encountered is the target color
    # A more robust approach might analyze object sizes or shapes if multiple candidates exist.
    # For these examples, taking the first one seems sufficient.
    # Let's find objects of the first potential target color.
    
    target_color = list(potential_target_colors)[0] # Choose one potential color
    target_bboxes = find_objects(input_grid_np, target_color)

    # If no objects of the chosen color, try another potential color?
    # For now, assume the first potential color is the correct one based on examples.
    if not target_bboxes:
        # Check if there are other potential target colors
        if len(potential_target_colors) > 1:
             target_color = list(potential_target_colors)[1]
             target_bboxes = find_objects(input_grid_np, target_color)
             if not target_bboxes:
                 return output_grid.tolist() # Still no targets, return original
        else:
             return output_grid.tolist() # No targets found at all

    # 4. Apply fill logic based on orientation
    if orientation == 'vertical':
        sep_c = separator_index
        for min_r, max_r, min_c, max_c in target_bboxes:
            if max_c < sep_c: # Target is left of separator
                fill_min_c = max_c + 1
                fill_max_c = sep_c - 1
            elif min_c > sep_c: # Target is right of separator
                fill_min_c = sep_c + 1
                fill_max_c = min_c - 1
            else: # Target overlaps or touches separator - skip filling?
                continue 

            # Fill the region
            for r in range(min_r, max_r + 1):
                for c in range(fill_min_c, fill_max_c + 1):
                    # Ensure indices are valid (though ranges should be correct)
                    if 0 <= r < height and 0 <= c < width:
                        # Only change background pixels
                        if output_grid[r, c] == background_color:
                            output_grid[r, c] = separator_color

    elif orientation == 'horizontal':
        sep_r = separator_index
        for min_r, max_r, min_c, max_c in target_bboxes:
            # Fill above separator with target color
            fill_min_r_above = 0
            fill_max_r_above = sep_r - 1
            for r in range(fill_min_r_above, fill_max_r_above + 1):
                 for c in range(min_c, max_c + 1):
                     if 0 <= r < height and 0 <= c < width:
                         if output_grid[r, c] == background_color:
                             output_grid[r, c] = target_color

            # Fill below separator (but above target) with separator color
            fill_min_r_below = sep_r + 1
            fill_max_r_below = min_r - 1 # Fill up to the row just before the target starts
            for r in range(fill_min_r_below, fill_max_r_below + 1):
                 for c in range(min_c, max_c + 1):
                      if 0 <= r < height and 0 <= c < width:
                         if output_grid[r, c] == background_color:
                             output_grid[r, c] = separator_color

    # 5. Return the modified grid
    return output_grid.tolist()
```