import numpy as np
from typing import List, Tuple

def calculate_metrics(input_grid: List[List[int]], expected_output: List[List[int]], transformed_output: List[List[int]]) -> dict:
    """Calculates metrics comparing expected and transformed outputs."""

    input_grid = np.array(input_grid)
    expected_output = np.array(expected_output)
    transformed_output = np.array(transformed_output)

    metrics = {
        "match": np.array_equal(expected_output, transformed_output),
        "pixels_off": None,
        "size_correct": None,
        "color_palette_correct": True,  # Assume true initially, update if needed
        "correct_pixel_counts": None,
        "input_colors": np.unique(input_grid).tolist(),
        "expected_colors": np.unique(expected_output).tolist(),
        "transformed_colors": [] if transformed_output.size == 0 else np.unique(transformed_output).tolist(),
        "input_shape": input_grid.shape,
        "expected_shape": expected_output.shape,
         "transformed_shape": transformed_output.shape if transformed_output.size >0 else (0,0)
    }

    if metrics["match"] == False:

        if transformed_output.size > 0:
            if expected_output.shape == transformed_output.shape:
                metrics["pixels_off"] = np.sum(expected_output != transformed_output)
            metrics["size_correct"] = (expected_output.shape == transformed_output.shape)

            expected_counts = {color: np.sum(expected_output == color) for color in metrics["expected_colors"]}
            transformed_counts = {color: np.sum(transformed_output == color) for color in metrics["transformed_colors"]}

            if expected_counts.keys() == transformed_counts.keys():
              metrics["correct_pixel_counts"] = (expected_counts == transformed_counts)

            for color in metrics["expected_colors"]:
                if color not in metrics["transformed_colors"]:
                    metrics["color_palette_correct"] = False
                    break
            for color in metrics["transformed_colors"]:
                if color not in metrics["expected_colors"]:
                    metrics["color_palette_correct"] = False
                    break
        else:
             metrics["size_correct"] = False
             metrics["correct_pixel_counts"] = False

    else:
        metrics["pixels_off"] = 0
        metrics["size_correct"] = True
        metrics["correct_pixel_counts"] = True

    return metrics

# Example Data (replace with your actual data)
examples = [
    {
        "input": [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 2, 0, 2, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ],
        "expected": [[0, 2, 2, 2], [0, 0, 2, 0], [2, 2, 2, 0], [2, 0, 2, 0]],
        "transformed": []
    },
     {
        "input": [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ],
        "expected": [[1, 0, 0], [1, 1, 0], [0, 1, 0], [1, 1, 1], [0, 0, 1]],
        "transformed": [[1, 0, 0], [1, 1, 0], [0, 1, 0], [1, 1, 1], [0, 0, 1]]
    },
    {
        "input": [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 8, 0, 8, 0, 0, 0, 0, 0],
            [0, 0, 0, 8, 8, 8, 8, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 8, 8, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ],
        "expected": [[0, 8, 0, 8, 0], [8, 8, 8, 8, 0], [0, 0, 0, 8, 8]],
        "transformed": []
    }

]

all_metrics = [calculate_metrics(**example) for example in examples]

for i, metrics in enumerate(all_metrics):
    print(f"Example {i+1}:")
    for key, value in metrics.items():
        print(f"  {key}: {value}")