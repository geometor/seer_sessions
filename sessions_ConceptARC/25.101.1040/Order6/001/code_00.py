import numpy as np
from collections import deque

"""
Identify all distinct, contiguous, non-white rectangular blocks in the input grid.
Assume blocks are vertically arranged and start in the same column (usually column 0).
Record each block's color, pixel data (shape), height, width, and original top row index.
Maintain the original top-to-bottom order of the blocks.
Calculate the vertical gaps (number of white rows) between consecutive blocks in the original order.
Sort the blocks based on their width in ascending order.
Create a new empty output grid of the same dimensions as the input, filled with white (0).
Place the sorted blocks onto the output grid sequentially from top to bottom.
The starting row for the first sorted block is the starting row of the first block in the original input order.
The vertical gap placed *after* placing the k-th sorted block is the gap that originally existed *after* the k-th block in the *original* input order.
Return the completed output grid.
"""

def find_objects(grid: np.ndarray) -> list[dict]:
    """
    Finds contiguous blocks of non-white pixels in the grid.

    Args:
        grid: The input grid as a numpy array.

    Returns:
        A list of dictionaries, where each dictionary represents an object
        and contains 'color', 'pixels', 'top_row', 'left_col', 'height', 'width'.
        The list is sorted by the 'top_row' of the objects.
    """
    objects = []
    visited = np.zeros_like(grid, dtype=bool)
    rows, cols = grid.shape

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and not visited[r, c]:
                color = grid[r, c]
                q = deque([(r, c)])
                visited[r, c] = True
                current_object_pixels = set([(r, c)])
                min_r, max_r = r, r
                min_c, max_c = c, c

                while q:
                    row, col = q.popleft()
                    min_r = min(min_r, row)
                    max_r = max(max_r, row)
                    min_c = min(min_c, col)
                    max_c = max(max_c, col)

                    # Check neighbors (4-connectivity)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            current_object_pixels.add((nr, nc))

                height = max_r - min_r + 1
                width = max_c - min_c + 1
                
                # Extract the pixel data for the block
                block_pixels = np.zeros((height, width), dtype=int)
                for pr, pc in current_object_pixels:
                    block_pixels[pr - min_r, pc - min_c] = color

                objects.append({
                    'color': color,
                    'pixels': block_pixels,
                    'top_row': min_r,
                    'left_col': min_c, # Assuming all start at col 0 based on examples
                    'height': height,
                    'width': width,
                })

    # Sort objects by their top row to get the original vertical order
    objects.sort(key=lambda obj: obj['top_row'])
    return objects

def calculate_gaps(objects: list[dict]) -> list[int]:
    """
    Calculates the vertical gaps between consecutive objects.

    Args:
        objects: A list of object dictionaries, sorted by top_row.

    Returns:
        A list of integers representing the gap size below each object
        (except the last one).
    """
    gaps = []
    for i in range(len(objects) - 1):
        current_obj = objects[i]
        next_obj = objects[i+1]
        gap = next_obj['top_row'] - (current_obj['top_row'] + current_obj['height'])
        gaps.append(gap)
    return gaps

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by reordering rectangular blocks based on width.

    1. Finds non-white rectangular blocks.
    2. Calculates vertical gaps between them in the original order.
    3. Sorts the blocks by width (ascending).
    4. Reconstructs the grid with sorted blocks, preserving original gaps relative
       to the *original* block order index.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    input_array = np.array(input_grid, dtype=int)
    rows, cols = input_array.shape

    # 1. Find objects and maintain original order
    original_objects = find_objects(input_array)
    if not original_objects:
        return input_grid # Return original if no objects found

    # 2. Calculate vertical gaps based on original order
    original_gaps = calculate_gaps(original_objects)

    # 3. Sort objects by width
    sorted_objects = sorted(original_objects, key=lambda obj: obj['width'])

    # 4. Initialize output grid
    output_array = np.zeros_like(input_array, dtype=int)

    # 5. Place sorted objects onto the output grid
    current_top_row = original_objects[0]['top_row'] # Start at the top row of the first original object

    for i, obj in enumerate(sorted_objects):
        # Determine placement position
        top = current_top_row
        left = obj['left_col'] # Use original left column (assumed constant here)
        height = obj['height']
        width = obj['width']
        pixels = obj['pixels']

        # Place the object
        if top + height <= rows and left + width <= cols:
             # Ensure the pixel block fits the identified dimensions
             actual_pixel_height, actual_pixel_width = pixels.shape
             if actual_pixel_height == height and actual_pixel_width == width:
                 output_array[top:top + height, left:left + width] = np.where(
                     pixels != 0, pixels, output_array[top:top + height, left:left + width]
                 )
             else: # Fallback if dimensions mismatch somehow (shouldn't happen with rects)
                 print(f"Warning: Dimension mismatch for object {i}. Using detected shape.")
                 output_array[top:top + actual_pixel_height, left:left + actual_pixel_width] = np.where(
                     pixels != 0, pixels, output_array[top:top + actual_pixel_height, left:left + actual_pixel_width]
                 )


        # Update current_top_row for the next block
        # The gap added is the gap that followed the i-th block in the *original* order
        if i < len(sorted_objects) - 1:
            gap_to_add = original_gaps[i] if i < len(original_gaps) else 0 # Handle potential index out of bounds if gaps are fewer
            current_top_row += height + gap_to_add
        # Else: it's the last block, no need to update further

    return output_array.tolist()