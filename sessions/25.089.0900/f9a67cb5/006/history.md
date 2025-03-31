
## train_1

**input:**
```
0 0 0 0 0 0 0 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
8 8 8 8 8 0 8 8 8 0 8 8 8 8 8 8 8
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
8 8 0 8 8 8 8 8 8 8 8 8 0 8 8 8 8
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
8 8 8 8 8 0 8 8 8 8 8 8 8 8 8 8 8
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 2 2 2 2 0 0 0 0 0 0 0
8 8 8 8 8 2 8 8 8 2 8 8 8 8 8 8 8
0 0 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0
8 8 2 8 8 8 8 8 8 8 8 8 2 8 8 8 8
0 0 2 0 0 0 0 0 0 0 0 0 2 0 0 0 0
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
8 8 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 8 0 0 8 0 0 0 8 0 0
0 0 8 0 0 8 0 0 0 8 0 0
0 0 8 0 0 8 0 0 0 8 0 0
2 0 8 0 0 0 0 0 0 8 0 0
0 0 8 0 0 8 0 0 0 8 0 0
0 0 0 0 0 8 0 0 0 8 0 0
0 0 8 0 0 8 0 0 0 0 0 0
0 0 8 0 0 8 0 0 0 8 0 0
0 0 0 0 0 8 0 0 0 0 0 0
0 0 8 0 0 8 0 0 0 8 0 0
0 0 8 0 0 8 0 0 0 8 0 0
```


**output:**
```
0 2 8 0 0 8 0 0 2 8 0 0
0 2 8 0 0 8 0 0 2 8 0 0
0 2 8 0 0 8 0 0 2 8 0 0
2 2 8 0 2 2 2 2 2 8 0 0
0 2 8 0 2 8 0 0 2 8 0 0
0 2 2 2 2 8 0 0 2 8 0 0
0 0 8 0 2 8 0 0 2 2 2 2
0 0 8 0 2 8 0 0 0 8 0 0
0 0 0 0 2 8 0 0 0 0 0 0
0 0 8 0 2 8 0 0 0 8 0 0
0 0 8 0 2 8 0 0 0 8 0 0
```


## train_3

**input:**
```
0 0 8 0 0 8 0 0 0 8 0 0 0
0 0 0 0 0 8 0 0 0 8 0 0 0
0 0 8 0 0 8 0 0 0 0 0 0 0
0 0 0 0 0 8 0 0 0 8 0 0 0
0 0 8 0 0 8 0 0 0 8 0 0 2
0 0 8 0 0 8 0 0 0 0 0 0 0
0 0 8 0 0 8 0 0 0 8 0 0 0
0 0 8 0 0 8 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 0 8 0 0 0
0 0 8 0 0 8 0 0 0 8 0 0 0
```


**output:**
```
0 0 8 0 0 8 2 0 0 8 0 0 0
0 0 0 0 0 8 2 0 0 8 0 0 0
0 0 8 0 0 8 2 2 2 2 2 0 0
0 0 0 0 0 8 2 0 0 8 2 0 0
0 0 8 0 0 8 2 0 0 8 2 2 2
0 0 8 0 0 8 2 2 2 2 2 0 0
0 0 8 0 0 8 2 0 0 8 0 0 0
0 0 8 0 0 8 2 0 0 8 0 0 0
2 2 2 2 2 2 2 0 0 8 0 0 0
0 0 8 0 0 8 0 0 0 8 0 0 0
```

## Perception of Task Elements

1.  **Input/Output Grids:** Both input and output are 2D grids of pixels with integer values representing colors.
2.  **Colors:** The significant colors are white (0), red (2), and azure (8). White represents the background or empty space. Azure seems to represent fixed barriers or walls. Red represents a starting point and the color used for filling.
3.  **Objects:**
    *   **Start Point:** Each input grid contains exactly one red pixel (2). This pixel serves as the starting point for the transformation.
    *   **Barriers:** Azure pixels (8) are present in the input grids, often forming lines or partial boundaries. These pixels remain unchanged in the output and act as barriers.
    *   **Fill Area:** The white pixels (0) represent areas that can potentially be filled.
