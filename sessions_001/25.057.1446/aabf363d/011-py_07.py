import numpy as np

def count_pixels(grid):
    """Counts the occurrences of each pixel value in the grid."""
    unique, counts = np.unique(grid, return_counts=True)
    return dict(zip(unique, counts))

def report_diffs(grid1, grid2):
    """
    Reports the differences between two grids.
    """
    if grid1.shape != grid2.shape:
        return "Different shapes: {} vs {}".format(grid1.shape, grid2.shape)

    diffs = grid1 != grid2
    num_diffs = np.sum(diffs)

    if num_diffs == 0:
      return "No differences"

    # Get coordinates of differences
    diff_coords = np.where(diffs)
    diff_report = {}

    # Iterate through the coordinates and collect the before and after values
    for i in range(len(diff_coords[0])):
      row = diff_coords[0][i]
      col = diff_coords[1][i]
      before = grid1[row,col]
      after = grid2[row,col]
      if (before, after) in diff_report:
        diff_report[(before,after)] += 1
      else:
        diff_report[(before,after)] = 1

    return diff_report