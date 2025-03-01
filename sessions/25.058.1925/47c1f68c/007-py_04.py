import numpy as np

def describe_grid(grid):
    dims = grid.shape
    blue_present = 1 in grid
    red_pixels = [(r, c) for r in range(dims[0]) for c in range(dims[1]) if grid[r, c] == 2]
    center_row, center_col = dims[0] // 2, dims[1] // 2

    def is_cross_pixel(r, c, grid):

        # Check for at least one neighbor in both horizontal and vertical directions
        has_horizontal_neighbor = (c > 0 and grid[r, c-1] == 2) or (c < grid.shape[1]-1 and grid[r, c+1] == 2)
        has_vertical_neighbor = (r > 0 and grid[r-1, c] == 2) or (r < grid.shape[0]-1 and grid[r+1, c] == 2)
        return has_horizontal_neighbor and has_vertical_neighbor
    
    cross_present = False
    cross_size = None

    if red_pixels:
        is_cross = is_cross_pixel(center_row, center_col, grid)
        if is_cross:
          cross_present = True
          #determine cross size:
          #find first row, starting at center
          first_row = center_row
          while first_row >= 0:
            if grid[first_row, center_col] == 2:
              first_row -= 1
            else:
              break
          first_row += 1
          last_row = center_row
          while last_row < grid.shape[0]:
            if grid[last_row, center_col] == 2:
              last_row += 1
            else:
              break
          cross_size = (last_row-first_row, last_row-first_row)

    other_red = False
    if red_pixels:
      for r,c in red_pixels:
        if not is_cross_pixel(r,c,grid):
          other_red = True

    print(f"Dimensions: {dims}")
    print(f"Blue Present: {blue_present}")
    print(f"Cross Present: {cross_present}")
    print(f"Cross Size: {cross_size}")
    print(f"Other Red: {other_red}")


# Example grids -  Replace with your actual grid data
example0_in = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0], [0, 0, 0, 0, 1, 2, 1, 0, 0, 0, 0], [0, 0, 0, 0, 1, 2, 1, 0, 0, 0, 0], [0, 1, 1, 1, 2, 2, 2, 1, 1, 1, 0], [0, 1, 2, 2, 2, 2, 2, 2, 2, 1, 0], [0, 1, 1, 1, 2, 2, 2, 1, 1, 1, 0], [0, 0, 0, 0, 1, 2, 1, 0, 0, 0, 0], [0, 0, 0, 0, 1, 2, 1, 0, 0, 0, 0], [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
example0_out = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0], [0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0], [0, 0, 0, 2, 2, 2, 2, 2, 0, 0, 0], [0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0], [0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
example1_in = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0], [0, 0, 0, 0, 1, 2, 1, 0, 0, 0, 0], [0, 0, 0, 0, 1, 2, 1, 0, 0, 0, 0], [0, 1, 1, 1, 2, 2, 2, 1, 1, 1, 0], [0, 1, 2, 2, 2, 2, 2, 2, 2, 1, 0], [0, 1, 1, 1, 2, 2, 2, 1, 1, 1, 0], [0, 0, 0, 0, 1, 2, 1, 0, 0, 0, 0], [0, 0, 0, 0, 1, 2, 1, 0, 0, 0, 0], [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
example1_out = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0], [0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0], [0, 0, 0, 2, 2, 2, 2, 2, 0, 0, 0], [0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0], [0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
example2_in = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 1, 1, 0, 0, 0, 0, 0], [0, 1, 2, 1, 0, 0, 0, 5, 0], [0, 1, 2, 1, 0, 0, 5, 5, 5], [0, 1, 2, 1, 0, 0, 0, 5, 0], [0, 1, 1, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]])
example2_out = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 5, 0], [0, 0, 0, 0, 0, 0, 5, 5, 5], [0, 0, 0, 0, 0, 0, 0, 5, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]])
example3_in = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1, 2, 1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1, 2, 1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1, 2, 1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1, 2, 1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1, 2, 1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1, 2, 1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1, 2, 1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1, 2, 1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1, 2, 1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
example3_out = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])

describe_grid(example0_in)
describe_grid(example1_in)
describe_grid(example2_in)
describe_grid(example3_in)
