import numpy as np
from collections import deque

"""
Identifies the connected component of non-white pixels with the largest
bounding box area and crops the input grid to that bounding box.
Connectivity is 8-way (including diagonals).
"""

def find_connected_components(grid_np):
    """
    Finds all connected components of non-white pixels in the grid using 8-way connectivity.

    Args:
        grid_np (np.array): The input grid as a numpy array.

    Returns:
        list: A list of components, where each component is a list of (row, col) tuples.
              Returns an empty list if no non-white pixels are found.
    """
    rows, cols = grid_np.shape
    visited = set()
    components = []

    for r in range(rows):
        for c in range(cols):
            # If pixel is non-white and not visited yet, start BFS
            if grid_np[r, c] != 0 and (r, c) not in visited:
                component = []
                q = deque([(r, c)])
                visited.add((r, c))

                while q:
                    row, col = q.popleft()
                    component.append((row, col))

                    # Check 8 neighbors (horizontal, vertical, diagonal)
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue  # Skip self

                            nr, nc = row + dr, col + dc

                            # Check boundaries
                            if 0 <= nr < rows and 0 <= nc < cols:
                                # Check if neighbor is non-white and not visited
                                if grid_np[nr, nc] != 0 and (nr, nc) not in visited:
                                    visited.add((nr, nc))
                                    q.append((nr, nc))

                # Add the found component to the list
                if component: # Ensure we don't add empty lists if logic were ever to allow it
                    components.append(component)

    return components

def transform(input_grid):
    """
    Transforms the input grid by cropping it to the bounding box of the
    connected component of non-white pixels that has the largest area.
    """
    # Convert input list of lists to a numpy array for efficient processing
    input_grid_np = np.array(input_grid, dtype=int)

    # Step 1: Identify all connected components of non-white pixels (8-way)
    components = find_connected_components(input_grid_np)

    # Handle edge case: no non-white pixels found
    if not components:
        # Return a minimal white grid as per typical ARC behavior for empty results
        return [[0]]

    largest_bbox_area = -1
    target_bbox = None # Will store (min_r, max_r, min_c, max_c) of the target component

    # Step 2 & 3: Iterate through components, calculate bounding box and its area
    for component in components:
        # This check is technically redundant if find_connected_components guarantees non-empty components
        if not component:
            continue

        # Determine the min/max row and column indices for the component
        rows = [r for r, c in component]
        cols = [c for r, c in component]

        min_r, max_r = min(rows), max(rows)
        min_c, max_c = min(cols), max(cols)

        # Calculate the dimensions and area of the bounding box
        height = max_r - min_r + 1
        width = max_c - min_c + 1
        area = height * width

        # Step 4: Select the component with the maximum bounding box area
        # If areas are equal, the first one encountered with the max area is kept.
        if area > largest_bbox_area:
            largest_bbox_area = area
            # Step 5: Store the coordinates of the largest bounding box found so far
            target_bbox = (min_r, max_r, min_c, max_c)

    # This case should ideally not be reached if components list is non-empty
    if target_bbox is None:
         return [[0]]

    # Step 6: Crop the original input grid using the target bounding box coordinates
    min_r, max_r, min_c, max_c = target_bbox
    # NumPy slicing: [start_row : end_row+1, start_col : end_col+1]
    output_grid_np = input_grid_np[min_r : max_r + 1, min_c : max_c + 1]

    # Convert the resulting numpy array back to a list of lists
    output_grid = output_grid_np.tolist()

    return output_grid