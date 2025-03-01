import numpy as np

def analyze_results(examples, transform_function):
    results = []
    for i, (input_grid, expected_output_grid) in enumerate(examples):
        actual_output_grid = transform_function(input_grid)
        is_correct = np.array_equal(np.array(actual_output_grid), np.array(expected_output_grid))
        results.append({
            "example_index": i,
            "input_grid": input_grid,
            "expected_output_grid": expected_output_grid,
            "actual_output_grid": actual_output_grid,
            "is_correct": is_correct,
        })
    return results

# dummy transform function to run tests
def transform(input_grid):
    # Convert input grid to a NumPy array
    input_array = np.array(input_grid)
    
    # Find the coordinates of the inner core pixel
    core_coords = find_inner_core(input_array)
    
    if core_coords is None:
      return input_grid #no transformation

    row, col = core_coords
        
    # Calculate bounding box (3x3)
    min_row, max_row = row - 1, row + 2
    min_col, max_col = col - 1, col + 2

    # Extract the 3x3 region
    output_grid = input_array[min_row:max_row, min_col:max_col].tolist()
    return output_grid

examples = [
([
    [1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 3, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1]
],
[
    [1, 1, 1],
    [1, 3, 1],
    [1, 1, 1]
]),
([
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 7, 7, 7, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 7, 7, 7, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 7, 7, 7, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
],
[
    [1, 1, 1],
    [1, 7, 7],
    [1, 7, 7]
]
),
([
    [0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 8, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1],
    [1, 5, 1, 0, 0, 0, 0, 0, 1, 2, 1],
    [1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1]
],
[
    [1, 1, 1], [1, 1, 1], [1, 1, 1]
]),
([
    [1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1],
    [1, 5, 1, 0, 0, 0, 0, 0, 1, 2, 1],
    [1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1]
],
[
    [1, 1, 1],
    [1, 5, 1],
    [1, 1, 1]
]),

([
    [1, 1, 1, 1, 1, 1],
    [1, 5, 5, 5, 5, 1],
    [1, 5, 5, 5, 5, 1],
    [1, 5, 5, 5, 5, 1],
    [1, 5, 5, 5, 5, 1],
    [1, 1, 1, 1, 1, 1]
],
[
    [1, 1, 1, 1, 1, 1],
    [1, 5, 5, 5, 5, 1],
    [1, 5, 5, 5, 5, 1],
    [1, 5, 5, 5, 5, 1],
    [1, 5, 5, 5, 5, 1],
    [1, 1, 1, 1, 1, 1]
])
]

results = analyze_results(examples, transform)
for result in results:
    print(result)
