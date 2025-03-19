import numpy as np

def get_grid_info(grid):
    """Returns grid dimensions and color counts."""
    dimensions = grid.shape
    unique, counts = np.unique(grid, return_counts=True)
    color_counts = dict(zip(unique, counts))
    return dimensions, color_counts

#Example Usage with made up data because task is not defined
train_examples = [
    (np.array([[5, 0], [0, 5]]), np.array([[2, 4], [4, 2]])),
    (np.array([[5, 0, 5], [0, 5, 0]]), np.array([[2, 4, 2], [4, 2, 4]])),
    (np.array([[5,5,5],[0,0,0],[5,0,5]]), np.array([[2,2,2],[4,4,4],[2,4,2]])),
]

for i, (input_grid, output_grid) in enumerate(train_examples):
    input_dims, input_colors = get_grid_info(input_grid)
    output_dims, output_colors = get_grid_info(output_grid)

    print(f"Example {i+1}:")
    print(f"  Input Dimensions: {input_dims}")
    print(f"  Input Colors: {input_colors}")
    print(f"  Output Dimensions: {output_dims}")
    print(f"  Output Colors: {output_colors}")

    # Check if dimensions match
    assert input_dims == output_dims, f"Dimensions mismatch in example {i+1}"

    # Check color substitution
    for color, count in input_colors.items():
        if color == 5:  # Gray
            assert output_colors.get(2, 0) == count, f"Gray substitution error in example {i+1}"
        elif color == 0: # White
            assert output_colors.get(4, 0) == count, f"White substitution error in example {i+1}"
        else:
             assert output_colors.get(color,0) == count, f"Unexpected color error in example {i+1}"
    print("----")