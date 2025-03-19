import numpy as np
from typing import List, Tuple

def transform(input_grid):
    """
    Transforms the input grid by applying a color substitution cipher.
    """
    # Initialize the output grid with the same dimensions as the input grid.
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # Iterate through each pixel of the input grid.
    for i in range(height):
        for j in range(width):
            # Apply the color mapping.
            if input_grid[i, j] == 5:
                output_grid[i, j] = 1
            elif input_grid[i, j] == 8:
                output_grid[i, j] = 9
            elif input_grid[i, j] == 6:
                output_grid[i, j] = 2

    return output_grid

def compare_grids(grid1, grid2):
    """
    Compares two grids and returns a list of differences.
    """
    if grid1.shape != grid2.shape:
        return "Grids have different shapes"

    differences = []
    height, width = grid1.shape
    for i in range(height):
        for j in range(width):
            if grid1[i, j] != grid2[i, j]:
                differences.append(((i, j), grid1[i, j], grid2[i, j]))
    return differences

def calculate_accuracy(grid1, grid2):
    """
    Calculates the accuracy of the transformation.
    """
    if grid1.shape != grid2.shape:
        return "Grids have different shapes"
    
    total_pixels = grid1.size
    correct_pixels = np.sum(grid1 == grid2)
    accuracy = (correct_pixels / total_pixels) * 100
    return accuracy


# now using the training examples, test the function
train = [
    (np.array([[5, 8, 6], [5, 5, 8], [8, 6, 6]]), np.array([[1, 9, 2], [1, 1, 9], [9, 2, 2]])),
    (np.array([[8, 5, 5], [8, 8, 6], [5, 6, 6]]), np.array([[9, 1, 1], [9, 9, 2], [1, 2, 2]])),
    (np.array([[8, 6, 5], [6, 6, 8], [5, 8, 5]]), np.array([[9, 2, 1], [2, 2, 9], [1, 9, 1]])),
    (np.array([[6, 8, 6, 8, 5], [8, 5, 8, 5, 6], [6, 6, 5, 6, 5]]), np.array([[2, 9, 2, 9, 1], [9, 1, 9, 1, 2], [2, 2, 1, 2, 1]])),
    (np.array([[5, 5, 6, 8, 8], [5, 5, 8, 8, 6], [8, 5, 6, 5, 6]]), np.array([[1, 1, 2, 9, 9], [1, 1, 9, 9, 2], [9, 1, 2, 1, 2]]))
]
results = []
for i, (input_grid, output_grid) in enumerate(train):
    transformed_grid = transform(input_grid)
    differences = compare_grids(transformed_grid, output_grid)
    accuracy = calculate_accuracy(transformed_grid, output_grid)
    results.append(
        {
            'example': i,
            'accuracy': accuracy,
            'differences': differences
        }
    )
for r in results:
    print(r)
