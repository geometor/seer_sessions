import numpy as np

def compare_grids(grid1, grid2):
    """Compares two grids and returns the coordinates and values where they differ."""
    if grid1.shape != grid2.shape:
        return "Grids have different shapes"

    diff_coords = []
    rows, cols = grid1.shape
    for r in range(rows):
        for c in range(cols):
            if grid1[r, c] != grid2[r, c]:
                diff_coords.append(((r, c), grid1[r, c], grid2[r, c]))
    return diff_coords

# iterate through each training example, and compare the expected output to the
#  result of the transform function

for i, example in enumerate(train):
    input_grid = example['input']
    expected_output_grid = example['output']
    actual_output_grid = transform(np.array(input_grid))
    differences = compare_grids(expected_output_grid, actual_output_grid)

    print(f"Example {i+1}:")
    if isinstance(differences, str):
        print(differences)  # Print error message if shapes are different
    elif len(differences) == 0:
        print("  No differences found.")
    else:
        print(f"  {len(differences)} differences found:")
        for diff in differences:
            coord, expected, actual = diff
            print(f"    Coordinate: {coord}, Expected: {expected}, Actual: {actual}")
    print("-" * 20)