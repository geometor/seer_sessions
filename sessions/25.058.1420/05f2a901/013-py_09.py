import numpy as np

def find_object(grid, color):
    """Finds the bounding box of an object of a given color."""
    rows, cols = np.where(grid == color)
    if len(rows) == 0:
        return None  # Object not found
    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)
    return (min_row, min_col), (max_row, max_col)

def get_object(grid, color):
    """extracts the contiguous block identified as an object"""
    coords = np.where(grid == color)
    # if the object does not exist, signal with an empty array with correct
    # shape
    if len(coords[0]) == 0:
       return np.array([])
    rows, cols = coords
    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)

    obj = grid[min_row:max_row+1, min_col:max_col+1]
    # return sliced original object from input_grid
    return obj

def object_details(grid, color):
    """Provides details of the object location and size"""
    obj = get_object(grid, color)
    if obj.size == 0:
        return "Not found"
    (min_row, min_col), (max_row, max_col) = find_object(grid, color)
    height = max_row - min_row + 1
    width = max_col - min_col + 1
    return {
        "top_left": (min_row, min_col),
        "bottom_right": (max_row, max_col),
        "height": height,
        "width": width,
        "shape": obj.shape,
        "area": obj.size
    }
def print_grid(grid):
    # helper function to pretty print a grid
    for row in grid:
        print(" ".join(str(cell) for cell in row))

# examples from the previous training round

examples = [
    (np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 2, 2, 0, 0, 0, 0],
              [0, 0, 0, 2, 2, 0, 0, 8, 0]]),
     np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 2, 2, 0],
              [0, 0, 0, 0, 0, 0, 2, 2, 8]])),
    (np.array([[0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 2, 2, 0, 0, 0],
               [0, 0, 0, 2, 2, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 8, 0],
               [0, 0, 0, 0, 0, 0, 0, 0]]),
     np.array([[0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 2, 2, 0, 0, 0],
               [0, 0, 0, 2, 2, 0, 8, 0],
               [0, 0, 0, 0, 0, 0, 0, 0]])),
    (np.array([[0, 0, 0, 0, 0, 0, 0],
               [0, 8, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 2, 2],
               [0, 0, 0, 0, 0, 2, 2]]),
     np.array([[0, 8, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 2, 2],
               [0, 0, 0, 0, 0, 2, 2]])),
        (np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 2, 2, 0, 0, 8, 0],
               [0, 0, 0, 2, 2, 0, 0, 0, 0]]),
    np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 2, 2, 0, 0, 8, 0],
               [0, 0, 0, 2, 2, 0, 0, 0, 0]]))
]

from previous_solution import transform  # import previous transform

def analyze_examples(examples, transform_function):
    results = []
    for i, (input_grid, expected_output) in enumerate(examples):
        actual_output = transform_function(input_grid.copy())
        red_input_details = object_details(input_grid, 2)
        blue_input_details = object_details(input_grid, 8)
        red_output_details = object_details(actual_output, 2)
        blue_output_details = object_details(actual_output, 8)
        expected_red_output_details = object_details(expected_output, 2)
        is_correct = np.array_equal(actual_output, expected_output)
        results.append({
            "example": i + 1,
            "input_red": red_input_details,
            "input_blue": blue_input_details,
            "output_red": red_output_details,
            "output_blue": blue_output_details,
            "expected_red_output": expected_red_output_details,
            "correct": is_correct,
        })
    return results

results = analyze_examples(examples, transform)
for result in results:
    print(result)