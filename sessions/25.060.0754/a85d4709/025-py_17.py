import numpy as np

def compare_grids(grid1, grid2):
    """Compares two grids and returns a report of differences."""
    if grid1.shape != grid2.shape:
        return "Different shapes: {} vs {}".format(grid1.shape, grid2.shape)
    diff = grid1 != grid2
    if not np.any(diff):
        return "Grids are identical."
    diff_indices = np.where(diff)
    report = "Differences:\n"
    for i in range(len(diff_indices[0])):
        row, col = diff_indices[0][i], diff_indices[1][i]
        report += "  Pixel at ({}, {}): {} vs {}\n".format(row, col, grid1[row, col], grid2[row, col])
    return report