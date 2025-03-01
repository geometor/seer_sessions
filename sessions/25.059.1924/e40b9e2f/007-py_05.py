import numpy as np

def analyze_example(input_grid, output_grid):
    """Analyzes a single input/output pair and returns a report."""

    def get_shape_bounds(grid):
        rows, cols = np.where(grid != 0)
        if len(rows) == 0:
            return None
        min_row, max_row = np.min(rows), np.max(rows)
        min_col, max_col = np.min(cols), np.max(cols)
        return min_row, max_row, min_col, max_col
    
    def shape_description(shape):
        rows, cols = shape.shape
        if rows == cols:
            return "square"
        elif cols > rows:
            return "horizontal rectangle"
        else:
            return "vertical rectangle"
    
    input_bounds = get_shape_bounds(input_grid)
    output_bounds = get_shape_bounds(output_grid)
    
    if input_bounds is None or output_bounds is None:
        return "Empty input or output grid."
    
    input_shape = input_grid[input_bounds[0]:input_bounds[1]+1, input_bounds[2]:input_bounds[3]+1]
    output_shape = output_grid[output_bounds[0]:output_bounds[1]+1, output_bounds[2]:output_bounds[3]+1]
    
    report = {
        "input_shape_description": shape_description(input_shape),
        "input_dimensions": input_shape.shape,
        "input_colors": np.unique(input_shape).tolist(),
        "output_shape_description": shape_description(output_shape),
        "output_dimensions": output_shape.shape,
        "output_colors": np.unique(output_shape).tolist(),
        "input_bounds": input_bounds,
        "output_bounds": output_bounds,
    }
    return report

# Example usage with the provided training data (assuming it's stored in 'train_data')
# Make sure the data is correctly structured
train_data = [
    ({'input': np.array([[0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0],
                       [0, 0, 4, 4, 0, 0],
                       [0, 0, 4, 4, 0, 0],
                       [0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0]]),
      'output': np.array([[0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0],
                        [0, 0, 7, 7, 0, 0],
                        [0, 0, 7, 7, 0, 0],
                        [0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0]])},
     {'input': np.array([[0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 4, 0, 0, 0],
       [0, 0, 0, 4, 0, 0, 0],
       [0, 0, 0, 4, 0, 0, 0],
       [0, 0, 0, 4, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0]]), 'output': np.array([[0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 7, 0, 0, 0],
       [0, 0, 0, 7, 0, 0, 0],
       [0, 0, 0, 7, 0, 0, 0],
       [0, 0, 0, 7, 0, 0, 0]])}),
    ({'input': np.array([[0, 0, 0, 0, 0, 0],
                       [0, 4, 4, 4, 4, 0],
                       [0, 0, 0, 0, 0, 0]]),
      'output': np.array([[0, 0, 0, 0, 0, 0],
                        [0, 7, 7, 7, 7, 0],
                        [0, 0, 0, 0, 0, 0]])},
     {'input': np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 7, 7, 7, 7, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0]]), 'output': np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 4, 4, 4, 4, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0]])}),
    ({'input': np.array([[0, 0, 0, 0, 0, 0],
                       [0, 0, 7, 0, 0, 0],
                       [0, 0, 7, 0, 0, 0],
                       [0, 0, 7, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0]]),
      'output': np.array([[0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 4, 0],
                        [0, 0, 0, 0, 4, 0],
                        [0, 0, 0, 0, 4, 0],
                        [0, 0, 0, 0, 0, 0]])},
     {'input': np.array([[0, 0, 0, 0, 0],
       [0, 4, 0, 0, 0],
       [0, 4, 0, 0, 0],
       [0, 4, 0, 0, 0],
       [0, 4, 0, 0, 0]]), 'output': np.array([[0, 0, 0, 0, 0],
       [0, 0, 0, 0, 7],
       [0, 0, 0, 0, 7],
       [0, 0, 0, 0, 7],
       [0, 0, 0, 0, 7]])}),
    ({'input': np.array([[0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 7, 7, 0],
                       [0, 0, 0, 0, 7, 7, 0],
                       [0, 0, 0, 0, 0, 0, 0]]),
      'output': np.array([[0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 4, 4, 0, 0, 0],
                        [0, 0, 4, 4, 0, 0, 0],
                        [0, 0, 0, 0, 0, 0, 0]])},
     {'input': np.array([[0, 0, 0, 0, 0, 0, 0],
       [0, 0, 4, 4, 0, 0, 0],
       [0, 0, 4, 4, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0]]), 'output': np.array([[0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 7, 7, 0],
       [0, 0, 0, 0, 7, 7, 0],
       [0, 0, 0, 0, 0, 0, 0]])})]

for i, example in enumerate(train_data):
    report = analyze_example(example['input'], example['output'])
    print(f"--- Example {i+1} ---")
    for key, value in report.items():
        print(f"{key}: {value}")
    print()