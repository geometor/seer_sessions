"""
Identify cross shapes in the input grid and add pixels at knight's move locations relative to the center of each cross.

The transformation rule involves the following steps:
1. Initialize the output grid as a copy of the input grid.
2. Iterate through each pixel of the input grid to find potential centers of cross shapes. A cross shape is defined as a central pixel of color C1 surrounded orthogonally (up, down, left, right) by pixels of color C2 (where C1 != C2 and C1, C2 != 0), and diagonally by white pixels (color 0).
3. For each identified cross center at (row, col) with color C1:
    a. Define the eight knight's move offsets relative to the center: (-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1).
    b. For each offset (dr, dc), calculate the target coordinates (new_row, new_col) = (row + dr, col + dc).
    c. If the target coordinates are within the grid boundaries, set the pixel at (new_row, new_col) in the output grid to color C1.
4. Return the modified output grid.
"""

import numpy as np

def _is_within_bounds(r, c, height, width):
  """Checks if coordinates (r, c) are within the grid dimensions."""
  return 0 <= r < height and 0 <= c < width

def _is_cross_center(grid, r, c, height, width):
  """
  Checks if the pixel at (r, c) is the center of a valid cross pattern.
  Returns the center color C1 if it is, otherwise None.
  """
  center_color_c1 = grid[r, c]
  if center_color_c1 == 0: # Center cannot be white
    return None

  cardinal_offsets = [(-1, 0), (1, 0), (0, -1), (0, 1)]
  diagonal_offsets = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

  arm_color_c2 = None

  # Check cardinal neighbors
  for dr, dc in cardinal_offsets:
    nr, nc = r + dr, c + dc
    if not _is_within_bounds(nr, nc, height, width):
      return None # Cross must be fully formed within bounds for arms

    neighbor_color = grid[nr, nc]
    if neighbor_color == 0 or neighbor_color == center_color_c1:
        return None # Arms cannot be white or same color as center

    if arm_color_c2 is None:
      arm_color_c2 = neighbor_color # Set the expected arm color
    elif neighbor_color != arm_color_c2:
      return None # All arms must have the same color C2

  if arm_color_c2 is None: # Should not happen if loop ran, but safety check
      return None

  # Check diagonal neighbors (must be white)
  for dr, dc in diagonal_offsets:
    nr, nc = r + dr, c + dc
    if _is_within_bounds(nr, nc, height, width):
      if grid[nr, nc] != 0:
        return None # Diagonal neighbors must be white

  # If all checks pass, it's a valid cross center
  return center_color_c1


def transform(input_grid):
    """
    Applies the cross pattern knight's move transformation.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the transformed output grid.
    """
    # Convert input list of lists to numpy array for easier slicing and manipulation
    input_grid_np = np.array(input_grid, dtype=int)
    height, width = input_grid_np.shape

    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid_np)

    # Define knight's move offsets
    knight_moves = [
        (-2, -1), (-2, 1),
        (-1, -2), (-1, 2),
        (1, -2), (1, 2),
        (2, -1), (2, 1)
    ]

    # Iterate through each cell to find potential cross centers
    for r in range(height):
        for c in range(width):
            # Check if the current cell is a center of a cross pattern
            center_color = _is_cross_center(input_grid_np, r, c, height, width)

            if center_color is not None:
                # If it is a cross center, apply knight's moves
                for dr, dc in knight_moves:
                    nr, nc = r + dr, c + dc

                    # Check if the target coordinate is within bounds
                    if _is_within_bounds(nr, nc, height, width):
                        # Place the center color at the knight's move position
                        # Note: This overwrites whatever might be there, consistent with examples
                        output_grid[nr, nc] = center_color

    # Return the modified grid (convert back to list of lists if necessary,
    # but numpy array is often preferred)
    return output_grid.tolist() # Convert back to list of lists as per standard ARC format