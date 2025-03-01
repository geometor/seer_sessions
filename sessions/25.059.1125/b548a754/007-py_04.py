import numpy as np

def analyze_example(input_grid, output_grid, predicted_grid):
    # Find the rectangular shape with red and blue pixels
    def find_shape(grid):
        rows, cols = grid.shape
        min_row, min_col = rows, cols
        max_row, max_col = -1, -1

        for r in range(rows):
            for c in range(cols):
                if grid[r, c] in [1, 2]:
                    min_row = min(min_row, r)
                    min_col = min(min_col, c)
                    max_row = max(max_row, r)
                    max_col = max(max_col, c)
        if max_row == -1:
            return None
        return (min_row, min_col, max_row, max_col)
    
    shape_bbox = find_shape(input_grid)
    if shape_bbox is None:
        return {
            "shape_found": False,
            "azure_pixels_removed": 0,
            "expansion_correct": False,
            'rectangle_height': 0,
            'rectangle_width': 0,

        }
    min_row, min_col, max_row, max_col = shape_bbox
    
    azure_count = np.sum(input_grid == 8)
    
    
    expansion_correct = np.array_equal(output_grid, predicted_grid)

    return {
        "shape_found": True,
        "azure_pixels_removed": azure_count,
        "expansion_correct": expansion_correct,
        'rectangle_height': max_row - min_row + 1,
        'rectangle_width' : max_col - min_col + 1,
    }


# Example data (replace with actual data from the task)
examples = [
  # example 0
  (np.array([[5, 5, 5, 5, 5, 5, 5],
            [5, 5, 8, 8, 8, 5, 5],
            [5, 5, 8, 1, 8, 5, 5],
            [5, 5, 2, 1, 2, 5, 5],
            [5, 5, 5, 5, 5, 5, 5]]),
  np.array([[5, 5, 5, 5, 5, 5, 5],
            [5, 5, 0, 0, 0, 5, 5],
            [5, 5, 0, 1, 0, 5, 5],
            [5, 5, 2, 1, 2, 5, 5],
            [5, 5, 2, 1, 2, 5, 5]]),
  np.array([[5, 5, 5, 5, 5, 5, 5],
            [5, 5, 0, 0, 0, 5, 5],
            [5, 5, 0, 1, 0, 5, 5],
            [5, 5, 2, 1, 2, 5, 5],
            [5, 5, 2, 1, 1, 5, 5]])), # output is incorrect in example

  # example 1
    (np.array([[8, 0, 0, 0, 8, 0, 0],
             [0, 8, 0, 8, 0, 0, 0],
             [0, 0, 1, 2, 1, 8, 0],
             [0, 0, 8, 0, 0, 0, 0]]),
     np.array([[0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0],
              [0, 0, 1, 2, 1, 0, 0],
              [0, 0, 1, 2, 1, 0, 0]]),
     np.array([[0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0],
              [0, 0, 1, 2, 1, 0, 0],
              [0, 0, 2, 1, 2, 0, 0]])), # output is incorrect in example
    
    # example 2
    (np.array([[0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 8, 8, 8, 8, 0, 0],
             [0, 8, 2, 1, 2, 1, 8, 0],
             [8, 2, 1, 2, 1, 2, 1, 8],
             [0, 0, 0, 0, 0, 0, 0, 0]]),
     np.array([[0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 2, 1, 2, 1, 0, 0],
              [0, 2, 1, 2, 1, 2, 1, 0],
              [0, 2, 1, 2, 1, 2, 1, 0]]),
     np.array([[0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 2, 1, 2, 1, 0, 0],
             [8, 2, 1, 2, 1, 2, 1, 8],
             [0, 2, 1, 2, 1, 2, 1, 0]])) # output is incorrect in example
]

for i, (input_grid, output_grid, predicted_grid) in enumerate(examples):
    analysis = analyze_example(input_grid, output_grid, predicted_grid)
    print(f"Example {i}: {analysis}")
