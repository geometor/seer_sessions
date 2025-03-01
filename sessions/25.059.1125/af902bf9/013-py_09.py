import numpy as np

def find_pixels_by_value(grid, value):
    """Finds the coordinates of pixels with a specific value."""
    return np.argwhere(grid == value).tolist()

def get_bounding_box(grid, value):
    """Calculates the bounding box for a color."""
    pixels = find_pixels_by_value(grid, value)
    if not pixels:
        return None, None
    min_row, min_col = np.min(pixels, axis=0)
    max_row, max_col = np.max(pixels, axis=0)
    return (min_row, min_col), (max_row, max_col)

def analyze_example(input_grid, output_grid):
    """Analyzes a single input-output pair."""
    analysis = {}

    # Yellow object analysis
    analysis['yellow_pixels_input'] = find_pixels_by_value(input_grid, 4)

    # Gray object analysis
    analysis['gray_pixels_input'] = find_pixels_by_value(input_grid, 5)
    analysis['gray_bounding_box_input'] = get_bounding_box(input_grid, 5)

    # Red rectangle analysis
    analysis['red_pixels_output'] = find_pixels_by_value(output_grid, 2)
    analysis['red_bounding_box_output'] = get_bounding_box(output_grid, 2)

    return analysis

# Example Usage (replace with actual input/output grids)
task_examples = [
    {
        'input': np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 5, 5, 5, 0, 0, 4, 4, 0],
                           [0, 5, 5, 5, 0, 0, 4, 4, 0],
                           [0, 5, 5, 5, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0]]),
        'output': np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 2, 2, 2, 0, 0, 4, 4, 0],
                            [0, 2, 2, 2, 0, 0, 4, 4, 0],
                            [0, 2, 2, 2, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0]]),
    },
    {
        'input': np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 5, 5, 5, 0],
                           [0, 0, 0, 0, 0, 0, 0, 5, 5, 5, 0],
                           [0, 0, 0, 0, 0, 0, 0, 5, 5, 5, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0]]),
        'output': np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0],
                            [0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0],
                            [0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0]]),
    },
        {
        'input': np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 5, 5, 5, 5, 5, 0],
                           [0, 0, 0, 0, 0, 0, 0, 5, 5, 5, 5, 5, 0],
                           [0, 0, 0, 0, 0, 0, 0, 5, 5, 5, 5, 5, 0],
                           [0, 0, 0, 0, 0, 0, 0, 5, 5, 5, 5, 5, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0]]),
        'output': np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 0],
                            [0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 0],
                            [0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 0],
                            [0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0]]),
    }

]
results = [analyze_example(ex['input'], ex['output']) for ex in task_examples]
print(results)