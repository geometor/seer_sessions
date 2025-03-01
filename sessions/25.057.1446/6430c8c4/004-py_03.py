import numpy as np

# Example Data (from the prompt)
train_examples = [
    {
        "input": np.array([
            [7, 7, 7, 7, 1, 1, 1, 1],
            [7, 7, 7, 7, 1, 1, 1, 1],
            [7, 7, 7, 7, 1, 1, 1, 1],
            [7, 7, 7, 7, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
        ]),
        "output": np.array([
            [3, 3, 3, 3],
            [3, 3, 3, 3],
            [3, 3, 3, 3],
            [3, 3, 3, 3],
        ]),
        "result": "success",
    },
    {
        "input": np.array([
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 7, 7, 7, 7, 1, 1],
            [1, 1, 7, 7, 7, 7, 1, 1],
            [1, 1, 7, 7, 7, 7, 1, 1],
            [1, 1, 7, 7, 7, 7, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
        ]),
        "output": np.array([
            [0, 0, 0, 0],
            [0, 3, 3, 3],
            [0, 3, 3, 3],
            [0, 3, 3, 3],

        ]),
        "result": "success",
    },
     {
        "input": np.array([
            [1, 1, 1, 1, 1, 1, 1, 1, 7, 7],
            [1, 1, 1, 1, 1, 1, 1, 1, 7, 7],
            [1, 1, 1, 1, 1, 1, 1, 1, 7, 7],
            [1, 1, 1, 1, 1, 1, 1, 1, 7, 7],

        ]),
        "output": np.array([
            [0, 0, 0, 3],
            [0, 0, 0, 3],
            [0, 0, 0, 3],
            [0, 0, 0, 3],
        ]),
         "result": "success"
    },
    {
        "input": np.array([
            [7, 7, 0, 0, 7, 7, 0, 0],
            [7, 7, 0, 0, 7, 7, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [7, 7, 0, 0, 7, 7, 0, 0],
            [7, 7, 0, 0, 7, 7, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
        ]),
        "output": np.array([
            [3, 3, 0, 0],
            [3, 3, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ]),
        "result": "success"
    },
        {
        "input": np.array([
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 7, 7],
            [0, 0, 0, 0, 0, 0, 7, 7],
            [0, 0, 0, 0, 0, 0, 7, 7],
            [0, 0, 0, 0, 0, 0, 7, 7],
        ]),
        "output": np.array([
   
            [0, 0, 3, 3],
            [0, 0, 3, 3],
            [0, 0, 3, 3],
            [0, 0, 3, 3],
        ]),
        "result": "success"
    },
]

def analyze_examples(examples):
    results = []
    for i, example in enumerate(examples):
        input_grid = example["input"]
        output_grid = example["output"]
        orange_regions = []
        white_bordering_orange = []

        # Find all 2x2 orange (7) regions
        for row in range(input_grid.shape[0] - 1):
            for col in range(input_grid.shape[1] - 1):
                if np.all(input_grid[row:row+2, col:col+2] == 7):
                    orange_regions.append((row, col))

                    # Check for adjacent white (1) pixels
                    # Check above
                    if row > 0 and input_grid[row-1, col] == 1:
                        white_bordering_orange.append((row - 1, col))
                    if row > 0 and input_grid[row-1, col+1] == 1:
                        white_bordering_orange.append((row - 1, col+1))
                    # Check below
                    if row < input_grid.shape[0] - 2 and input_grid[row+2, col] == 1:
                        white_bordering_orange.append((row+2, col))
                    if row < input_grid.shape[0] - 2 and input_grid[row+2, col+1] == 1:
                        white_bordering_orange.append((row+2, col+1))
                    #check left
                    if col > 0 and input_grid[row, col-1] == 1:
                        white_bordering_orange.append((row, col-1))
                    if col > 0 and input_grid[row+1, col-1] == 1:
                         white_bordering_orange.append((row+1, col-1))
                    # Check right
                    if col < input_grid.shape[1]-2 and input_grid[row, col+2] == 1:
                        white_bordering_orange.append((row, col+2))
                    if col < input_grid.shape[1]-2 and input_grid[row+1, col+2] == 1:
                        white_bordering_orange.append((row+1, col+2))

        results.append({
            "example_index": i,
            "input_shape": input_grid.shape,
            "output_shape": output_grid.shape,
            "orange_regions_count": len(orange_regions),
            "orange_regions_coords": orange_regions,
            "white_bordering_orange_count": len(white_bordering_orange),
            "white_bordering_orange_coords": white_bordering_orange
        })
    return results

analysis_results = analyze_examples(train_examples)
for result in analysis_results:
    print(result)