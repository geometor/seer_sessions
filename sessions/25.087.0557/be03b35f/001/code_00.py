import numpy as np

"""
Locate the 2x2 subgrid in the input grid that is diagonally opposite the 2x2 block of red pixels (which is always in the bottom-right). This target subgrid is the top-left 2x2 region. Extract this 2x2 subgrid. Rotate the extracted subgrid 90 degrees counter-clockwise. The resulting 2x2 grid is the final output.
"""

def rotate_subgrid_ccw(grid, top, left, height, width):
  """
  Extracts a subgrid and rotates it 90 degrees counter-clockwise.

  Args:
    grid: The input grid (numpy array).
    top: The starting row index of the subgrid.
    left: The starting column index of the subgrid.
    height: The height of the subgrid.
    width: The width of the subgrid.

  Returns:
    The rotated subgrid (numpy array).
  """
  subgrid = grid[top:top+height, left:left+width]
  # np.rot90 rotates counter-clockwise by default with k=1
  rotated_subgrid = np.rot90(subgrid, k=1)
  return rotated_subgrid

def transform(input_grid):
    """
    Transforms the input grid by extracting the top-left 2x2 subgrid
    and rotating it 90 degrees counter-clockwise.
    """
    # Convert input list of lists to a numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)

    # Define the region to extract (top-left 2x2)
    # Based on the examples, the red block confirms the pattern,
    # but the target subgrid is always the top-left 2x2.
    top = 0
    left = 0
    height = 2
    width = 2

    # Extract and rotate the specified subgrid counter-clockwise
    output_grid_np = rotate_subgrid_ccw(input_np, top, left, height, width)

    # Convert the numpy array back to a list of lists for the expected output format
    output_grid = output_grid_np.tolist()

    return output_grid