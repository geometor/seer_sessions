import numpy as np

def analyze_results(examples, transform_function):
    results = []
    for i, (input_grid, expected_output) in enumerate(examples):
        predicted_output = transform_function(input_grid)
        input_grid = np.array(input_grid)
        expected_output = np.array(expected_output)
        predicted_output = np.array(predicted_output)

        # Basic metrics
        input_shape = input_grid.shape
        expected_shape = expected_output.shape
        predicted_shape = predicted_output.shape
        correct = np.array_equal(expected_output, predicted_output)


        results.append({
            "example": i + 1,
            "input_shape": input_shape,
            "expected_shape": expected_shape,
            "predicted_shape": predicted_shape,
            "correct": correct,
        })

    return results
# Dummy data and transform for demonstration in this context:
examples = [
    ([[5, 5, 5], [5, 5, 5], [5, 5, 5]], [[5, 5, 5], [5, 5, 5], [5, 5, 5]]),  # Example 1
    ([[0, 0, 5, 0, 0], [0, 5, 5, 5, 0], [5, 5, 1, 5, 5], [0, 5, 5, 5, 0], [0, 0, 5, 0, 0]], [[5, 0, 0], [5, 5, 0], [1, 5, 5], [5, 5, 0], [5, 0, 0]]),  # Example 2
    ([[5, 5, 5, 5, 0, 0, 0, 0], [5, 1, 5, 5, 0, 0, 5, 5], [5, 5, 5, 5, 0, 0, 5, 1], [0, 0, 0, 0, 0, 0, 5, 5]], [[5, 5, 0, 0, 0, 0], [1, 5, 0, 0, 5, 5], [5, 5, 0, 0, 5, 1], [0, 0, 0, 0, 5, 5]]) # Example 3
]

#the provided transform function
def find_object(grid, color):
    # Find all pixels of the specified color
    coords = np.argwhere(grid == color)
    if coords.size == 0:
        return [], 0, 0, 0, 0

    # Use a simple bounding box approach to define the object
    min_row = np.min(coords[:, 0])
    max_row = np.max(coords[:, 0])
    min_col = np.min(coords[:, 1])
    max_col = np.max(coords[:, 1])

    object_coords = []

    for r in range(min_row, max_row + 1):
        for c in range(min_col, max_col+1):
            if grid[r,c] == color:
                object_coords.append((r,c))


    return object_coords, min_row, min_col, max_row-min_row+1, max_col-min_col+1

def transform(input_grid):
    # Convert input to numpy array
    input_grid = np.array(input_grid)

    # Find the grey (5) object and its top-left corner, height, and width
    object_coords, min_row, min_col, obj_height, obj_width = find_object(input_grid, 5)

    # Create output with height and width
    output_grid = np.zeros((obj_height, obj_width), dtype=int)

    # Fill the output grid
    for r in range(obj_height):
        for c in range(obj_width):
            if (min_row+r,min_col+c) in object_coords:
                output_grid[r,c] = 5

    return output_grid.tolist()

analysis = analyze_results(examples, transform)
for result in analysis:
    print(result)