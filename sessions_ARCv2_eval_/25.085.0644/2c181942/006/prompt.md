
Previous Code:
```python
import numpy as np

"""
Applies gravity to whole objects in the input grid.

Identifies connected objects of non-background colors (anything other than azure - 8) 
using 8-way connectivity. Each object falls downwards as a single unit, maintaining 
its shape. An object stops falling when any part of its bottom edge reaches the 
bottom of the grid or lands on top of any part of another object that has already 
settled in the output grid. Objects do not move horizontally. The relative vertical 
order of pixels within an object is preserved, and the relative horizontal positions 
of objects are preserved. The output grid is initially filled with the background 
color (azure - 8), and the objects are drawn in their final settled positions.
"""

def find_components_bfs(grid, background_color):
    """
    Finds connected components (objects) of non-background colors using 8-way 
    connectivity via Breadth-First Search (BFS).

    Args:
        grid (np.ndarray): The input grid.
        background_color (int): The color considered as background.

    Returns:
        list: A list of dictionaries, where each dictionary represents an object
              and contains 'color', 'coords' (a set of (r, c) tuples of absolute
              coordinates), 'rel_coords' (a set of (r, c) tuples relative to the
              bounding box top-left), and 'bbox' (min_r, min_c, max_r, max_c).
    """
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    
    # Iterate through each cell to find starting points of objects
    for r in range(height):
        for c in range(width):
            # If the cell is not background and hasn't been visited yet, start BFS
            if grid[r, c] != background_color and not visited[r, c]:
                obj_color = grid[r, c]
                coords = set() # Stores absolute coordinates of the object's pixels
                q = [(r, c)] # Queue for BFS
                visited[r, c] = True
                min_r, max_r = r, r # Bounding box limits
                min_c, max_c = c, c

                # Perform BFS
                while q:
                    row, col = q.pop(0)
                    coords.add((row, col))
                    # Update bounding box
                    min_r = min(min_r, row)
                    max_r = max(max_r, row)
                    min_c = min(min_c, col)
                    max_c = max(max_c, col)

                    # Check 8 neighbors (including diagonals)
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue # Skip self
                            nr, nc = row + dr, col + dc
                            
                            # Check if neighbor is within grid bounds
                            if 0 <= nr < height and 0 <= nc < width:
                                # Check if neighbor is part of the same object and not visited
                                if not visited[nr, nc] and grid[nr, nc] == obj_color:
                                    visited[nr, nc] = True
                                    q.append((nr, nc))
                
                # Calculate coordinates relative to the object's bounding box top-left
                rel_coords = set((cr - min_r, cc - min_c) for cr, cc in coords)
                
                # Store the found object's properties
                objects.append({
                    'color': obj_color,
                    'coords': coords, # Absolute coordinates in the original grid
                    'rel_coords': rel_coords, # Coordinates relative to bbox top-left
                    'bbox': (min_r, min_c, max_r, max_c) # Bounding box: top, left, bottom, right
                })
    return objects


def transform(input_grid):
    """
    Applies gravity simulation to non-background objects in the grid.

    Args:
        input_grid (np.ndarray): A 2D numpy array representing the input grid.

    Returns:
        np.ndarray: A 2D numpy array representing the transformed grid with objects settled by gravity.
    """
    background_color = 8
    height, width = input_grid.shape

    # 1. Initialize the output grid with the background color
    output_grid = np.full((height, width), background_color, dtype=int)

    # 2. Identify all distinct non-background objects in the input grid
    objects = find_components_bfs(input_grid, background_color)

    # 3. Sort objects primarily by their bottom edge (max_r), then top edge (min_r).
    # This helps in processing objects that should settle lower first, ensuring
    # correct stacking order.
    objects.sort(key=lambda obj: (obj['bbox'][2], obj['bbox'][0]))

    # 4. Process each object to determine its final position after falling
    for obj in objects:
        color = obj['color']
        rel_coords = obj['rel_coords']
        min_r, min_c, _, _ = obj['bbox'] # Original top-left position

        # Determine the maximum distance the object can fall vertically
        fall_distance = 0
        while True:
            # Assume it can fall one step further in the next iteration
            can_fall_further = True
            # Calculate the potential vertical offset for the *next* step down
            next_r_offset = fall_distance + 1

            # Check collision for every pixel of the object at the potential new position
            for rel_r, rel_c in rel_coords:
                # Calculate the target row and column in the grid for this pixel
                target_r = min_r + rel_r + next_r_offset
                target_c = min_c + rel_c # Column remains the same

                # Check 1: Collision with grid bottom
                if target_r >= height:
                    can_fall_further = False
                    break # Cannot fall further, hit the bottom

                # Check 2: Collision with another object already settled in the output grid
                if output_grid[target_r, target_c] != background_color:
                    can_fall_further = False
                    break # Cannot fall further, hit another settled object

            # If no collision was detected for any pixel at the next step down
            if can_fall_further:
                fall_distance += 1 # Increment the fall distance, try falling further
            else:
                # Collision detected or bottom reached, stop checking further fall.
                # The current 'fall_distance' is the maximum possible.
                break

        # 5. Calculate the final top-left position of the object after falling
        final_r = min_r + fall_distance
        final_c = min_c # Object only moves vertically

        # 6. Place the object onto the output grid at its final settled position
        for rel_r, rel_c in rel_coords:
            # Draw each pixel of the object using its relative coordinates and final position
            output_grid[final_r + rel_r, final_c + rel_c] = color

    # 7. Return the final grid with all objects settled
    return output_grid
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 2 2 2 2 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 2 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 6 6 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 3 8 8 2 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 3 8 8 2 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 1 1 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 4 4 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 4 4 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 4 4 4 4 8 8 8 8
8 8 8 8 3 3 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 3 3 3 3 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 3 8 8 3 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
```
Expected Output:
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 3 3 8 8 6 6 8 8 2 8 8 8 8 8 8 8 8 8
8 8 8 3 3 3 8 8 2 2 2 8 8 8 8 8 8 8 8 8
8 8 8 3 3 3 8 8 2 2 2 8 8 8 8 8 8 8 8 8
8 8 3 3 8 8 1 1 8 8 2 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
```
Transformed Output:
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 3 3 8 8 8 8 8 8 8 4 4 8 8 8 8 8
8 8 8 3 3 3 3 8 8 8 8 8 8 4 4 8 8 8 8 8
8 8 8 3 8 8 3 8 8 8 8 8 4 4 4 4 8 8 8 8
8 8 8 8 8 3 1 1 2 8 8 8 8 2 2 2 2 8 8 8
8 8 8 8 8 3 6 6 2 8 8 8 8 8 2 2 8 8 8 8
```
Match: False
Pixels Off: 52
Size Correct: True
Color Palette Correct: False
Color Count Correct: False
Score: 45.217391304347814

