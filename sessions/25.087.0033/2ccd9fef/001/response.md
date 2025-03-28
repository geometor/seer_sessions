```python
import numpy as np
from collections import Counter
from typing import List, Tuple, Set

"""
Identify the first repeating vertical block in the input grid. The height 'H' is determined by the first row index (>= 1) that is identical to row 0.
Extract this first block (top H rows).
Identify the most frequent color in this block as the background color.
Find all connected shapes of non-background colors within the block.
Classify shapes as 'border' shapes if they touch any of the four edges of the block, otherwise classify them as 'internal' shapes.
Create an output grid with the same dimensions as the extracted block, filled with the background color.
Draw the border shapes onto the output grid unchanged.
For each internal shape, expand it horizontally to the right by 2 columns. That is, for every pixel (r, c) in the original internal shape, the pixels (r, c), (r, c+1), and (r, c+2) in the output grid should be set to the shape's color, provided they are within the grid bounds.
Draw these expanded internal shapes onto the output grid.
"""

def _find_shapes(grid: np.ndarray, background_color: int) -> List[Tuple[int, Set[Tuple[int, int]], bool]]:
    """
    Finds connected components (shapes) of non-background colors in the grid.

    Args:
        grid: The input numpy array grid.
        background_color: The color considered as background.

    Returns:
        A list of tuples, where each tuple represents a shape:
        (color, set_of_coordinates, is_border)
        - color: The color of the shape.
        - set_of_coordinates: A set containing (row, col) tuples of the shape's pixels.
        - is_border: True if the shape touches any border of the grid, False otherwise.
    """
    height, width = grid.shape
    visited = np.zeros((height, width), dtype=bool)
    shapes = []

    for r in range(height):
        for c in range(width):
            # If not visited and not background color, start BFS for a new shape
            if not visited[r, c] and grid[r, c] != background_color:
                color = grid[r, c]
                coords = set()
                is_border = False
                q = [(r, c)] # Queue for BFS
                visited[r, c] = True

                while q:
                    row, col = q.pop(0)
                    coords.add((row, col))

                    # Check if this pixel is on the border
                    if row == 0 or row == height - 1 or col == 0 or col == width - 1:
                        is_border = True

                    # Explore neighbors (4-directional: up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        # Check if neighbor is within bounds, not visited, and has the same color
                        if 0 <= nr < height and 0 <= nc < width and \
                           not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))

                shapes.append((color, coords, is_border))
    return shapes


def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Transforms the input grid based on identifying a repeating block,
    finding shapes within the first block, and expanding internal shapes horizontally.
    """
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape

    # 1. Determine Block Height (H)
    # Find the first row (index >= 1) identical to the first row (index 0)
    H = height # Default to full height if no repeat found
    if height > 1:
        first_row = input_np[0]
        for i in range(1, height):
            if np.array_equal(first_row, input_np[i]):
                H = i
                break

    # 2. Extract the First Unit (Block)
    first_block = input_np[:H]
    block_height, block_width = first_block.shape

    # Handle edge case of empty or invalid block
    if block_height == 0 or block_width == 0:
        return [[]] # Or handle as appropriate for the task constraints

    # 3. Identify Background Color
    # Find the most frequent color in the first block
    pixel_counts = Counter(first_block.flatten())
    # Ensure there's at least one pixel to avoid error on empty blocks
    if not pixel_counts:
         return first_block.tolist() # Return empty/original if block was empty
    background_color = pixel_counts.most_common(1)[0][0]

    # 4. Identify Shapes within the first block
    shapes = _find_shapes(first_block, background_color)

    # 5. Construct Output Grid (Initialize with background color)
    output_grid = np.full((block_height, block_width), background_color, dtype=int)

    # 6. Process Shapes and Draw onto Output Grid
    for color, coords, is_border in shapes:
        if is_border:
            # Draw original border shape directly
            for r, c in coords:
                # Check bounds just in case (should be within block bounds by definition)
                if 0 <= r < block_height and 0 <= c < block_width:
                    output_grid[r, c] = color
        else:
            # Expand internal shape horizontally to the right by 2 columns
            modified_coords = set()
            for r, c in coords:
                # Add original pixel and the two to its right
                for dc in range(3): # dc = 0, 1, 2
                    nc = c + dc
                    # Check only horizontal bound; vertical is implicit
                    if nc < block_width:
                         modified_coords.add((r, nc))

            # Draw the modified shape
            for r, c in modified_coords:
                 # Check vertical bound (should be safe but good practice)
                 if 0 <= r < block_height:
                    output_grid[r, c] = color

    # Return the result as a list of lists
    return output_grid.tolist()
```