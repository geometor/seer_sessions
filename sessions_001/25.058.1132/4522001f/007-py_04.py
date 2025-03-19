import numpy as np

def find_pixels(grid, color):
    return np.argwhere(grid == color)

def get_green_square_dimensions(grid):
    green_pixels = find_pixels(grid, 3)
    if len(green_pixels) == 0:
        return 0, 0
    rows = green_pixels[:, 0]
    cols = green_pixels[:, 1]
    return max(rows) - min(rows) + 1, max(cols) - min(cols) + 1

# Example Data (replace with actual data from the task)
example_data = [
    {
        "input": np.array([[0, 0, 0], [0, 2, 0], [0, 0, 0]]),
        "output": np.array([[3, 0, 0], [0, 0, 0], [0, 0, 0]]),
    },
    {
        "input": np.array([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 2, 0],[0, 0, 0, 0]]),
        "output": np.array([[3, 3, 0, 0], [3, 3, 0, 0], [0, 0, 0, 0],[0,0,0,0]]),
    },
    {
        "input": np.array([[0, 0, 0, 0], [0, 0, 0, 0], [0, 2, 0, 0],[0, 0, 0, 0]]),
        "output": np.array([[3, 3, 0, 0], [3, 3, 0, 0], [0, 0, 0, 0],[0,0,0,0]]),
    },
        {
        "input": np.array([[2, 0, 0], [0, 0, 0], [0, 0, 0]]),
        "output": np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]]),
    },

]

results = []
for i, example in enumerate(example_data):
    input_grid = example["input"]
    output_grid = example["output"]

    red_pixel_location = find_pixels(input_grid, 2)
    if len(red_pixel_location) > 0:
        red_row, red_col = red_pixel_location[0]
    else:
        red_row, red_col = -1, -1  # Indicate no red pixel

    green_height, green_width = get_green_square_dimensions(output_grid)

    results.append(
        {
            "example": i + 1,
            "red_row": red_row,
            "red_col": red_col,
            "green_height": green_height,
            "green_width": green_width,
        }
    )

for result in results:
    print(result)