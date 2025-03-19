import numpy as np

def calculate_metrics(input_grid, output_grid, predicted_output_grid):
    """Calculates differences between expected and predicted output."""
    diff = output_grid != predicted_output_grid
    num_errors = np.sum(diff)
    error_pixels = np.where(diff)
    return num_errors, list(zip(error_pixels[0], error_pixels[1]))

task = {
    "train": [
        {
            "input": [
                [8, 8, 8, 8, 8, 8, 8, 8, 8],
                [8, 5, 5, 5, 8, 8, 8, 8, 8],
                [8, 5, 5, 5, 8, 8, 8, 8, 8],
                [8, 5, 5, 5, 8, 8, 8, 8, 8],
                [8, 8, 8, 8, 8, 8, 8, 8, 8],
                [8, 8, 8, 8, 8, 8, 8, 8, 8],
                [8, 8, 8, 8, 8, 8, 8, 8, 8],
                [8, 8, 8, 8, 8, 8, 8, 8, 8],
                [8, 8, 8, 8, 8, 8, 8, 8, 8],
            ],
            "output": [
                [8, 8, 8, 8, 8, 8, 8, 8, 8],
                [8, 5, 5, 5, 8, 8, 8, 8, 8],
                [8, 5, 5, 5, 8, 8, 8, 8, 8],
                [8, 5, 5, 5, 8, 8, 8, 8, 8],
                [8, 8, 8, 8, 8, 8, 8, 8, 8],
                [8, 5, 5, 5, 8, 8, 8, 8, 8],
                [8, 5, 5, 5, 8, 8, 8, 8, 8],
                [8, 5, 5, 5, 8, 8, 8, 8, 8],
                [8, 8, 8, 8, 8, 8, 8, 8, 8],
            ],
        },
        {
            "input": [
                [8, 8, 8, 8, 8, 8, 8, 8],
                [8, 8, 8, 3, 3, 3, 8, 8],
                [8, 8, 8, 3, 3, 3, 8, 8],
                [8, 8, 8, 8, 8, 8, 8, 8],
            ],
            "output": [
                [8, 8, 8, 8, 8, 8, 8, 8],
                [8, 8, 8, 3, 3, 3, 8, 8],
                [8, 8, 8, 8, 8, 8, 8, 8],
                [8, 8, 8, 8, 8, 8, 8, 8],
            ],
        },
        {
            "input": [
                [8, 8, 8, 8, 8, 8, 8],
                [8, 1, 1, 8, 8, 2, 2],
                [8, 8, 8, 8, 8, 8, 8],
                [8, 8, 6, 8, 8, 8, 8],
                [8, 8, 8, 8, 8, 8, 8],
            ],
            "output": [
                [8, 8, 8, 8, 8, 8, 8],
                [8, 1, 1, 8, 8, 2, 2],
                [8, 8, 8, 8, 8, 8, 8],
                [8, 8, 8, 8, 8, 8, 8],
                [8, 8, 8, 8, 8, 8, 8],
            ],
        },
        {
            "input": [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 3, 3, 0, 0, 0],
                [0, 0, 0, 0, 0, 3, 3, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            ],
            "output": [
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 3, 3, 0, 0, 0],
                [0, 0, 0, 0, 0, 3, 3, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            ],
        },
    ]
}
results = []

for example in task["train"]:
    input_grid = np.array(example["input"])
    output_grid = np.array(example["output"])
    predicted_output_grid = transform(input_grid)  # Use the existing transform function
    num_errors, error_pixels = calculate_metrics(input_grid, output_grid, predicted_output_grid)
    results.append({
        "num_errors": num_errors,
        "error_pixels": error_pixels
    })

for i, result in enumerate(results):
    print(f"Example {i+1}:")
    print(f"  Number of Errors: {result['num_errors']}")
    # print(f"  Error Pixels: {result['error_pixels']}")  # only enable if needed