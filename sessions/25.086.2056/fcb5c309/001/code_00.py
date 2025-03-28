import numpy as np
from collections import deque

"""
Identifies all contiguous objects of non-white pixels in the input grid.
Calculates the size of each object.
Finds the maximum size among all objects.
Identifies the color ('scatter_color') of the pixels belonging to objects whose size is *not* the maximum size.
Determines the numerical value ('digit_value') of the 'scatter_color'.
Selects a predefined pixel grid pattern corresponding to the 'digit_value'.
Constructs the output grid using the 'scatter_color' for the digit pattern pixels and white (0) for the background pixels.
"""

# Predefined digit patterns (using 1 as placeholder for scatter_color, 0 for white)
# Note: Dimensions might vary per digit.
DIGIT_PATTERNS = {
    # Pattern for 2 (7x7)
    2: np.array([
        [1, 1, 1, 1, 1, 1, 1],
        [1, 0, 1, 0, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 1, 1],
        [1, 1, 1, 1, 1, 1, 1]
    ], dtype=int),

    # Pattern for 3 (6x7)
    3: np.array([
        [1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 1, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 1],
        [1, 1, 0, 1, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1]
    ], dtype=int), # Height 6, Width 7

    # Pattern for 4 (7x7)
    4: np.array([
        [1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 1],
        [1, 1, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1]
    ], dtype=int),
    # Add patterns for 0, 1, 5, 6, 7, 8, 9 if they might appear as scatter colors.
    # Assuming only 2, 3, 4 based on examples for now.
}

def _find_objects(grid):
    """
    Finds all contiguous objects of the same non-zero color in the grid.

    Args:
        grid (np.array): The input grid.

    Returns:
        list: A list of tuples, where each tuple is (color, size).
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            # If pixel is non-white and not visited yet
            if grid[r, c] != 0 and not visited[r, c]:
                color = grid[r, c]
                size = 0
                q = deque([(r, c)])
                visited[r, c] = True

                # Perform BFS to find all connected pixels of the same color
                while q:
                    curr_r, curr_c = q.popleft()
                    size += 1

                    # Check neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc

                        # Check bounds, color match, and visited status
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                
                objects.append({'color': color, 'size': size})

    return objects

def transform(input_grid):
    """
    Transforms the input grid based on identifying the 'scatter' color
    (color of objects not having the maximum size) and drawing the digit
    corresponding to that color's value.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the output grid.
    """
    input_grid_np = np.array(input_grid)

    # 1. Find all non-white objects and their sizes/colors.
    objects = _find_objects(input_grid_np)

    if not objects:
        # Handle case with no non-white pixels if necessary
        # For now, assume valid inputs based on examples
        # Returning an empty or default grid might be an option
        # Let's assume the pattern for 0 if no objects? Or raise error?
        # Based on task, this shouldn't happen. If it does, maybe return empty grid?
        # For now, let's assume valid input means >0 objects
        if input_grid_np.shape == (0,0): return np.array([[]]) # Handle totally empty input
        return np.zeros((1,1), dtype=int) # Placeholder for error/unexpected

    # 2. Find the maximum size among these objects.
    max_size = 0
    if objects:
      max_size = max(obj['size'] for obj in objects)

    # 3. Identify the 'scatter_color'.
    scatter_color = -1 # Initialize with invalid value
    found_scatter = False
    for obj in objects:
        if obj['size'] != max_size:
            # Assume the first color found that isn't max size is the scatter color
            # Assumes uniqueness based on examples
            scatter_color = obj['color']
            found_scatter = True
            break # Stop once found

    # Handle case where no scatter color is found (e.g., all objects are max size)
    if not found_scatter:
        # This case didn't appear in training. What should happen?
        # Maybe default to the color of the max_size objects if only one color exists?
        # Or return an empty/error grid?
        # Let's assume task guarantees a scatter color exists.
        # If only one object exists, it can't be scatter.
        if len(objects) == 1:
             # Maybe the single object *is* the scatter object? Needs clarification.
             # Or perhaps return the pattern for 0?
             # For now, return small default grid if scatter not identifiable.
             print("Warning: Could not definitively identify scatter color.")
             return np.zeros((1,1), dtype=int) # Placeholder
        else:
             # Multiple objects, all max_size? This also seems unlikely.
             print("Warning: Multiple objects found, all with max size. Cannot identify scatter color.")
             return np.zeros((1,1), dtype=int) # Placeholder


    # 4. Determine the numerical value ('digit_value').
    digit_value = scatter_color

    # 5. Retrieve the predefined pixel grid pattern.
    if digit_value not in DIGIT_PATTERNS:
        # Handle case where the scatter color doesn't have a defined pattern
        print(f"Error: No digit pattern defined for color value {digit_value}")
        # Return a default or empty grid
        return np.zeros((1, 1), dtype=int) # Placeholder

    pattern = DIGIT_PATTERNS[digit_value]

    # 6. Construct the output grid.
    # Create a copy of the pattern to modify
    output_grid = pattern.copy()

    # Replace placeholder '1' with the actual scatter_color
    output_grid[output_grid == 1] = scatter_color
    # Background '0' is already correct.

    # 7. Return the constructed output grid.
    return output_grid