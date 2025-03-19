import numpy as np

def analyze_example(input_grid, output_grid):
    """
    Analyzes an input-output grid pair and returns metrics.
    """
    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)
    
    # Find azure lines
    vertical_line_col, horizontal_lines_row = find_azure_lines(input_grid)

    analysis = {
        "input_shape": input_grid.shape,
        "output_shape": output_grid.shape,
        "vertical_line_col": vertical_line_col,
        "horizontal_lines_row": horizontal_lines_row,
        "differences": (input_grid != output_grid).sum(),
         "input_colors": np.unique(input_grid).tolist(),
        "output_colors": np.unique(output_grid).tolist(),
    }
    
    return analysis
# Example Usage (replace with actual grids from the task):

task_data = [
    {
        "input": [
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 8, 8, 8, 8, 8, 8, 8, 0],
            [0, 8, 0, 0, 0, 0, 0, 8, 0],
            [0, 8, 0, 0, 0, 0, 0, 8, 0],
            [0, 8, 8, 8, 8, 8, 8, 8, 0],
            [0, 8, 0, 0, 0, 0, 0, 8, 0],
            [0, 8, 0, 0, 0, 0, 0, 8, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
        ],
        "output": [
            [2, 2, 2, 2, 2, 6, 6, 6, 6],
            [8, 8, 8, 8, 8, 8, 8, 8, 8],
            [8, 8, 1, 1, 1, 3, 3, 8, 8],
            [8, 8, 1, 1, 1, 3, 3, 8, 8],
            [8, 8, 8, 8, 8, 8, 8, 8, 8],
            [8, 8, 1, 1, 1, 3, 3, 8, 8],
            [8, 8, 1, 1, 1, 3, 3, 8, 8],
            [1, 1, 1, 1, 1, 1, 1, 1, 1],
        ],
    },
     {
        "input": [
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 8, 0, 0, 0, 0],
            [0, 0, 0, 0, 8, 0, 0, 0, 0],
            [0, 0, 0, 0, 8, 0, 0, 0, 0],
            [0, 8, 8, 8, 8, 8, 8, 8, 0],
            [0, 0, 0, 0, 8, 0, 0, 0, 0],
            [0, 0, 0, 0, 8, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
        ],
        "output": [
            [2, 2, 2, 2, 6, 6, 6, 6, 6],
            [2, 2, 2, 2, 8, 6, 6, 6, 6],
            [2, 2, 2, 2, 8, 6, 6, 6, 6],
            [2, 2, 2, 2, 8, 6, 6, 6, 6],
            [8, 8, 8, 8, 8, 8, 8, 8, 8],
            [1, 1, 1, 1, 8, 1, 1, 1, 1],
            [1, 1, 1, 1, 8, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1],
        ],
    },
  {
        "input": [
          [8, 8, 8, 8, 8, 8],
          [8, 0, 0, 0, 0, 8],
          [8, 0, 0, 0, 0, 8],
          [8, 8, 8, 8, 8, 8]
        ],
        "output": [
           [8, 8, 8, 8, 8, 8],
           [8, 1, 1, 1, 1, 8],
           [8, 1, 1, 1, 1, 8],
           [8, 8, 8, 8, 8, 8]
        ],
    },
]

analysis_results = [analyze_example(ex["input"], ex["output"]) for ex in task_data]
print(analysis_results)
