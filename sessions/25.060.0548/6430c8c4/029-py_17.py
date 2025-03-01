import numpy as np

def compare_grids(grid1, grid2):
    """Compares two grids and returns a grid highlighting differences."""
    if grid1.shape != grid2.shape:
        return "Grids have different shapes"
    comparison = (grid1 == grid2).astype(int)
    return comparison

def analyze_results(task):
     results = []
     for example in task['train']:
        input_grid = np.array(example['input'])
        output_grid = np.array(example['output'])
        predicted_output = transform(input_grid)
        comparison = compare_grids(output_grid, predicted_output)

        input_colors = np.unique(input_grid)
        output_colors = np.unique(output_grid)
        
        #color counts:
        input_color_counts = {color: np.count_nonzero(input_grid == color) for color in input_colors}
        output_color_counts = {color: np.count_nonzero(output_grid == color) for color in output_colors}


        results.append({
            'input_colors': input_colors.tolist(),
            'output_colors': output_colors.tolist(),
            'input_color_counts': input_color_counts,
            'output_color_counts':output_color_counts,
            'comparison': comparison.tolist() if isinstance(comparison, np.ndarray) else comparison
        })
     return results
task = {
    "train": [
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 7, 7, 7, 7, 7, 0, 0], [0, 0, 0, 7, 7, 7, 7, 7, 0, 0], [0, 0, 0, 7, 7, 7, 7, 7, 0, 0], [0, 0, 0, 7, 7, 7, 7, 7, 0, 0], [0, 0, 0, 7, 7, 7, 7, 7, 0, 0], [0, 0, 0, 7, 7, 7, 7, 7, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 3, 3, 3, 3, 3, 0, 0], [0, 0, 0, 3, 3, 3, 3, 3, 0, 0], [0, 0, 0, 3, 3, 3, 3, 3, 0, 0], [0, 0, 0, 3, 3, 3, 3, 3, 0, 0], [0, 0, 0, 3, 3, 3, 3, 3, 0, 0], [0, 0, 0, 3, 3, 3, 3, 3, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
        },
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 6, 6, 6, 0, 0], [0, 0, 0, 0, 0, 6, 6, 6, 0, 0], [0, 0, 0, 0, 0, 6, 6, 6, 0, 0], [0, 0, 0, 0, 0, 6, 6, 6, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 1, 1, 0, 0], [0, 0, 0, 0, 0, 1, 1, 1, 0, 0], [0, 0, 0, 0, 0, 1, 1, 1, 0, 0], [0, 0, 0, 0, 0, 1, 1, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
        },
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 2, 2, 2, 2, 2, 2, 2, 0], [0, 2, 2, 2, 2, 2, 2, 2, 0], [0, 2, 2, 2, 2, 2, 2, 2, 0], [0, 2, 2, 2, 2, 2, 2, 2, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 8, 8, 8, 8, 8, 8, 8, 0], [0, 8, 8, 8, 8, 8, 8, 8, 0], [0, 8, 8, 8, 8, 8, 8, 8, 0], [0, 8, 8, 8, 8, 8, 8, 8, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]],
        },
		{
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 2, 2, 2, 2, 2, 2, 2, 0], [0, 2, 2, 6, 6, 6, 2, 2, 0], [0, 2, 2, 6, 6, 6, 2, 2, 0], [0, 2, 2, 2, 2, 2, 2, 2, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 8, 8, 8, 8, 8, 8, 8, 0], [0, 8, 8, 1, 1, 1, 8, 8, 0], [0, 8, 8, 1, 1, 1, 8, 8, 0], [0, 8, 8, 8, 8, 8, 8, 8, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]],
        }
    ]
}

analysis = analyze_results(task)
print(analysis)
