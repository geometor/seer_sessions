import numpy as np
from collections import defaultdict, deque

"""
Identifies the largest contiguous object of color gray (5) in the input grid.
Identifies all other non-background (non-0) pixels as source pixels.
Calculates the minimum Manhattan distance from each unique source pixel color to the gray object.
Determines the replacement color by finding the source color(s) with the overall minimum distance.
If multiple colors share the minimum distance, the one with the highest numerical value is chosen.
Creates an output grid containing only the original gray object's shape, but colored with the determined replacement color. All other pixels are background (0).
"""

def find_objects(grid, ignore_color=0):
    """
    Finds all contiguous objects of the same color in the grid.

    Args:
        grid (np.array): The input grid.
        ignore_color (int): The color to treat as background/ignore.

    Returns:
        list: A list of tuples, where each tuple is (color, set_of_coords).
              Returns an empty list if the grid is empty.
    """
    if grid.size == 0:
        return []
    height, width = grid.shape
    visited = set()
    objects = []
    for r in range(height):
        for c in range(width):
            if (r, c) not in visited and grid[r, c] != ignore_color:
                color = grid[r, c]
                coords = set()
                queue = deque([(r, c)])
                visited.add((r, c))
                current_object_coords = set()

                while queue:
                    row, col = queue.popleft()
                    current_object_coords.add((row, col))

                    # Check neighbors (8-directional, including diagonals)
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue
                            nr, nc = row + dr, col + dc
                            if 0 <= nr < height and 0 <= nc < width and \
                               (nr, nc) not in visited and grid[nr, nc] == color:
                                visited.add((nr, nc))
                                queue.append((nr, nc))
                
                if current_object_coords:
                     objects.append((color, current_object_coords))
                     
    return objects

def manhattan_distance(p1, p2):
    """Calculates Manhattan distance between two points (r, c)."""
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def transform(input_grid):
    """
    Transforms the input grid according to the described rule.
    
    1. Finds the target gray (5) object.
    2. Finds source pixels (non-background, non-target).
    3. Calculates min distances from source colors to target object.
    4. Determines replacement color based on min distance (highest value tie-breaker).
    5. Creates output grid with target shape filled with replacement color.
    """
    input_np = np.array(input_grid, dtype=int)
    if input_np.size == 0:
        return []
        
    height, width = input_np.shape
    background_color = 0
    target_object_input_color = 5
    
    # Find all non-background objects
    objects = find_objects(input_np, ignore_color=background_color)

    # Identify the target object (must be color 5)
    # If multiple color 5 objects exist, choose the largest one.
    target_object_coords = set()
    target_candidates = []
    for color, coords in objects:
        if color == target_object_input_color:
            target_candidates.append(coords)

    if not target_candidates:
        # No gray object found, return an empty grid
        return np.zeros_like(input_np).tolist()

    # Select the largest gray object if multiple exist (unlikely based on examples)
    target_object_coords = max(target_candidates, key=len)

    # Identify source pixels (not background, not target object)
    source_pixels = []
    for r in range(height):
        for c in range(width):
            color = input_np[r, c]
            if color != background_color and (r, c) not in target_object_coords:
                source_pixels.append({'r': r, 'c': c, 'color': color})

    if not source_pixels:
         # No source pixels found, the rule cannot be applied. Return empty grid.
        return np.zeros_like(input_np).tolist()

    # Calculate minimum distances from each source color to the target object
    min_distances_by_color = defaultdict(lambda: float('inf'))
    unique_source_colors = sorted(list(set(p['color'] for p in source_pixels)), reverse=True) # Sort high to low for potential tie-break pre-computation, though direct max() is used later

    for color in unique_source_colors:
        min_dist_for_this_color = float('inf')
        source_pixels_of_this_color = [p for p in source_pixels if p['color'] == color]
        
        # Iterate through source pixels of the current color
        for sp in source_pixels_of_this_color:
            sp_coord = (sp['r'], sp['c'])
            min_dist_for_sp = float('inf')
            # Find the closest point in the target object to this source pixel
            for tp_coord in target_object_coords:
                 dist = manhattan_distance(sp_coord, tp_coord)
                 min_dist_for_sp = min(min_dist_for_sp, dist)
                 # Optimization: if distance is 1, this is the minimum possible for this sp
                 if min_dist_for_sp == 1:
                     break 
            # Update the minimum distance found *for this color*
            min_dist_for_this_color = min(min_dist_for_this_color, min_dist_for_sp)
            # Optimization: if the minimum distance for this color is 1, no need to check other sp's of this color
            if min_dist_for_this_color == 1:
                 break

        min_distances_by_color[color] = min_dist_for_this_color

    # Determine the winning replacement color
    if not min_distances_by_color:
        # Should not happen if source_pixels exist, but as a safeguard
        return np.zeros_like(input_np).tolist()

    # Find the minimum distance achieved across all colors
    overall_min_distance = min(min_distances_by_color.values())

    # Find all colors that achieved this minimum distance
    candidate_colors = [
        color for color, dist in min_distances_by_color.items()
        if dist == overall_min_distance
    ]

    # Apply tie-breaking rule: select the color with the highest numerical value
    replacement_color = max(candidate_colors)

    # Construct the output grid
    output_np = np.full_like(input_np, background_color)
    for r, c in target_object_coords:
         # Ensure coordinates are within bounds (should be, but safety check)
         if 0 <= r < height and 0 <= c < width:
             output_np[r, c] = replacement_color

    return output_np.tolist()