import numpy as np

def get_grid_properties(grid):
    """Calculates properties of a grid."""
    return {
        'shape': grid.shape,
        'size': grid.size,
        'unique_colors': np.unique(grid).tolist(),
        'max_color': np.max(grid),
        'min_color': np.min(grid),
     }

def compare_grids(input_grid, output_grid):
    """Compares properties of input and output grids."""
    input_props = get_grid_properties(input_grid)
    output_props = get_grid_properties(output_grid)

    comparison = {
        'shape_match': input_props['shape'] == output_props['shape'],
        'size_match': input_props['size'] == output_props['size'],
        'unique_colors_match': input_props['unique_colors'] == output_props['unique_colors'],
        'max_color_match' : input_props['max_color'] == output_props['max_color'],
        'min_color_match' : input_props['min_color'] == output_props['min_color']

    }
    return comparison
#Dummy data
input_grid1 = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
output_grid1 = np.array([[9, 8, 7], [6, 5, 4], [3, 2, 1]])

input_grid2 = np.array([[0, 0, 5], [0, 0, 0], [5, 0, 0]])
output_grid2 = np.array([[0, 0, 5], [0, 0, 0], [5, 0, 0]])

input_grid3 = np.array([[1, 1, 1], [1, 2, 1], [1, 1, 1]])
output_grid3 = np.array([[1, 1, 1], [1, 2, 1], [1, 1, 1]])
# Compare
comparison1 = compare_grids(input_grid1, output_grid1)
comparison2 = compare_grids(input_grid2, output_grid2)
comparison3 = compare_grids(input_grid3, output_grid3)


print(f"Comparison 1: {comparison1}")
print(f"Comparison 2: {comparison2}")
print(f"Comparison 3: {comparison3}")

