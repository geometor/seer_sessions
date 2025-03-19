import numpy as np

def describe_grid(grid):
    """Provides a basic description of the grid's objects."""
    unique, counts = np.unique(grid, return_counts=True)
    color_counts = dict(zip(unique, counts))
    description = ", ".join(f"{count} of color {color}" for color, count in color_counts.items())
    return description

# Example Grids (Replace with actual grids from the task)
example1_in = np.array([[0,0,0,0,0],[0,0,8,0,0],[0,4,4,4,0],[0,0,0,0,0]]) #example
example1_out = np.array([[0,0,8,0,0],[0,8,8,8,0],[0,4,4,4,0],[0,0,0,0,0]])
example2_in = np.array([[0,0,0,0,0,0],[0,0,8,0,0,0],[0,4,4,4,0,0],[0,0,0,0,0,0]])
example2_out = np.array([[0,0,8,0,0,0],[0,8,8,8,0,0],[0,4,4,4,0,0],[0,0,0,0,0,0]])
example3_in = np.array([[0,0,0,0,0,0,0],[0,0,0,8,0,0,0],[0,0,4,4,4,0,0],[0,0,0,0,0,0,0]])
example3_out = np.array([[0,0,0,8,0,0,0],[0,0,8,8,8,0,0],[0,0,4,4,4,0,0],[0,0,0,0,0,0,0]])

grids = [example1_in, example1_out, example2_in, example2_out, example3_in, example3_out]
for i, grid in enumerate(grids):
    print(f"Grid {i+1}: {describe_grid(grid)}")


def compare_grids(grid1, grid2):
    """Checks if two grids are identical."""
    return np.array_equal(grid1, grid2)

# Example usage with predicted outputs (replace with actual predictions)
predicted1_out = transform(example1_in)  # Using the original transform function
predicted2_out = transform(example2_in)
predicted3_out = transform(example3_in)

print(f"Example 1 - Correct: {compare_grids(example1_out, predicted1_out)}")
print(f"Example 2 - Correct: {compare_grids(example2_out, predicted2_out)}")
print(f"Example 3 - Correct: {compare_grids(example3_out, predicted3_out)}")