4.  **Transformation:** The core transformation is a "flood fill" or "paint bucket" operation. Starting from the single red pixel, the red color spreads outwards into adjacent white pixels. The spread stops when it encounters an azure pixel or the edge of the grid.
5.  **Connectivity:** The fill spreads cardinally (up, down, left, right) to adjacent pixels. Diagonal movement is not observed.
6.  **State Preservation:** The original red pixel and all azure pixels remain in their positions in the output grid. Only white pixels change color to red.

## YAML Facts


```yaml
task_type: grid_transformation
input_features:
  - background_color: white (0)
  - barrier_color: azure (8)
  - start_color: red (2)
  - grid_dimensions: variable (height and width)
objects:
  - object_type: start_point
    color: red (2)
    count: 1
    description: The single pixel from which the fill operation originates.
  - object_type: barriers
    color: azure (8)
    count: multiple
    description: Pixels that block the spread of the fill color. They remain unchanged.
    shape: Can form lines, partial enclosures, or scattered points.
  - object_type: fill_area
    color: white (0)
    count: multiple
    description: Pixels representing empty space that can be filled with the start_color.
relationships:
  - relationship_type: containment/boundary
    element1: fill_area (white pixels)
    element2: barriers (azure pixels)
    description: Azure pixels define the boundaries for the fill operation.
  - relationship_type: adjacency
    description: The fill spreads to cardinally adjacent (up, down, left, right) white pixels.
transformation:
  type: flood_fill
  start_condition: Find the single red (2) pixel.
  fill_color: red (2)
  target_pixels: white (0)
  barrier_pixels: azure (8), grid_edges
  persistence:
    - Original red pixel remains red.
    - Azure pixels remain azure.
output_features:
  - background_color: white (0) (remaining unfilled areas)
  - barrier_color: azure (8) (unchanged)
  - fill_color: red (2) (original start point + filled white pixels)
```


## Natural Language Program

1.  Create a copy of the input grid to serve as the output grid.
2.  Locate the coordinates (row, column) of the single pixel with the color red (2) in the input grid. This is the starting point.
3.  Initialize a queue or stack for flood fill processing, adding the starting point coordinates. Maintain a set of visited coordinates to avoid redundant processing, initially containing the starting point.
4.  While the processing queue/stack is not empty:
    a.  Dequeue/pop a coordinate (current\_row, current\_col).
    b.  For each cardinal neighbor (up, down, left, right) of the current coordinate:
        i.  Calculate the neighbor's coordinates (neighbor\_row, neighbor\_col).
        ii. Check if the neighbor coordinate is within the grid boundaries.
        iii. Check if the neighbor coordinate has already been visited.
        iv. If the neighbor is within bounds and not visited:
            1.  Mark the neighbor coordinate as visited.
            2.  Check the color of the pixel at (neighbor\_row, neighbor\_col) in the output grid.
            3.  If the neighbor's color is white (0):
                *   Change the color of the pixel at (neighbor\_row, neighbor\_col) in the output grid to red (2).
                *   Enqueue/push the neighbor coordinate onto the processing queue/stack.
