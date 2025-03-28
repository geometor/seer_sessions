import numpy as np

"""
Initialize the output_grid as an identical copy of the input_grid.
Scan the input_grid to find all occurrences of a specific "cross" pattern. A cross is defined by:
    *   A central pixel at coordinates (r, c) with color C1, where C1 is not white (0).
    *   The four cardinal neighbors (up, down, left, right) of the center pixel all have the same color C2, where C2 is not white (0) and C1 is different from C2.
    *   The four diagonal neighbors of the center pixel are all white (0) (checking only those neighbors that fall within the grid boundaries).
For each identified cross pattern with center (r, c), center color C1, and arm color C2:
    a.  Define the set of eight diagonal offsets: D = {(-2, -2), (-2, 2), (-1, -1), (-1, 1), (1, -1), (1, 1), (2, -2), (2, 2)}.
    b.  For each offset (dr, dc) in D:
        i.  Calculate the target coordinates (target_r, target_c) = (r + dr, c + dc).
        ii. If (target_r, target_c) is within the grid bounds, update the output_grid at (target_r, target_c) to color C1 (overwriting any previous color).
    c.  Define the set of four extended cardinal offsets: E = {(-2, 0), (2, 0), (0, -2), (0, 2)}.
    d.  For each offset (dr, dc) in E:
        i.  Calculate the target coordinates (target_r, target_c) = (r + dr, c + dc).
        ii. If (target_r, target_c) is within the grid bounds, update the output_grid at (target_r, target_c) to color C2 (overwriting any previous color).
After processing all identified crosses, return the final output_grid.
"""

def _is_within_bounds(r, c, height, width):
  """Checks if coordinates (r, c) are within the grid dimensions."""
  return 0 <= r < height and 0 <= c < width

def _find_crosses(grid, height, width):
  """
  Finds all cross patterns in the grid.

  Yields:
      tuple: (center_row, center_col, center_color, arm_color)
             for each valid cross found.
  """
  cardinal_offsets = [(-1, 0), (1, 0), (0, -1), (0, 1)] # Up, Down, Left, Right
  diagonal_offsets = [(-1, -1), (-1, 1), (1, -1), (1, 1)] # Diagonals

  # Iterate through potential center cells (can't be on the very edge for a full cross)
  for r in range(1, height - 1):
      for c in range(1, width - 1):
          center_color_c1 = grid[r, c]

          # 1. Center must not be white
          if center_color_c1 == 0:
              continue

          arm_color_c2 = None
          valid_cardinal = True

          # 2. Check cardinal neighbors (arms)
          for dr, dc in cardinal_offsets:
              nr, nc = r + dr, c + dc
              neighbor_color = grid[nr, nc]

              # Arms must not be white and not same color as center
              if neighbor_color == 0 or neighbor_color == center_color_c1:
                  valid_cardinal = False
                  break

              if arm_color_c2 is None:
                  arm_color_c2 = neighbor_color # Set expected arm color C2
              elif neighbor_color != arm_color_c2:
                  valid_cardinal = False # All arms must have same color C2
                  break

          if not valid_cardinal or arm_color_c2 is None:
              continue # Move to next potential center if cardinal checks fail

          # 3. Check diagonal neighbors (must be white)
          valid_diagonal = True
          for dr, dc in diagonal_offsets:
              nr, nc = r + dr, c + dc
              # Only check if within bounds, edge crosses might not have all diagonals
              if _is_within_bounds(nr, nc, height, width):
                  if grid[nr, nc] != 0:
                      valid_diagonal = False
                      break # Diagonal neighbor is not white

          if valid_diagonal:
              # If all checks pass, yield the cross details needed for placement
              yield r, c, center_color_c1, arm_color_c2


def transform(input_grid):
    """
    Applies the transformation: finds crosses and places the center color
    at specific diagonal offsets and the arm color at extended cardinal offsets.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    # Convert input to numpy array for easier manipulation
    input_grid_np = np.array(input_grid, dtype=int)
    height, width = input_grid_np.shape

    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid_np)

    # Define the required offsets from the center
    diagonal_placement_offsets = [
        (-2, -2), (-2, 2),
        (-1, -1), (-1, 1),
        (1, -1), (1, 1),
        (2, -2), (2, 2)
    ]
    extended_cardinal_placement_offsets = [
        (-2, 0), (2, 0),
        (0, -2), (0, 2)
    ]

    # Find all cross patterns in the input grid
    # Now includes arm_color_c2
    crosses = list(_find_crosses(input_grid_np, height, width))

    # Process each found cross
    for center_r, center_c, center_color_c1, arm_color_c2 in crosses:
        # Apply the 8 diagonal placement offsets using the center color C1
        for dr, dc in diagonal_placement_offsets:
            target_r, target_c = center_r + dr, center_c + dc

            # Check if the target coordinate is within bounds
            if _is_within_bounds(target_r, target_c, height, width):
                # Place the center color C1 at the target destination
                output_grid[target_r, target_c] = center_color_c1

        # Apply the 4 extended cardinal placement offsets using the arm color C2
        for dr, dc in extended_cardinal_placement_offsets:
            target_r, target_c = center_r + dr, center_c + dc

            # Check if the target coordinate is within bounds
            if _is_within_bounds(target_r, target_c, height, width):
                # Place the arm color C2 at the target destination
                output_grid[target_r, target_c] = arm_color_c2

    # Convert the final numpy array back to a list of lists
    return output_grid.tolist()