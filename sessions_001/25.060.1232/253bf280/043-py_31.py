import numpy as np

def get_azure_pixels(grid):
    azure_coords = np.where(grid == 8)
    return list(zip(azure_coords[0], azure_coords[1]))

def analyze_example(input_grid, output_grid):
    azure_pixels = get_azure_pixels(input_grid)
    if not azure_pixels:
        return {
            "azure_count": 0,
            "azure_min_row": None,
            "azure_max_row": None,
            "azure_min_col": None,
            "azure_max_col": None,
            "green_min_row": None,
            "green_max_row": None,
            "green_col": None,
        }

    min_row, min_col = np.min(azure_pixels, axis=0)
    max_row, max_col = np.max(azure_pixels, axis=0)

    green_coords = np.where(output_grid == 3)
    green_pixels = list(zip(green_coords[0], green_coords[1]))

    if not green_pixels:
        return {
            "azure_count": len(azure_pixels),
            "azure_min_row": min_row,
            "azure_max_row": max_row,
            "azure_min_col": min_col,
            "azure_max_col": max_col,
            "green_min_row": None,
            "green_max_row": None,
            "green_col": None,
        }

    green_min_row = np.min(green_coords[0])
    green_max_row = np.max(green_coords[0])
    green_col = green_pixels[0][1]  # Assuming all green pixels are in the same column


    return {
        "azure_count": len(azure_pixels),
        "azure_min_row": min_row,
        "azure_max_row": max_row,
        "azure_min_col": min_col,
        "azure_max_col": max_col,
        "green_min_row": green_min_row,
        "green_max_row": green_max_row,
        "green_col": green_col,
    }

task = {
    "train": [
        {
            "input": [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 8, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 8, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            ],
            "output": [
                [0, 0, 0, 0, 3, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 3, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            ],
        },
        {
            "input": [
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 8, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 8, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0]
            ],
            "output": [
                [0, 0, 0, 3, 0, 0, 0, 0],
                [0, 0, 0, 3, 0, 0, 0, 0],
                [0, 0, 0, 3, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0]
            ],
        },
		{
            "input": [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 8, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            ],
            "output": [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 3, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            ],
        },
        {
            "input": [
                [0, 0, 0, 0, 0, 0, 0],
                [0, 8, 0, 0, 0, 0, 0],
                [0, 8, 0, 0, 0, 0, 0],
                [0, 8, 0, 0, 0, 0, 0],
                [0, 8, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0]
            ],
            "output": [
                [0, 3, 0, 0, 0, 0, 0],
                [0, 3, 0, 0, 0, 0, 0],
                [0, 3, 0, 0, 0, 0, 0],
                [0, 3, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0]
            ],
        },
        {
            "input": [
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 8, 8, 0],
                [0, 0, 0, 0, 0, 0]
            ],
            "output": [
                [0, 0, 0, 3, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0]
            ],
        }
    ],
    "test": [
        {
            "input": [
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 8, 8, 0, 0, 0],
                [0, 0, 0, 0, 8, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0]
            ],
            "output": [
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 3, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0]
            ]
        }
    ]
}

results = []
for example in task["train"]:
  input_grid = np.array(example["input"])
  output_grid = np.array(example["output"])
  results.append(analyze_example(input_grid, output_grid))

for i, res in enumerate(results):
    print(f"Example {i+1}: {res}")