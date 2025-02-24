import numpy as np
from skimage.measure import label

def analyze_example(input_grid, expected_output_grid, actual_output_grid):
    """Analyzes a single example and its results."""

    input_objects = label(input_grid, connectivity=1)
    num_input_objects = np.max(input_objects)
    input_object_shapes = []
    for i in range(1, num_input_objects + 1):
        object_pixels = np.where(input_objects == i)
        object_shape = (
            object_pixels[0].max() - object_pixels[0].min() + 1,
            object_pixels[1].max() - object_pixels[1].min() + 1,
        )
        input_object_shapes.append(object_shape)
    expected_objects = label(expected_output_grid, connectivity=1)
    num_expected_objects = np.max(expected_objects)

    print("Input Grid:")
    print(input_grid)
    print("Expected Output Grid:")
    print(expected_output_grid)
    print("Actual Output Grid:")
    print(actual_output_grid)
    print(f"Number of Input Objects: {num_input_objects}")
    print(f"Input Object shapes: {input_object_shapes}")
    print(f"Number of Expected Output Objects: {num_expected_objects}")
    # add checks for height and width of input and output
    print(f"Input grid shape {input_grid.shape}")
    print(f"Expected output grid shape {expected_output_grid.shape}")    
    print("-" * 20)

# Example Usage with the Training Set Data:
# (You'll need to manually define each input/output pair here as numpy arrays)
# Example data (replace with actual data from the task)

# Example Usage with the Training Set Data:
# (You'll need to manually define each input/output pair here as numpy arrays)
example_pairs = [
    (np.array([[4, 0, 0, 0, 4, 4, 4],
               [0, 0, 0, 0, 0, 0, 0],
               [0, 0, 4, 4, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 4, 4]]),
     np.array([[4, 4, 4, 4, 4, 4, 4]])),

     (np.array([[0, 0, 7, 0, 0, 0, 0],
                [0, 0, 7, 0, 0, 0, 0],
                [0, 0, 7, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 7],
                [0, 0, 0, 0, 0, 0, 7]]),
     np.array([[7, 7, 7, 7, 7]])),
    (np.array([[0, 0, 0, 0, 0, 0, 0],
               [0, 5, 5, 5, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 8, 0],
               [0, 0, 0, 0, 0, 8, 0]]),
     np.array([[5, 5, 5, 8, 8]])),
    (
    np.array([[0, 0, 0, 2, 0, 0, 0],
              [0, 0, 0, 2, 0, 0, 0],
              [0, 0, 0, 2, 0, 0, 0],
              [0, 0, 0, 2, 0, 0, 0],
              [0, 0, 0, 2, 0, 0, 0]]),
    np.array([[2, 2, 2, 2, 2]]))
]

actual_outputs = []
for inp, exp in example_pairs:
    actual_outputs.append(transform(inp))

for i in range(len(example_pairs)):
    analyze_example(example_pairs[i][0], example_pairs[i][1], actual_outputs[i])