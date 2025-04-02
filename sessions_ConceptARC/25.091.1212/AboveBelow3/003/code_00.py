import numpy as np
import collections

def find_topmost_object(grid: np.ndarray) -> tuple[dict[tuple[int, int], int], int]:
    """
    Finds the topmost non-background object(s) in the grid.

    Args:
        grid: A numpy array representing the input grid.

    Returns:
        A tuple containing:
        - A dictionary mapping coordinates (r, c) of the topmost object pixels 
          to their colors. Returns an empty dict if no non-background pixels exist.
        - The maximum row index (max_r) occupied by the topmost object. 
          Returns -1 if no object is found.
    """
    height, width = grid.shape
    background_color = 0
    
    # Find all non-background pixels
    non_background_coords = list(zip(*np.where(grid != background_color)))

    if not non_background_coords:
        return {}, -1 # No object found

    # Determine the minimum row index with non-background pixels
    min_r = min(r for r, c in non_background_coords)

    # Identify all connected non-background pixels forming the topmost object(s) using BFS.
    # Start BFS from all non-background pixels located at min_r.
    q = collections.deque([(r, c) for r, c in non_background_coords if r == min_r])
    visited = set(q)
    topmost_object_pixels = {} # Store {(r, c): color}
    max_r = -1

    while q:
        r, c = q.popleft()
        
        # Record the pixel and its color, update max_r
        color = grid[r, c]
        # Ensure we are only adding non-background pixels (should be guaranteed by neighbors check, but safe)
        if color != background_color:
            topmost_object_pixels[(r, c)] = color
            max_r = max(max_r, r)
        else:
            continue # Should not happen with the check below

        # Explore neighbors (4-connectivity: up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            
            # Check boundaries and if the neighbor is non-background and not visited
            if 0 <= nr < height and 0 <= nc < width and \
               grid[nr, nc] != background_color and (nr, nc) not in visited:
                visited.add((nr, nc))
                q.append((nr, nc))
                
    return topmost_object_pixels, max_r

def calculate_shift(grid: np.ndarray, max_r: int) -> int:
    """
    Calculates the downward shift distance based on consecutive all-background 
    rows below the object's maximum row extent.

    Args:
        grid: A numpy array representing the input grid.
        max_r: The maximum row index occupied by the object.

    Returns:
        The calculated downward shift distance.
    """
    height = grid.shape[0]
    background_color = 0
    shift = 0
    
    # Start checking from the row immediately below the object
    for r_check in range(max_r + 1, height):
        # Check if the entire row is composed of the background color
        if np.all(grid[r_check, :] == background_color):
            shift += 1
        else:
            # Stop counting at the first row that is not entirely background
            break 
            
    return shift

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Identifies the topmost non-background object in the input grid, calculates a 
    vertical downward shift distance based on the number of consecutive all-background 
    rows immediately below the object, and moves only this topmost object down by 
    that distance. All other objects in the grid remain stationary.

    1. Convert input list of lists to a NumPy array.
    2. Find the topmost non-background object and its maximum row index (`max_r`).
    3. If no object is found, return the original grid.
    4. Calculate the downward `shift` distance by counting consecutive all-background rows below `max_r`.
    5. Create a copy of the input grid to serve as the output grid.
    6. Erase the original topmost object from the output grid by setting its pixels to the background color.
    7. Draw the topmost object in the output grid at its new position, shifted down by `shift` rows, ensuring pixels stay within grid bounds.
    8. Convert the output NumPy array back to a list of lists and return it.
    """
    grid = np.array(input_grid, dtype=int)
    height, width = grid.shape
    background_color = 0

    # Find the topmost object and its maximum row extent
    topmost_object_pixels, max_r = find_topmost_object(grid)

    # If no object was found (e.g., grid is all background), return original
    if not topmost_object_pixels:
        return input_grid

    # Calculate the downward shift distance
    shift = calculate_shift(grid, max_r)

    # Create the output grid as a copy of the input
    output_grid = grid.copy()

    # Erase the original topmost object from the output grid
    for r, c in topmost_object_pixels.keys():
        output_grid[r, c] = background_color

    # Draw the shifted topmost object onto the output grid
    for (r, c), color in topmost_object_pixels.items():
        new_r = r + shift
        # Draw the pixel only if the new row is within the grid height
        if 0 <= new_r < height:
            output_grid[new_r, c] = color
            
    # Convert the final NumPy array back to a list of lists
    return output_grid.tolist()