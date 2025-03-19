import numpy as np

def find_pixels_by_color(grid, color):
    return np.argwhere(grid == color)

def analyze_example(input_grid, output_grid):
    input_green_count = len(find_pixels_by_color(input_grid, 3))
    output_green_count = len(find_pixels_by_color(output_grid, 3))
    return {
        "input_green_count": input_green_count,
        "output_green_count": output_green_count,
    }

#dummy data
examples = [
    {
        "input": np.array([[0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 3, 0, 3],
                           [0, 0, 0, 0, 0, 0]]),
        "output": np.array([[0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 3, 3, 3],
                            [0, 0, 0, 0, 0, 0]]),
    },
            {
        "input": np.array([[0, 0, 0, 0, 0, 0],
                           [0, 3, 0, 0, 0, 3],
                           [0, 0, 0, 0, 0, 0]]),
        "output": np.array([[0, 0, 0, 0, 0, 0],
                            [0, 3, 3, 3, 3, 3],
                            [0, 0, 0, 0, 0, 0]]),
    },
    {
        "input": np.array([[0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 3, 0, 0, 3, 0],
                           [0, 0, 0, 0, 0, 0, 0]]),
        "output": np.array([[0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 3, 3, 3, 3, 0],
                            [0, 0, 0, 0, 0, 0, 0]]),
    },
    {
        "input": np.array([[0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 3, 0, 0, 3, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0]]),
        "output": np.array([[0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 3, 3, 3, 3, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0]]),
    }
]

for i, example in enumerate(examples):
    analysis = analyze_example(example["input"], example["output"])
    print(f"Example {i+1}:")
    print(f"  Input Green Pixels: {analysis['input_green_count']}")
    print(f"  Output Green Pixels: {analysis['output_green_count']}")