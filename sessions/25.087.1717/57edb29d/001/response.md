```python
import numpy as np
from collections import Counter, deque

"""
Transformation Rule Description:
1. Identify the border color, which is consistently yellow (4) in the examples.
2. Find all connected components (objects) consisting of non-border colors within the input grid.
3. For each component found, determine if it is fully enclosed by the border color. An object is considered enclosed if every neighboring pixel of every pixel in the object is either part of the object itself or is the border color. Objects touching the grid edge are not considered enclosed.
4. For each enclosed object:
    a. Determine its bounding box (min_row, min_col, max_row, max_col).
    b. Identify its 'inner color', defined as the color of the pixel at the top-left corner of its bounding box (input_grid[min_row, min_col]).
    c. Extract the rectangular subgrid corresponding to the object's content, defined by its bounding box.
5. Count the occurrences of each 'inner color' among all identified enclosed objects.
6. Find the 'inner color' that occurs exactly once (the unique inner color).
7. The output grid is the extracted content (subgrid) of the object associated with this unique inner color.
8. If no unique inner color is found (e.g., no objects, no enclosed objects, or all enclosed objects have inner colors that appear multiple times), the transformation is undefined based on the examples (an error might be raised, or a default grid returned).
"""

def is_enclosed_by_border(grid, component_coords, border_color):
    """
    Checks if a component is fully enclosed by the border color.

    Args:
        grid (np.ndarray): The input grid.
        component_coords (set): A set of (row, col) tuples representing the component.
        border_color (int): The color value representing the border.

    Returns:
        bool: True if the component is enclosed, False otherwise.
    """
    height, width = grid.shape
    # If the component is empty, it cannot be enclosed in a meaningful way
    if not component_coords:
        return False
        
    for r, c in component_coords:
        # Check all 4 neighbors (up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            
            # Check if neighbor is within grid bounds
            if 0 <= nr < height and 0 <= nc < width:
                # If the neighbor is not part of the component itself...
                if (nr, nc) not in component_coords:
                    # ...it MUST be the border color for the component to be enclosed
                    if grid[nr, nc] != border_color:
                        return False
            else:
                # If a neighbor is outside the grid bounds, the component touches the edge
                # and is therefore not enclosed by the border color within the grid.
                return False
                
    # If all boundary checks passed for all coordinates in the component
    return True

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (np.ndarray): A 2D numpy array representing the input grid.

    Returns:
        np.ndarray: A 2D numpy array representing the output grid.
        Raises ValueError if a uniquely colored enclosed object cannot be found.
    """
    border_color = 4
    height, width = input_grid.shape
    visited = np.zeros_like(input_grid, dtype=bool)
    enclosed_objects = []

    # Iterate through each pixel to find starting points for components
    for r in range(height):
        for c in range(width):
            # Start BFS only if it's a non-border pixel and not visited yet
            if input_grid[r, c] != border_color and not visited[r, c]:
                component_coords = set()
                q = deque([(r, c)])
                visited[r, c] = True
                # Initialize bounding box with the starting pixel
                min_r, min_c, max_r, max_c = r, c, r, c

                # Perform BFS to find all connected non-border pixels
                while q:
                    curr_r, curr_c = q.popleft()
                    component_coords.add((curr_r, curr_c))
                    
                    # Update bounding box dynamically
                    min_r = min(min_r, curr_r)
                    min_c = min(min_c, curr_c)
                    max_r = max(max_r, curr_r)
                    max_c = max(max_c, curr_c)

                    # Explore neighbors
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc
                        
                        # Check neighbor validity: within bounds, not border, not visited
                        if 0 <= nr < height and 0 <= nc < width and \
                           input_grid[nr, nc] != border_color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))

                # After finding a component, check if it's enclosed by the border
                if is_enclosed_by_border(input_grid, component_coords, border_color):
                    # Determine the 'inner color' using the top-left pixel of the bounding box
                    inner_color = input_grid[min_r, min_c]
                    # Extract the content subgrid based on the bounding box
                    content = input_grid[min_r : max_r + 1, min_c : max_c + 1]
                    # Store the relevant information
                    enclosed_objects.append({'inner_color': inner_color, 'content': content})

    # Check if any enclosed objects were found
    if not enclosed_objects:
        # Handle the case where no objects are enclosed by the border
        # Depending on requirements, could return empty grid, None, or raise error
        raise ValueError("No objects enclosed by the border color were found.")

    # Count the frequency of each inner color among the enclosed objects
    inner_color_counts = Counter(obj['inner_color'] for obj in enclosed_objects)

    # Find the inner color that appears exactly once
    unique_inner_color = None
    unique_colors_found = []
    for color, count in inner_color_counts.items():
        if count == 1:
            unique_colors_found.append(color)
            
    # Check if exactly one unique color was found
    if len(unique_colors_found) == 1:
         unique_inner_color = unique_colors_found[0]
    elif len(unique_colors_found) == 0:
        # No unique color found (all counts > 1 or no objects)
         raise ValueError("Could not find a uniquely colored enclosed object.")
    else:
        # Multiple unique colors found - ambiguity not handled by observed rule
        raise ValueError(f"Ambiguous: Multiple uniquely colored objects found (colors: {unique_colors_found}).")


    # Retrieve and return the content of the object with the unique inner color
    for obj in enclosed_objects:
        if obj['inner_color'] == unique_inner_color:
            return obj['content']

    # This point should not be reached if logic is correct and a unique object exists
    raise RuntimeError("Logic error: Failed to retrieve the object content for the unique color.")
```