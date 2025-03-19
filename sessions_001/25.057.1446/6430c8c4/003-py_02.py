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

        # Find all 2x2 orange (7) regions
        for row in range(input_grid.shape[0] - 1):
            for col in range(input_grid.shape[1] - 1):
                if np.all(input_grid[row:row+2, col:col+2] == 7):
                      orange_regions.append((row,col))

        results.append({
            "example_index": i,
            "orange_regions_count": len(orange_regions),
            "orange_regions_coords": orange_regions,

        })
    return results

analysis_results = analyze_examples(train_examples)
print(analysis_results)