5.  Return the modified output grid.
```python
import collections
import copy

"""
Perform a flood fill operation starting from the single red (2) pixel.
The fill spreads cardinally (up, down, left, right) into adjacent white (0) pixels.
The spread is blocked by azure (8) pixels and the grid boundaries.
Azure pixels and the original red pixel remain unchanged.
"""

def transform(input_grid):
    """
    Applies a flood fill transformation starting from the red pixel.

    Args:
        input_grid (list[list[int]]): The input 2D grid.

    Returns:
        list[list[int]]: The transformed 2D grid.
    """

    # Get grid dimensions
    height = len(input_grid)
    if height == 0:
        return []
    width = len(input_grid[0])
    if width == 0:
        return [[] for _ in range(height)]

    # Initialize output_grid as a deep copy of the input_grid
    output_grid = copy.deepcopy(input_grid)

    # Find the starting red pixel (color 2)
    start_pos = None
    for r in range(height):
        for c in range(width):
            if input_grid[r][c] == 2:
                start_pos = (r, c)
                break
        if start_pos:
            break

    # If no starting red pixel is found, return the original grid copy
    if not start_pos:
        return output_grid

    # Initialize the queue for Breadth-First Search (BFS) flood fill
    queue = collections.deque([start_pos])
    # Initialize a set to keep track of visited coordinates to avoid cycles and redundant checks
    visited = {start_pos}

    # Define cardinal directions (up, down, left, right)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # Perform the flood fill
    while queue:
        # Get the current pixel coordinates from the queue
        current_r, current_c = queue.popleft()

        # Explore neighbors in cardinal directions
        for dr, dc in directions:
            neighbor_r, neighbor_c = current_r + dr, current_c + dc

            # Check if the neighbor is within the grid boundaries
            if 0 <= neighbor_r < height and 0 <= neighbor_c < width:
                # Check if the neighbor has already been visited
                if (neighbor_r, neighbor_c) not in visited:
                    # Mark the neighbor as visited
                    visited.add((neighbor_r, neighbor_c))
                    
                    # Check if the neighbor pixel is white (0) - the fill target
                    if output_grid[neighbor_r][neighbor_c] == 0:
                        # Change the neighbor's color to red (2) in the output grid
                        output_grid[neighbor_r][neighbor_c] = 2
                        # Add the neighbor to the queue to process its neighbors later
                        queue.append((neighbor_r, neighbor_c))

    # Return the modified grid
    return output_grid
```
```python
import collections
import copy

"""
Performs a flood fill operation on a 2D grid.
The fill starts from a single 'start_color' pixel (red, 2).
It spreads cardinally (up, down, left, right) into adjacent 'target_pixels' (white, 0).
The spread is blocked by 'barrier_pixels' (azure, 8) and the grid boundaries.
Barrier pixels and the original start pixel retain their color.
White pixels reachable from the start pixel without crossing barriers are changed to the 'fill_color' (red, 2).
"""

def transform(input_grid):
    """
    Applies a flood fill transformation starting from the red pixel (2),
    filling white pixels (0) and stopping at azure barriers (8) or grid edges.

    Args:
        input_grid (list[list[int]]): The input 2D grid representing colors.

    Returns:
        list[list[int]]: The transformed 2D grid with the flood fill applied.
    """

    # Get grid dimensions
    height = len(input_grid)
    if height == 0:
        return []
    width = len(input_grid[0])
    if width == 0:
        return [[] for _ in range(height)]

    # Initialize output_grid as a deep copy of the input_grid to modify
    output_grid = copy.deepcopy(input_grid)

    # --- Find the starting point ---
    start_pos = None
    start_color = 2  # Red
    for r in range(height):
        for c in range(width):
            if input_grid[r][c] == start_color:
                start_pos = (r, c)
                break
        if start_pos:
            break

    # If no starting red pixel is found, return the original grid copy
    if not start_pos:
        return output_grid

    # --- Initialize Flood Fill (BFS) ---
    fill_color = 2      # Red
    target_color = 0    # White
    barrier_color = 8   # Azure

    queue = collections.deque([start_pos])
    # Keep track of visited coordinates to avoid cycles and redundant checks
    visited = {start_pos}

    # Define cardinal directions (up, down, left, right)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # --- Perform Flood Fill ---
    while queue:
        # Get the current pixel coordinates from the front of the queue
        current_r, current_c = queue.popleft()

        # Explore neighbors in cardinal directions
        for dr, dc in directions:
            neighbor_r, neighbor_c = current_r + dr, current_c + dc

            # 1. Check if the neighbor is within the grid boundaries
            if 0 <= neighbor_r < height and 0 <= neighbor_c < width:

                # 2. Check if the neighbor has already been visited
                if (neighbor_r, neighbor_c) not in visited:

                    # Mark the neighbor as visited *before* checking its color
                    # This prevents adding it multiple times if reachable from different paths
                    visited.add((neighbor_r, neighbor_c))

                    # 3. Check if the neighbor is a target pixel (white, 0)
                    # This implicitly handles barriers (azure, 8) and already filled pixels (red, 2)
                    # as they are not equal to the target_color.
                    if output_grid[neighbor_r][neighbor_c] == target_color:

                        # Change the neighbor's color to the fill color in the output grid
                        output_grid[neighbor_r][neighbor_c] = fill_color

                        # Add the neighbor to the queue to process its neighbors later
                        queue.append((neighbor_r, neighbor_c))

    # Return the modified grid after the fill is complete
    return output_grid
```
```python
import collections
import copy

"""
Performs a flood fill operation on a 2D grid.
The fill starts from a single 'start_color' pixel (red, 2).
It spreads cardinally (up, down, left, right) into adjacent 'target_pixels' (white, 0).
The spread is blocked by 'barrier_pixels' (azure, 8) and the grid boundaries.
Barrier pixels and the original start pixel retain their color.
White pixels reachable from the start pixel without crossing barriers are changed to the 'fill_color' (red, 2).
"""

def transform(input_grid):
    """
    Applies a flood fill transformation starting from the red pixel (2),
    filling white pixels (0) and stopping at azure barriers (8) or grid edges.

    Args:
        input_grid (list[list[int]]): The input 2D grid representing colors.

    Returns:
        list[list[int]]: The transformed 2D grid with the flood fill applied.
    """

    # Get grid dimensions
    height = len(input_grid)
    if height == 0:
        return []
    width = len(input_grid[0])
    if width == 0:
        return [[] for _ in range(height)]

    # Initialize output_grid as a deep copy of the input_grid to modify
    # This ensures barriers (8) and the original start pixel (2) are preserved
    output_grid = copy.deepcopy(input_grid)

    # --- Find the starting point ---
    start_pos = None
    start_color = 2  # Red
    for r in range(height):
        for c in range(width):
            if input_grid[r][c] == start_color:
                start_pos = (r, c)
                break
        if start_pos:
            break

    # If no starting red pixel is found, something is wrong with the input assumptions,
    # but we return the unmodified copy as per the logic observed.
    if not start_pos:
        return output_grid

    # --- Initialize Flood Fill (BFS) ---
    fill_color = 2      # Red - The color to fill with
    target_color = 0    # White - The color of pixels to be filled
    # barrier_color = 8 # Azure - Implicitly handled by only filling target_color

    # Queue for BFS, initialized with the starting position
    queue = collections.deque([start_pos])
    # Set to keep track of visited coordinates to prevent cycles and redundant processing
    visited = {start_pos}

    # Define cardinal directions (up, down, left, right) for neighbor checking
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # --- Perform Flood Fill ---
    while queue:
        # Get the current pixel coordinates from the front of the queue
        current_r, current_c = queue.popleft()

        # Explore neighbors in cardinal directions
        for dr, dc in directions:
            neighbor_r, neighbor_c = current_r + dr, current_c + dc

            # 1. Check if the neighbor is within the grid boundaries
            if 0 <= neighbor_r < height and 0 <= neighbor_c < width:

                # 2. Check if the neighbor has already been visited
                if (neighbor_r, neighbor_c) not in visited:

                    # 3. Check if the neighbor is a target pixel (white, 0)
                    # We only fill and explore from white pixels. Azure (8) and
                    # already-filled red (2) pixels act as barriers implicitly.
                    if output_grid[neighbor_r][neighbor_c] == target_color:

                        # Mark the neighbor as visited *only if* it's a target pixel
                        # This ensures we don't stop exploring just because we hit a barrier early
                        visited.add((neighbor_r, neighbor_c))

                        # Change the neighbor's color to the fill color in the output grid
                        output_grid[neighbor_r][neighbor_c] = fill_color

                        # Add the newly filled neighbor to the queue to process its neighbors
                        queue.append((neighbor_r, neighbor_c))
                    else:
                        # If the neighbor is not a target color (e.g., it's a barrier or already red),
                        # mark it as visited so we don't check it again from another path.
                        # This is important for efficiency, especially in complex shapes.
                         visited.add((neighbor_r, neighbor_c))


    # Return the modified grid after the fill is complete
    return output_grid
```
