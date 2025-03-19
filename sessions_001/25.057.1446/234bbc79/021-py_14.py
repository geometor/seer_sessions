import numpy as np

def get_grid_info(grid):
    """Collects information about a grid."""
    
    rows, cols = grid.shape
    unique_colors = np.unique(grid)
    color_counts = {color: np.count_nonzero(grid == color) for color in unique_colors}
    return {
        "rows": rows,
        "cols": cols,
        "unique_colors": unique_colors.tolist(),
        "color_counts": color_counts,
    }

def analyze_example(input_grid, output_grid, predicted_grid):
   
    input_info = get_grid_info(input_grid)
    output_info = get_grid_info(output_grid)
    predicted_info = get_grid_info(predicted_grid)

    comparison = input_grid == output_grid
    changes = np.where(comparison == False)
    num_changes = len(changes[0])
    correct_changes = np.where(predicted_grid == output_grid)
    incorrect_changes = np.where(predicted_grid != output_grid)

    return {
        'input': input_info,
        'output': output_info,
        'predicted': predicted_info,
        'changes' : num_changes,
        'correct' : len(correct_changes[0]),
        'incorrect' : len(incorrect_changes[0])
    }


input_grid1 = np.array([[8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 1, 1, 1, 1, 1, 1, 1, 8], [8, 1, 1, 1, 1, 1, 1, 1, 8], [8, 1, 1, 1, 1, 1, 1, 1, 8], [8, 1, 1, 1, 1, 1, 2, 2, 8], [8, 1, 1, 1, 1, 1, 2, 5, 8], [8, 1, 1, 1, 1, 1, 1, 1, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8]])
output_grid1 = np.array([[8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 1, 1, 1, 1, 1, 1, 1, 8], [8, 1, 1, 1, 1, 1, 1, 1, 8], [8, 1, 1, 1, 1, 1, 1, 1, 8], [8, 1, 1, 1, 1, 1, 2, 0, 8], [8, 1, 1, 1, 1, 1, 0, 0, 8], [8, 1, 1, 1, 1, 1, 1, 1, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8]])
predicted_grid1 = transform(input_grid1)

input_grid2 = np.array([[8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 5, 2, 8, 1, 1, 8, 1, 1, 1, 8], [8, 2, 8, 8, 1, 1, 8, 1, 1, 1, 8], [8, 8, 8, 8, 1, 1, 8, 1, 1, 1, 8], [8, 8, 8, 8, 1, 1, 8, 1, 1, 1, 8], [8, 8, 8, 8, 1, 1, 8, 1, 1, 1, 8], [8, 8, 8, 8, 1, 1, 8, 1, 1, 1, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]])
output_grid2 = np.array([[8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 0, 0, 8, 1, 1, 8, 1, 1, 1, 8], [8, 0, 8, 8, 1, 1, 8, 1, 1, 1, 8], [8, 8, 8, 8, 1, 1, 8, 1, 1, 1, 8], [8, 8, 8, 8, 1, 1, 8, 1, 1, 1, 8], [8, 8, 8, 8, 1, 1, 8, 1, 1, 1, 8], [8, 8, 8, 8, 1, 1, 8, 1, 1, 1, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]])
predicted_grid2 = transform(input_grid2)

input_grid3 = np.array([[8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 1, 1, 8, 8, 8], [8, 8, 8, 1, 1, 8, 8, 8], [8, 8, 8, 1, 1, 8, 8, 8], [8, 8, 8, 1, 1, 8, 8, 8], [8, 8, 8, 1, 1, 8, 8, 8], [8, 8, 8, 5, 2, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8]])
output_grid3 = np.array([[8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 1, 1, 8, 8, 8], [8, 8, 8, 1, 1, 8, 8, 8], [8, 8, 8, 1, 1, 8, 8, 8], [8, 8, 8, 1, 1, 8, 8, 8], [8, 8, 8, 1, 1, 8, 8, 8], [8, 8, 8, 0, 0, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8]])
predicted_grid3 = transform(input_grid3)

analysis1 = analyze_example(input_grid1, output_grid1, predicted_grid1)
analysis2 = analyze_example(input_grid2, output_grid2, predicted_grid2)
analysis3 = analyze_example(input_grid3, output_grid3, predicted_grid3)

print("Analysis 1:", analysis1)
print("Analysis 2:", analysis2)
print("Analysis 3:", analysis3)