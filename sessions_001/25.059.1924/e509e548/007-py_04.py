import numpy as np

def code_execution(input_grid, output_grid, transformed_grid):
    """
    Analyzes and provides metrics about the input, output, and transformed grids.

    Args:
        input_grid:  The original input grid.
        output_grid: The expected output grid.
        transformed_grid: The grid produced by the `transform` function.

    Returns:
        A dictionary containing relevant metrics and observations.
    """

    results = {}

    # Basic Grid Properties
    results['input_shape'] = input_grid.shape
    results['output_shape'] = output_grid.shape
    results['transformed_shape'] = transformed_grid.shape

    # Check for overall transformation correctness.
    results['correct_transformation'] = np.array_equal(output_grid, transformed_grid)

    # Component analysis for the input grid (specifically focusing on color 3 - green)
    input_green_components = find_connected_components(input_grid, 3)
    results['input_green_components_count'] = len(input_green_components)
    results['input_green_component_sizes'] = [len(c) for c in input_green_components]
    results['input_unique_colors'] = np.unique(input_grid).tolist()

    # Component analysis for the expected output grid
    output_green_components = find_connected_components(output_grid, 3)
    results['output_green_components_count'] = len(output_green_components)  # Usually should be 0 if green is fully transformed.
    results['output_green_component_sizes'] = [len(c) for c in output_green_components]

    output_blue_components = find_connected_components(output_grid, 1)
    results['output_blue_components_count'] = len(output_blue_components)
    results['output_blue_component_sizes'] = [len(c) for c in output_blue_components]
    
    output_magenta_components = find_connected_components(output_grid, 6)
    results['output_magenta_components_count'] = len(output_magenta_components)
    results['output_magenta_component_sizes'] = [len(c) for c in output_magenta_components]

    results['output_unique_colors'] = np.unique(output_grid).tolist()
    

    # Changes - Focus on pixels that changed color
    changes = []
    for r in range(input_grid.shape[0]):
        for c in range(input_grid.shape[1]):
            if input_grid[r,c] != output_grid[r,c]:
                changes.append({
                    'location': (r, c),
                    'original_color': int(input_grid[r, c]),
                    'new_color': int(output_grid[r, c])
                })
    results['changes'] = changes

    return results


def find_connected_components(grid, color):
    """
    Finds connected components of a specific color in a grid.

    Args:
        grid: The input grid (2D numpy array).
        color: The color to find connected components of.

    Returns:
        A list of sets, where each set contains the (row, col) coordinates of a connected component.
    """
    visited = set()
    components = []

    def dfs(row, col, current_component):
        if (row, col) in visited or not (0 <= row < grid.shape[0] and 0 <= col < grid.shape[1]) or grid[row, col] != color:
            return
        visited.add((row, col))
        current_component.add((row, col))
        # Check adjacent cells (up, down, left, right)
        dfs(row + 1, col, current_component)
        dfs(row - 1, col, current_component)
        dfs(row, col + 1, current_component)
        dfs(row, col - 1, current_component)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == color and (row, col) not in visited:
                current_component = set()
                dfs(row, col, current_component)
                components.append(current_component)
    return components

# Example data provided (assuming these are defined elsewhere)
# These need to be numpy arrays for the functions to work.

input_grid1 = np.array([[5, 0, 5, 5, 5, 5, 5, 5, 0, 0],
                       [0, 0, 5, 5, 5, 5, 5, 0, 0, 0],
                       [0, 5, 5, 5, 5, 5, 0, 0, 0, 0],
                       [5, 5, 5, 5, 5, 0, 0, 0, 0, 0],
                       [5, 5, 5, 5, 0, 0, 0, 0, 0, 0],
                       [5, 5, 5, 0, 0, 0, 0, 0, 0, 0],
                       [5, 5, 5, 0, 0, 0, 0, 0, 0, 0],
                       [5, 5, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
                       [0, 0, 0, 0, 0, 0, 0, 0, 3, 3]])

output_grid1 = np.array([[5, 0, 5, 5, 5, 5, 5, 5, 0, 0],
                        [0, 0, 5, 5, 5, 5, 5, 0, 0, 0],
                        [0, 5, 5, 5, 5, 5, 0, 0, 0, 0],
                        [5, 5, 5, 5, 5, 0, 0, 0, 0, 0],
                        [5, 5, 5, 5, 0, 0, 0, 0, 0, 0],
                        [5, 5, 5, 0, 0, 0, 0, 0, 0, 0],
                        [5, 5, 5, 0, 0, 0, 0, 0, 0, 0],
                        [5, 5, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                        [0, 0, 0, 0, 0, 0, 0, 0, 6, 6]])
transformed_grid1 = transform(input_grid1)

input_grid2 = np.array([[5, 0, 5, 5, 5, 5, 5, 5, 0, 0, 3, 3, 3],
                       [0, 0, 5, 5, 5, 5, 5, 0, 0, 0, 3, 3, 3],
                       [0, 5, 5, 5, 5, 5, 0, 0, 0, 0, 0, 0, 0],
                       [5, 5, 5, 5, 5, 0, 0, 0, 0, 0, 0, 0],
                       [5, 5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0],
                       [5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 0, 0]])
output_grid2 = np.array([[5, 0, 5, 5, 5, 5, 5, 5, 0, 0, 6, 6, 6],
                        [0, 0, 5, 5, 5, 5, 5, 0, 0, 0, 6, 6, 6],
                        [0, 5, 5, 5, 5, 5, 0, 0, 0, 0, 0, 0, 0],
                        [5, 5, 5, 5, 5, 0, 0, 0, 0, 0, 0, 0],
                        [5, 5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0],
                        [5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 6, 6, 0, 0]])
transformed_grid2 = transform(input_grid2)

input_grid3 = np.array([[3, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [3, 3, 0, 0, 0, 0, 0, 0, 0, 0],
                       [3, 3, 3, 0, 0, 0, 0, 0, 0, 0],
                       [3, 3, 3, 3, 0, 0, 0, 0, 0, 0],
                       [3, 3, 3, 3, 3, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
output_grid3 = np.array([[6, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [6, 6, 0, 0, 0, 0, 0, 0, 0, 0],
                        [6, 6, 6, 0, 0, 0, 0, 0, 0, 0],
                        [6, 6, 6, 6, 0, 0, 0, 0, 0, 0],
                        [6, 6, 6, 6, 6, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])

transformed_grid3 = transform(input_grid3)


results1 = code_execution(input_grid1, output_grid1, transformed_grid1)
results2 = code_execution(input_grid2, output_grid2, transformed_grid2)
results3 = code_execution(input_grid3, output_grid3, transformed_grid3)

print("Example 1 Results:")
print(results1)
print("\nExample 2 Results:")
print(results2)
print("\nExample 3 Results:")
print(results3)