import numpy as np

# Example Data (replace with actual data from ARC task)
# These are simplified representations for demonstration.
# I will need the full data from the ARC task to do this properly.

# Since I do not have the actual ARC task loaded into this environment,
# I will have to demonstrate the *type* of analysis I would do,
# using placeholder data.

# I am going to make up some very small grids that represent the key
# characteristics of the input, process, and output.

train_examples = [
    {
        'input': np.array([[1, 1, 1, 1, 1],
                           [1, 4, 1, 4, 1],
                           [1, 1, 1, 1, 1],
                           [1, 4, 1, 4, 1],
                           [1, 1, 1, 1, 1]]),
        'output': np.array([[0, 0, 0, 0, 0],
                            [0, 4, 0, 4, 0],
                            [0, 0, 0, 0, 0],
                            [0, 4, 0, 4, 0],
                            [0, 0, 0, 0, 0]])
    },
      {
        'input': np.array([[1, 1, 1, 1, 1,1],
                           [1, 1, 1, 1, 1,1],
                           [1, 4, 1, 4, 1,1],
                           [1, 1, 1, 1, 1,1],
                           [1, 4, 1, 4, 1,1],
                           [1, 1, 1, 1, 1,1]]),
        'output': np.array([[0, 0, 0, 0, 0],
                            [0, 4, 0, 4, 0],
                            [0, 0, 0, 0, 0],
                            [0, 4, 0, 4, 0],
                            [0, 0, 0, 0, 0]])
    },
    {
        'input': np.array([[8, 8, 8, 8, 8, 8, 8],
                           [8, 4, 8, 8, 8, 4, 8],
                           [8, 8, 8, 8, 8, 8, 8],
                           [8, 8, 8, 8, 8, 8, 8],
                           [8, 8, 8, 8, 8, 8, 8],
                           [8, 4, 8, 8, 8, 4, 8],
                           [8, 8, 8, 8, 8, 8, 8]]),
        'output': np.array([[0, 0, 0, 0, 0, 0, 0],
                            [0, 4, 0, 0, 0, 4, 0],
                            [0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0],
                            [0, 4, 0, 0, 0, 4, 0],
                            [0, 0, 0, 0, 0, 0, 0]])
    }
]


def analyze_example(example):
    input_grid = example['input']
    output_grid = example['output']
    yellow_pixels = find_pixels_by_color(input_grid, 4)
    (min_row, min_col), (max_row, max_col) = bounding_box(yellow_pixels)
    predicted_output = transform(input_grid)

    print("Input Grid Shape:", input_grid.shape)
    print("Output Grid Shape:", output_grid.shape)
    print("Yellow Pixels:", yellow_pixels)
    print("Bounding Box (Initial):", (min_row, min_col), (max_row, max_col))
    print("Predicted Output Shape", predicted_output.shape)
    print("Output and predicted output are equal", np.array_equal(output_grid,predicted_output))
    print("---")


for i, example in enumerate(train_examples):
    print(f"Example {i+1}:")
    analyze_example(example)
