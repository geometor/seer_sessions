def grid_properties(grid):
    height, width = grid.shape
    unique_colors = np.unique(grid)
    return {
        'height': height,
        'width': width,
        'unique_colors': unique_colors.tolist()
    }

def analyze_example(input_grid, output_grid, predicted_output):
    input_props = grid_properties(input_grid)
    output_props = grid_properties(output_grid)
    predicted_props = grid_properties(predicted_output)
    return {
        'input': input_props,
        'output': output_props,
        'predicted': predicted_props,
        'correct': np.array_equal(output_grid, predicted_output)
    }


examples = [
    # Example 1 (already analyzed - included for completeness)
     (np.array([[0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0],
       [0, 0, 2, 2, 2, 0],
       [0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0]]),
     np.array([[0, 0, 0, 0, 0, 0],
       [0, 0, 3, 3, 3, 3],
       [0, 0, 3, 3, 3, 3],
       [0, 0, 2, 2, 2, 0],
       [0, 0, 1, 0, 0, 0],
       [0, 0, 1, 0, 0, 0]])),

    # Example 2
    (np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0]]),
     np.array([[3, 3, 3, 3, 3, 3, 3, 0, 0],
               [3, 3, 3, 3, 3, 3, 3, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [1, 0, 0, 0, 0, 0, 0, 0, 0]])),
    # Example 3
        (np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
    np.array([[3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0],
               [3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]))
]

analysis_results = []
for input_grid, output_grid in examples:
  predicted_output = transform(input_grid)
  analysis_results.append(analyze_example(input_grid, output_grid, predicted_output))

analysis_results