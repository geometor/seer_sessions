import numpy as np

def analyze_grid_transformations(task_data):
    analysis = {}
    for phase in ["train", "test"]:
        analysis[phase] = []
        for example_num, example in enumerate(task_data[phase]):
            input_grid = np.array(example["input"])
            output_grid = np.array(example["output"])

            input_dims = input_grid.shape
            output_dims = output_grid.shape

            # Check for consistent colors and their positions
            unique_input_colors = np.unique(input_grid)
            unique_output_colors = np.unique(output_grid)
            
            color_positions = {}
            for color in unique_input_colors:
                color_positions[color] = np.where(input_grid == color)
            
            first_row_input = input_grid[0].tolist()
            last_row_input = input_grid[-1].tolist()

            first_col_input = input_grid[:,0].tolist()
            last_col_input = input_grid[:,-1].tolist()
            
            first_row_output = output_grid[0].tolist()
            last_row_output = output_grid[-1].tolist()

            first_col_output = output_grid[:,0].tolist()
            last_col_output = output_grid[:,-1].tolist()            

            analysis[phase].append({
                "example_num": example_num + 1,
                "input_dims": input_dims,
                "output_dims": output_dims,
                "unique_input_colors": unique_input_colors.tolist(),
                "unique_output_colors": unique_output_colors.tolist(),
                "color_positions": color_positions,
                "first_row_input": first_row_input,
                "first_row_output" : first_row_output,
                "last_row_input": last_row_input,
                "last_row_output" : last_row_output,
                "first_col_input": first_col_input,
                "first_col_output" : first_col_output,
                "last_col_input": last_col_input,
                "last_col_output" : last_col_output,
            })
    return analysis

task_data = {
    "train": [
        {
            "input": [
                [5, 0, 5, 0, 5],
                [0, 5, 0, 5, 0],
                [5, 0, 5, 0, 5],
                [0, 5, 0, 5, 0]
            ],
            "output": [
                [5, 0, 5, 0],
                [0, 5, 0, 5],
                [5, 0, 5, 0],
                [0, 5, 0, 5],
                [5, 0, 5, 0]
            ]
        },
                        {
            "input": [
                [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
            ],
            "output": [
                [8], [8], [8], [8], [8], [8], [8], [8], [8], [8], [8], [8]
            ]
        },

        {
            "input": [
                [7, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [7, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [7, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [7, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [7, 0, 0, 0, 0, 0, 0, 0, 0, 0],

            ],
            "output": [
                [7, 7, 7, 7, 7],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
            ]
        }
    ],
    "test": [
        {
            "input": [
                [1, 1, 1, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1, 1, 8],
            ],
            "output": [
                [1, 1],
                [1, 1],
                [1, 1],
                [1, 1],
                [1, 1],
                [1, 1],
                [1, 1],
                [1, 8],
            ]
        }
    ]
}
analysis = analyze_grid_transformations(task_data)
print(analysis)