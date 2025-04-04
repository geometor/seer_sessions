import numpy as np

def analyze_results(input_grid, expected_output, transformed_output):
    input_grid = np.array(input_grid)
    expected_output = np.array(expected_output)
    transformed_output = np.array(transformed_output)

    metrics = {
        "match": np.array_equal(expected_output, transformed_output),
        "pixels_off": np.sum(expected_output != transformed_output),
        "size_correct": expected_output.shape == transformed_output.shape,
        "color_palette_correct": True,  # Assuming color palette will always be from the original
        "correct_pixel_counts": {},
    }
    
    #check output shape, stop if not a match
    if not metrics["size_correct"] : return metrics

    for color in np.unique(np.concatenate((expected_output.flatten(), transformed_output.flatten()))):
        expected_count = np.sum(expected_output == color)
        transformed_count = np.sum(transformed_output == color)
        metrics["correct_pixel_counts"][int(color)] = expected_count == transformed_count

    return metrics

# Example Data (from the prompt) - formatted
examples = [
    {
        "input": [
            [1, 0, 0, 5, 0, 1, 0],
            [0, 1, 0, 5, 1, 1, 1],
            [1, 0, 0, 5, 0, 0, 0]
        ],
        "expected_output": [
            [0, 0, 0],
            [0, 2, 0],
            [0, 0, 0]
        ],
        "transformed_output": [
            [0, 2, 0],
            [0, 2, 0],
            [0, 2, 0]
        ]
    },
    {
        "input": [
            [1, 1, 0, 5, 0, 1, 0],
            [0, 0, 1, 5, 1, 1, 1],
            [1, 1, 0, 5, 0, 1, 0]
        ],
        "expected_output": [
            [0, 2, 0],
            [0, 0, 2],
            [0, 2, 0]
        ],
        "transformed_output": [
            [0, 2, 0],
            [0, 2, 0],
            [0, 2, 0]
        ]
    },
    {
        "input": [
            [0, 0, 1, 5, 0, 0, 0],
            [1, 1, 0, 5, 1, 0, 1],
            [0, 1, 1, 5, 1, 0, 1]
        ],
        "expected_output": [
            [0, 0, 0],
            [2, 0, 0],
            [0, 0, 2]
        ],
        "transformed_output": [
            [0, 2, 0],
            [0, 2, 0],
            [0, 2, 0]
        ]
    }
]

for i, example in enumerate(examples):
    metrics = analyze_results(example["input"], example["expected_output"], example["transformed_output"])
    print(f"Example {i + 1}:")
    for key, value in metrics.items():
        print(f"  {key}: {value}")
