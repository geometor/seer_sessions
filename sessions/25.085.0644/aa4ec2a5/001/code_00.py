import numpy as np
from collections import deque

"""
Identifies connected blue (1) objects in the input grid.
For each object:
1. Finds all adjacent (including diagonal) yellow (4) pixels, marking them as the border.
2. Determines if the area enclosed by the border (including the original blue pixels and potentially some yellow pixels) contained only blue pixels or both blue and yellow pixels in the input.
   - "Enclosed" yellow pixels are those yellow pixels in the input that are not part of the border and are not reachable from the grid edges without crossing the border or the blue object.
3. If the enclosed area was originally only blue:
   - Change the border pixels to red (2).
   - The original blue pixels remain blue (1).
4. If the enclosed area was originally blue and yellow:
   - Change the border pixels to red (2).
   - Change the original blue pixels to azure (8).
   - Change the enclosed yellow pixels:
     - to azure (8) if they are adjacent (including diagonal) to any red border pixel.
     - to magenta (6) otherwise.
Pixels not part of any object transformation remain their original color.
"""

def find_objects(grid, color):
    """
    Finds all connected components (objects) of a specific color in the grid.
    Connectivity includes diagonals (8-way).
    Args:
        grid (np.array): The input grid.
        color (int): The color of the objects to find.
    Returns:
        list[set]: A list where each element is a set of (row, col) tuples
                   representing the coordinates of one object.
    """
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(height):
        for c in range(width):
            # If it's the target color and not yet visited, start a new object search (BFS)
            if grid[r, c] == color and not visited[r, c]:
                obj_coords = set()
                q = deque([(r, c)])
                visited[r, c] = True
                while q:
                    row, col = q.popleft()
                    obj_coords.add((row, col))
                    # Check 8 neighbors
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue
                            nr, nc = row + dr, col + dc
                            # Check bounds and if neighbor is the same color and unvisited
                            if 0 <= nr < height and 0 <= nc < width and \
                               grid[nr, nc] == color and not visited[nr, nc]:
                                visited[nr, nc] = True
                                q.append((nr, nc))
                if obj_coords:
                    objects.append(obj_coords)
    return objects

def get_neighbors(r, c, height, width, diagonal=True):
    """
    Gets valid neighbor coordinates for a given cell (r, c).
    Args:
        r (int): Row index.
        c (int): Column index.
        height (int): Grid height.
        width (int): Grid width.
        diagonal (bool): Include diagonal neighbors if True.
    Returns:
        list[tuple]: List of valid (row, col) neighbor coordinates.
    """
    neighbors = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            # Skip diagonals if diagonal is False
            if not diagonal and (dr != 0 and dc != 0):
                 continue
            nr, nc = r + dr, c + dc
            # Check if neighbor is within grid bounds
            if 0 <= nr < height and 0 <= nc < width:
                neighbors.append((nr, nc))
    return neighbors

def transform(input_grid):
    """
    Applies the described transformation rule to the input grid.
    Args:
        input_grid (list[list[int]]): The input grid.
    Returns:
        list[list[int]]: The transformed output grid.
    """
    input_grid_np = np.array(input_grid, dtype=int)
    output_grid = np.copy(input_grid_np)
    height, width = input_grid_np.shape
    
    # Find all blue objects
    blue_objects = find_objects(input_grid_np, 1)
    
    # Keep track of pixels that have been assigned to a border or filled region
    # to handle cases where objects might be close, though examples don't show overlap.
    processed_pixels = set() 

    for blue_coords in blue_objects:
        # If any part of this object was already processed (e.g., part of a border of another nearby object)
        # this check might prevent some transformations, but based on examples it seems objects are separate.
        # We proceed assuming objects and their influence zones don't overlap significantly.
        
        border_coords = set()
        
        # 1. Find border pixels: Yellow (4) pixels adjacent (8-way) to the current blue object.
        for r, c in blue_coords:
            for nr, nc in get_neighbors(r, c, height, width, diagonal=True):
                # Check if neighbor is yellow and not already part of another object's processed area
                if input_grid_np[nr, nc] == 4 and (nr, nc) not in processed_pixels:
                    border_coords.add((nr, nc))
        
        # 2. Determine internal yellow pixels using flood fill from edges.
        # Create a temporary grid to mark different regions:
        # 0: Undecided (initially yellow not border)
        # 1: Blue object pixel
        # -1: Border pixel
        # -2: External yellow pixel (reachable from edge)
        temp_grid = np.zeros_like(input_grid_np, dtype=int) 
        
        for r, c in blue_coords:
            temp_grid[r, c] = 1
        for r, c in border_coords:
            temp_grid[r, c] = -1

        # Flood fill queue, starting with edge yellow pixels not part of the border
        q = deque()
        visited_flood = np.zeros_like(input_grid_np, dtype=bool) # Visited for this flood fill

        # Seed the queue with yellow non-border pixels on the grid edges
        for r in range(height):
            for c in [0, width - 1]:
                 if temp_grid[r, c] == 0 and not visited_flood[r,c]: # Yellow, non-border, unvisited
                    q.append((r,c))
                    visited_flood[r,c] = True
                    temp_grid[r, c] = -2 # Mark as external
        for c in range(1, width - 1): # Avoid double-checking corners
             for r in [0, height - 1]:
                if temp_grid[r, c] == 0 and not visited_flood[r,c]: # Yellow, non-border, unvisited
                    q.append((r,c))
                    visited_flood[r,c] = True
                    temp_grid[r, c] = -2 # Mark as external

        # Perform flood fill (8-way) to mark all reachable external yellow pixels
        while q:
            r, c = q.popleft()
            for nr, nc in get_neighbors(r, c, height, width, diagonal=True):
                 # If neighbor is yellow, not border, and not visited by flood fill
                 if temp_grid[nr, nc] == 0 and not visited_flood[nr, nc]: 
                    visited_flood[nr, nc] = True
                    temp_grid[nr, nc] = -2 # Mark as external
                    q.append((nr, nc))

        # Identify internal yellow pixels: those originally yellow (4) that are still marked 0 in temp_grid
        internal_yellow_coords = set()
        for r in range(height):
            for c in range(width):
                if input_grid_np[r, c] == 4 and temp_grid[r, c] == 0:
                     internal_yellow_coords.add((r, c))

        # Add coordinates processed for this object to the global set
        processed_pixels.update(blue_coords)
        processed_pixels.update(border_coords)
        processed_pixels.update(internal_yellow_coords)
        
        # 3. Apply Coloring Rules to the output grid

        # Change border pixels to red (2)
        for r, c in border_coords:
            output_grid[r, c] = 2

        # Check if there were any internal yellow pixels
        if not internal_yellow_coords:
            # Case 1: Only blue inside. Blue pixels remain blue (1).
            # No action needed as output_grid started as a copy.
            pass 
        else:
            # Case 2: Blue and yellow inside.
            # Change original blue pixels to azure (8)
            for r, c in blue_coords:
                output_grid[r, c] = 8
            
            # Change internal yellow pixels based on adjacency to the red border
            for r, c in internal_yellow_coords:
                is_adj_to_border = False
                # Check 8 neighbors of the internal yellow pixel
                for nr, nc in get_neighbors(r, c, height, width, diagonal=True):
                    # If any neighbor is a border pixel for *this* object
                    if (nr, nc) in border_coords:
                        is_adj_to_border = True
                        break
                
                if is_adj_to_border:
                    output_grid[r, c] = 8 # Azure
                else:
                    output_grid[r, c] = 6 # Magenta

    return output_grid.tolist()