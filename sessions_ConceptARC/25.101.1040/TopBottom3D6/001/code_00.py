"""
Identifies all unique non-background colors in the input grid.
For each color, finds and counts the number of distinct contiguous objects (using 8-way adjacency).
Selects the color(s) with the maximum number of objects.
If there's a tie in the object count, calculates the bounding box encompassing all pixels of each tied color.
Selects the color among the tied ones whose bounding box has the largest area (height * width).
Determines the bounding box of the finally selected color.
Creates an output grid with the dimensions of this final bounding box, filled entirely with the selected color.
"""

import numpy as np
from collections import deque

def _find_objects(grid: np.ndarray, color: int) -> list[set[tuple[int, int]]]:
    """
    Finds all distinct contiguous objects of a given color in the grid.
    Uses Breadth-First Search (BFS) with 8-way adjacency.

    Args:
        grid: The input grid as a NumPy array.
        color: The target color to find objects for.

    Returns:
        A list of sets, where each set contains the (row, col) coordinates
        of the pixels belonging to one object.
    """
    rows, cols = grid.shape
    visited = set()
    objects = []
    
    # Define 8-way adjacent neighbor offsets
    neighbors = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1), (1, 0), (1, 1),
    ]

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and (r, c) not in visited:
                # Start BFS for a new object
                current_object = set()
                q = deque([(r, c)])
                visited.add((r, c))
                current_object.add((r, c))

                while q:
                    row, col = q.popleft()
                    
                    # Explore neighbors
                    for dr, dc in neighbors:
                        nr, nc = row + dr, col + dc
                        
                        # Check bounds and if the neighbor is the correct color and not visited
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == color and (nr, nc) not in visited:
                            visited.add((nr, nc))
                            current_object.add((nr, nc))
                            q.append((nr, nc))
                            
                objects.append(current_object)
                
    return objects

def _get_bounding_box(grid: np.ndarray, color: int) -> tuple[int, int, int, int, int, int] | None:
    """
    Calculates the bounding box enclosing all pixels of a given color.

    Args:
        grid: The input grid as a NumPy array.
        color: The target color.

    Returns:
        A tuple (min_row, min_col, max_row, max_col, height, width) 
        or None if the color is not present.
    """
    coords = np.argwhere(grid == color)
    if coords.size == 0:
        return None
        
    min_row, min_col = coords.min(axis=0)
    max_row, max_col = coords.max(axis=0)
    
    height = max_row - min_row + 1
    width = max_col - min_col + 1
    
    return min_row, min_col, max_row, max_col, height, width

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid based on object count and bounding box area.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the output grid.
    """
    grid = np.array(input_grid, dtype=int)
    
    # 1. Identify unique non-background colors
    unique_colors = np.unique(grid[grid != 0]) # Exclude background color 0 (white)
    
    if unique_colors.size == 0:
        # Handle edge case: input grid is all background or empty
        return [] 
        
    # 2. & 3. Find objects and count for each color
    object_counts = {}
    for color in unique_colors:
        objects = _find_objects(grid, color)
        object_counts[color] = len(objects)

    # 4. Determine max object count and candidate colors
    if not object_counts: # Should not happen if unique_colors > 0, but for safety
        return []
    max_count = max(object_counts.values())
    candidate_colors = [color for color, count in object_counts.items() if count == max_count]
    
    selected_color = -1 # Initialize

    # 5. Check if only one candidate
    if len(candidate_colors) == 1:
        selected_color = candidate_colors[0]
    else:
        # 6. Tie-breaker: Largest bounding box area
        max_area = -1
        best_color = -1
        
        for color in candidate_colors:
            bbox = _get_bounding_box(grid, color)
            if bbox:
                _, _, _, _, height, width = bbox
                area = height * width
                # print(f"Color {color}: Area {area}") # Debug print
                if area > max_area:
                    max_area = area
                    best_color = color
                # If areas are equal, the first one encountered with max area is kept.
                # Could add secondary tie-breaker (e.g., lowest color index) if needed.
                
        selected_color = best_color

    if selected_color == -1:
         # Should not happen if there were unique colors, but handle defensively
        return [] 

    # 7. Get final bounding box for the selected color
    final_bbox = _get_bounding_box(grid, selected_color)
    if not final_bbox:
        # Should not happen if the color was selected, but handle defensively
        return []
        
    _, _, _, _, output_height, output_width = final_bbox
    
    # 8. & 9. Create and fill the output grid
    output_grid_np = np.full((output_height, output_width), selected_color, dtype=int)
    
    return output_grid_np.tolist()
