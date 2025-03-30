import numpy as np
from collections import deque

"""
Identify all distinct contiguous blocks of connected pixels that have the same, non-white color (pixels with value 0 are background and ignored).
For each identified block, determine its minimum bounding box (the smallest rectangle enclosing all pixels of the block).
Calculate the area of each block's bounding box (height * width).
Find the maximum bounding box area among all the blocks.
Identify all blocks whose bounding boxes have this maximum area.
If there is only one block with the maximum bounding box area, choose its color.
If there are multiple blocks whose bounding boxes share the maximum area, compare their color values (1-9) and choose the color of the block that has the numerically *smallest* color value.
If no non-white blocks are found in the input grid, choose white (color 0).
Construct a 3x3 output grid and fill all its cells with the chosen color.
"""

# === Helper Functions ===

def find_contiguous_blocks(grid):
    """
    Finds all contiguous blocks of the same non-background color (0).

    Uses Breadth-First Search (BFS) to find connected components for each color.

    Args:
        grid (np.array): The input grid.

    Returns:
        list: A list of dictionaries, where each dictionary contains:
              {'color': int, 'coords': set_of_tuples, 'size': int}
              representing a contiguous block. Returns an empty list if no
              non-background blocks are found.
    """
    height, width = grid.shape
    visited = set()
    blocks = []

    for r in range(height):
        for c in range(width):
            # Process pixel if it's non-background and not yet visited
            if grid[r, c] != 0 and (r, c) not in visited:
                color = grid[r, c]
                component_coords = set()
                queue = deque([(r, c)])
                visited.add((r, c))

                # Start BFS from the current pixel
                while queue:
                    row, col = queue.popleft()
                    component_coords.add((row, col))

                    # Check cardinal neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        # Check if neighbor is within grid bounds
                        if 0 <= nr < height and 0 <= nc < width:
                            # Check if neighbor has the same color and hasn't been visited
                            if grid[nr, nc] == color and (nr, nc) not in visited:
                                visited.add((nr, nc))
                                queue.append((nr, nc))

                # Store the found block if it's not empty
                if component_coords:
                    blocks.append({
                        'color': color,
                        'coords': component_coords,
                        'size': len(component_coords) # size = pixel count
                    })

    return blocks

def get_bounding_box(coords):
    """
    Calculates the bounding box dimensions and corners for a set of coordinates.

    Args:
        coords (set): A set of (row, col) tuples.

    Returns:
        tuple: (min_r, min_c, max_r, max_c, height, width) or
               (None, None, None, None, 0, 0) if coords is empty.
    """
    if not coords:
        return None, None, None, None, 0, 0

    rows = [r for r, c in coords]
    cols = [c for r, c in coords]
    min_r, max_r = min(rows), max(rows)
    min_c, max_c = min(cols), max(cols)
    # Height and width are inclusive of the min/max row/col
    height = max_r - min_r + 1
    width = max_c - min_c + 1
    return min_r, min_c, max_r, max_c, height, width

# === Main Transformation Function ===

def transform(input_grid):
    """
    Transforms the input grid based on finding the object with the largest bounding box area.

    The transformation logic is:
    1. Find all contiguous blocks of non-white pixels.
    2. Calculate the bounding box area for each block.
    3. Find the maximum bounding box area among all blocks.
    4. Identify all blocks with this maximum area.
    5. Among these maximum-area blocks, select the one with the smallest color index.
    6. If no non-white blocks are found, use white (0).
    7. Create a 3x3 output grid filled with the selected color.

    Args:
        input_grid (list of lists): The input grid representation.

    Returns:
        list of lists: A 3x3 grid filled with the determined color.
    """
    # Convert input to NumPy array for easier processing
    input_grid_np = np.array(input_grid, dtype=int)

    # Handle potential empty input
    if input_grid_np.size == 0:
        # Return a default 3x3 white grid if input is empty
        return [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    # Step 1: Find all contiguous blocks
    blocks = find_contiguous_blocks(input_grid_np)

    # If no non-white blocks found, default to white
    if not blocks:
        output_color = 0
    else:
        # Step 2 & 3: Calculate bounding box areas and find the maximum area
        max_area = -1
        blocks_with_details = []
        for block in blocks:
            coords = block['coords']
            color = block['color']
            _, _, _, _, height, width = get_bounding_box(coords)
            area = height * width
            blocks_with_details.append({'color': color, 'area': area})
            if area > max_area:
                max_area = area

        # Step 4: Identify all blocks with the maximum area
        max_area_blocks = [b for b in blocks_with_details if b['area'] == max_area]

        # Step 5 & 7: Tie-break using the minimum color index
        # Sort the max area blocks by color (ascending)
        max_area_blocks.sort(key=lambda x: x['color'])
        # The first block after sorting has the minimum color index
        output_color = max_area_blocks[0]['color']

    # Step 9: Create the 3x3 output grid filled with the chosen color
    output_grid_np = np.full((3, 3), output_color, dtype=int)

    # Convert the NumPy array back to a list of lists for the final output
    output_grid = output_grid_np.tolist()

    return output_grid