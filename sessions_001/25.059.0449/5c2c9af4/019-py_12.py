def compare_grids(grid1, grid2):
    """
    Compares two grids and returns a list of discrepancies.
    Each discrepancy is a tuple: (row, col, grid1_val, grid2_val)
    """
    discrepancies = []
    rows, cols = grid1.shape
    for r in range(rows):
        for c in range(cols):
            if grid1[r, c] != grid2[r, c]:
                discrepancies.append((r, c, grid1[r, c], grid2[r, c]))
    return discrepancies

# Dummy data for demonstration since I am missing the actual input and output grids.
# I will create a simple example to demonstrate the function.
input_grid = np.array([[0, 0, 0], [0, 3, 0], [3, 0, 0]])
expected_output = np.array([[0, 0, 0], [3, 3, 0], [3, 0, 0]])

current_output = transform(input_grid)
discrepancies = compare_grids(expected_output, current_output)
print(f"Discrepancies: {discrepancies}")