import numpy as np
from collections import Counter, deque

"""
Identifies distinct objects in the input grid, where objects consist of a border of one color and a center of another color.
It then counts the frequency of each center color across all identified objects.
The final output is the single digit representing the color that appears most frequently as a center color.
"""

def find_objects(grid: np.ndarray) -> list[list[tuple[int, int]]]:
    """
    Finds connected components (objects) of non-background pixels using BFS.

    Args:
        grid: A numpy array representing the input grid.

    Returns:
        A list of objects, where each object is a list of (row, col) tuples.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    
    for r in range(rows):
        for c in range(cols):
            # If we find a non-background pixel that hasn't been visited
            if grid[r, c] != 0 and not visited[r, c]:
                obj_coords = []
                q = deque([(r, c)])
                visited[r, c] = True
                
                while q:
                    row, col = q.popleft()
                    obj_coords.append((row, col))
                    
                    # Check 4 neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        
                        # Check bounds and if neighbor is part of the object and not visited
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] != 0 and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            
                if obj_coords:
                    objects.append(obj_coords)
                    
    return objects

def get_center_color(grid: np.ndarray, obj_coords: list[tuple[int, int]]) -> int | None:
    """
    Determines the center color of an object defined by its coordinates.
    Assumes object has a border and a center color.

    Args:
        grid: The numpy array representing the input grid.
        obj_coords: A list of (row, col) tuples for the object.

    Returns:
        The center color index, or None if not found or ambiguous.
    """
    if not obj_coords:
        return None

    colors_in_object = Counter()
    for r, c in obj_coords:
        colors_in_object[grid[r, c]] += 1

    # Filter out potential background color if accidentally included (shouldn't happen with find_objects)
    if 0 in colors_in_object:
        del colors_in_object[0]

    # Expecting exactly two colors: border and center
    if len(colors_in_object) != 2:
      # If only one color, it might be a solid block, not border/center
      # Or it might be more complex than the examples show
      # Based on examples, we expect exactly two colors per object.
      return None 
      
    # The less frequent color is assumed to be the center color
    # (or equally frequent if center area == border area, pick one)
    # Sort by count, the first element is the least frequent (center)
    sorted_colors = sorted(colors_in_object.items(), key=lambda item: item[1])
    
    return sorted_colors[0][0]


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by finding the most frequent center color among objects.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A 1x1 grid containing the most frequent center color.
    """
    
    # Convert input to numpy array for easier processing
    grid = np.array(input_grid, dtype=int)
    
    # Find all distinct objects (connected components of non-background colors)
    objects = find_objects(grid)
    
    # Identify the center color for each valid object
    center_colors = []
    for obj_coords in objects:
        center_color = get_center_color(grid, obj_coords)
        if center_color is not None:
            center_colors.append(center_color)
            
    # Count the frequency of each center color
    if not center_colors:
      # Handle cases where no valid objects with centers were found
      # Based on examples, this shouldn't happen. Defaulting to 0 maybe?
      # Let's assume valid input guarantees at least one object.
      # If the counter is empty, most_common will raise an error.
      # Returning an empty grid or a default might be options.
      # For now, let it error if no center colors found, indicating unexpected input.
      # Or return [[0]] as a default? Let's return the most frequent color or default to 0 if none.
       return [[0]] # Default if no center colors found


    center_color_counts = Counter(center_colors)
    
    # Find the color with the highest frequency
    # If there's a tie, most_common returns one of the most frequent ones.
    # The problem description doesn't specify tie-breaking, assume any top one is fine.
    most_frequent_center_color = center_color_counts.most_common(1)[0][0]
    
    # The output is a 1x1 grid containing this color
    output_grid = [[most_frequent_center_color]]
    
    return output_grid