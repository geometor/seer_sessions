import numpy as np

# Provided code (find_rectangle, extract_interior - copied for completeness)
def find_rectangle(grid, color=2):
    """Finds the bounding box of a rectangle of the specified color."""
    rows, cols = np.where(grid == color)
    if len(rows) == 0:
        return None  # No rectangle found

    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)

    # Check if it's a solid rectangle
    for r in range(min_row, max_row + 1):
        for c in range(min_col, max_col + 1):
            if grid[r, c] != color:
               return None

    return (min_row, min_col), (max_row, max_col)

def extract_interior(grid, top_left, bottom_right):
    """Extracts the interior of a rectangle defined by top_left and bottom_right."""
    return grid[top_left[0]+1:bottom_right[0], top_left[1]+1:bottom_right[1]]

task = {
    "train": [
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 2, 2, 2, 2, 2, 2, 0], [0, 0, 0, 2, 0, 0, 8, 0, 2, 0], [0, 0, 0, 2, 1, 0, 0, 0, 2, 0], [0, 0, 0, 2, 3, 3, 0, 3, 2, 0], [0, 0, 0, 2, 3, 3, 5, 1, 2, 0], [0, 0, 0, 2, 5, 1, 3, 0, 2, 0], [0, 0, 0, 2, 5, 0, 8, 0, 2, 0], [0, 0, 0, 2, 2, 2, 2, 2, 2, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[0, 0, 8, 0, 3, 3, 3, 3], [1, 0, 0, 0, 3, 0, 3, 1], [3, 3, 0, 3, 3, 0, 8, 1], [3, 3, 5, 1, 0, 3, 0, 0], [5, 1, 3, 0, 1, 3, 1, 1], [5, 0, 8, 0, 3, 0, 8, 8]]
        },
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0], [0, 0, 0, 0, 0, 2, 4, 1, 4, 4, 4, 2, 0, 0, 0, 0], [0, 0, 0, 0, 0, 2, 1, 4, 1, 1, 1, 2, 0, 0, 0, 0], [0, 0, 0, 0, 0, 2, 4, 1, 4, 4, 4, 2, 0, 0, 0, 0], [0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[4, 1, 4, 4, 4], [1, 4, 1, 1, 1]]
        },
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 2, 2, 2, 2, 2, 0, 0], [0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0], [0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0], [0, 0, 0, 0, 2, 2, 2, 2, 2, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[0, 0, 0], [0, 0, 0]]
        },
        {
            "input" : [[2, 2, 2, 2, 2, 2, 2, 2, 2],
                       [2, 0, 0, 0, 6, 6, 0, 0, 2],
                       [2, 0, 6, 6, 6, 0, 0, 0, 2],
                       [2, 6, 6, 6, 6, 6, 6, 0, 2],
                       [2, 2, 2, 2, 2, 2, 2, 2, 2]],
            "output": [[0, 0, 0, 6, 6, 0, 0],
                       [0, 6, 6, 6, 0, 0, 0],
                       [6, 6, 6, 6, 6, 6, 0]]
        }

    ],
    "test": [
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 0, 0, 0], [0, 0, 0, 0, 0, 0, 2, 6, 6, 6, 2, 0, 0, 0], [0, 0, 0, 0, 0, 0, 2, 6, 6, 6, 2, 0, 0, 0], [0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[6, 6, 6], [6, 6, 6]]
        }
    ]
}

def analyze_examples(task):
    results = []
    for i, example in enumerate(task["train"]):
        input_grid = np.array(example["input"])
        output_grid = np.array(example["output"])
        rectangle_bounds = find_rectangle(input_grid)
        if rectangle_bounds:
            top_left, bottom_right = rectangle_bounds
            interior = extract_interior(input_grid, top_left, bottom_right)
            interior_shape = interior.shape
            output_shape = output_grid.shape
            results.append({
                "example": i + 1,
                "rectangle_found": True,
                "interior_shape": interior_shape,
                "output_shape": output_shape,
                "interior": interior.tolist(),
                "output": output_grid.tolist()
            })
        else:
            results.append({
                "example": i + 1,
                "rectangle_found": False,
                "interior_shape": None,
                "output_shape": output_grid.shape
                ,"interior": None,
                "output": output_grid.tolist()
            })
    return results

analysis = analyze_examples(task)
for result in analysis:
    print(result)