## Example 2:
Input:
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 3 3 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 3 8 8 3 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 3 3 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 1 8 8 2 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 1 8 8 2 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 4 4 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 1 1 1 1 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 1 1 1 1 8 8 8 8 8 8 8 8 8 2 8 8 8 8 8 8
8 8 1 1 8 8 8 8 8 8 8 8 2 2 2 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 2 2 2 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
```
Expected Output:
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 3 8 8 3 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 3 3 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 1 1 8 8 3 3 8 8 8 2 8 8 8 8 8 8 8 8
8 8 8 1 1 1 1 8 8 2 2 2 2 8 8 8 8 8 8 8 8
8 8 8 1 1 1 1 8 8 2 2 2 2 8 8 8 8 8 8 8 8
8 8 8 1 1 8 8 4 4 8 8 8 2 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
```
Transformed Output:
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 8 8 8 8 8 8
8 1 1 1 1 8 8 8 8 8 8 8 2 2 2 8 8 8 8 8 8
8 1 1 1 1 8 1 4 4 2 8 8 2 2 2 8 3 3 8 8 8
8 8 1 1 8 8 1 3 3 2 8 8 8 8 2 3 8 8 3 8 8
```
Match: False
Pixels Off: 60
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 15.873015873015873

## Example 3:
Input:
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 2 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 3 3 8 8 8 8
8 8 8 2 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 3 3 8 8 8 8
8 8 2 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 1 1 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 2 8 8 7 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 2 8 8 7 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 3 3 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 7 8 8 7 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 7 7 7 7 8 8 8 8 8 8 8 8 8 8 8 8 8 1 1 1 1 8 8 8
8 8 7 7 8 8 8 8 8 8 8 8 8 8 8 8 8 8 1 1 1 1 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
```
Expected Output:
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 1 1 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 1 1 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 1 1 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 1 1 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 2 8 8 8 1 1 8 8 7 7 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 2 2 2 8 8 7 7 7 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 2 2 2 8 8 7 7 7 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 2 8 8 8 3 3 8 8 7 7 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 3 3 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 3 3 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
```
Transformed Output:
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 7 8 8 7 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 7 7 7 7 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 7 7 8 8 8 8 8 8 8 8 8 8 8 8 8 8 1 1 1 1 8 8 8
8 8 8 2 2 8 8 8 8 8 8 8 8 8 8 8 8 8 1 1 1 1 8 8 8
8 8 8 2 2 8 8 8 8 8 8 2 3 3 7 8 8 8 8 3 3 8 8 8 8
8 8 2 8 8 2 8 8 8 8 8 2 1 1 7 8 8 8 8 3 3 8 8 8 8
```
Match: False
Pixels Off: 68
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 13.599999999999994
