import numpy as np

def analyze_example(example):
    input_grid = np.array(example['input'])
    output_grid = np.array(example['output'])

    input_non_white = input_grid[input_grid != 0]
    output_non_white = output_grid[output_grid != 0]

    input_unique, input_counts = np.unique(input_non_white, return_counts=True)
    output_unique, output_counts = np.unique(output_non_white, return_counts=True)
    
    input_colors = {color: count for color, count in zip(input_unique, input_counts)}
    output_colors = {color: count for color, count in zip(output_unique, output_counts)}
    
    input_height, input_width = input_grid.shape
    output_height, output_width = output_grid.shape
    
    print(f"  Input Shape: {input_grid.shape}")
    print(f"  Output Shape: {output_grid.shape}")
    print(f"  Input Colors: {input_colors}")
    print(f"  Output Colors: {output_colors}")
    print(f"  Input has single row pattern: {input_height == np.count_nonzero(np.any(input_grid != 0, axis=1))}")
    print(f"  Output has single row pattern: {output_height == np.count_nonzero(np.any(output_grid != 0, axis=1))}")
    
    # Additional Analysis
    if input_height == np.count_nonzero(np.any(input_grid != 0, axis=1)):
      first_non_white_row_input = np.where(np.any(input_grid != 0, axis=1))[0][0]
      print(f"  Index of the first non-white row in input: {first_non_white_row_input}")
      
      input_row = input_grid[first_non_white_row_input]
      input_row_non_white = input_row[input_row != 0]
      print(f"  Input non-white row: {input_row_non_white}")

    if output_height == np.count_nonzero(np.any(output_grid != 0, axis=1)):
      first_non_white_row_output = np.where(np.any(output_grid != 0, axis=1))[0][0]
      print(f"  Index of the first non-white row in output: {first_non_white_row_output}")

      output_row = output_grid[first_non_white_row_output]
      output_row_non_white = output_row[output_row != 0]
      print(f"  Output non-white row: {output_row_non_white}")

task_data = {
    "train": [
        {
            "input": [
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 2, 3, 2, 3, 2, 3],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
            ],
            "output": [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            ],
        },
        {
            "input": [
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [2, 3, 2, 3, 2, 3, 2, 3],
            ],
            "output": [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3],
            ],
        },
        {
            "input": [
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [2, 3, 2, 3, 2, 3, 2],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
            ],
            "output": [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            ],
        },
    ]
}
for i, example in enumerate(task_data['train']):
    print(f"Example {i+1}:")
    analyze_example(example)