import numpy as np

# Provided input and output grids for all training examples
train_task = {
    "train": [
        {
            "input": np.array([
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]
            ]),
            "output": np.array([
                [0, 0, 0],
                [0, 0, 0],
                [0, 0, 0],
                [0, 8, 8],
                [0, 0, 0]
            ])
        },
        {
            "input": np.array([
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 1, 0, 0, 0, 0, 0]
            ]),
            "output": np.array([
                [0, 0, 0],
                [0, 0, 0],
                [0, 0, 0],
                [8, 8, 0],
                [0, 0, 0]
            ])
        },
        {
           "input": np.array([
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]
           ]),
            "output": np.array([
               [0, 0, 0],
               [0, 0, 0],
               [0, 0, 0],
               [0, 0, 8],
               [0, 0, 8]
            ])
        }
    ]
}

def analyze_examples(task):
    results = []
    for example in task["train"]:
        input_grid = example["input"]
        output_grid = example["output"]
        input_rows, input_cols = input_grid.shape
        output_rows, output_cols = output_grid.shape

        # Find blue stripe (column with blue pixels)
        blue_cols = []
        for j in range(input_cols):
            if np.any(input_grid[:, j] == 1):
                blue_cols.append(j)

        # Get the bottom two blue pixels in the column
        bottom_two_indices = []
        if blue_cols: #check that blue_cols isn't empty
            for col in blue_cols:
                blue_indices = np.where(input_grid[:, col] == 1)[0]
                if len(blue_indices) >= 2:
                  bottom_two_indices.append( (blue_indices[-2], col)) # row, col
                  bottom_two_indices.append( (blue_indices[-1], col))
        results.append({
            "input_shape": (input_rows, input_cols),
            "output_shape": (output_rows, output_cols),
            "blue_columns": blue_cols,
            'num_blue_cols': len(blue_cols),
            "bottom_two_indices": bottom_two_indices
        })
    return results

results = analyze_examples(train_task)
for i, res in enumerate(results):
    print(f"Example {i+1}:")
    print(f"  Input shape: {res['input_shape']}")
    print(f"  Output shape: {res['output_shape']}")
    print(f"  Blue columns: {res['blue_columns']}")
    print(f"  Number of Blue columns: {res['num_blue_cols']}")
    print(f"  Bottom two blue pixel indices: {res['bottom_two_indices']}")
