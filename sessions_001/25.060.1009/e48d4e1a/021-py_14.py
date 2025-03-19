import numpy as np

def analyze_example(input_grid, output_grid, predicted_grid):
    """Analyzes a single example and returns relevant metrics."""

    def get_object_coords(grid, color):
        return np.argwhere(grid == color).tolist()

    def calculate_center(coords):
        if not coords:
            return None
        coords = np.array(coords)
        return tuple(coords.mean(axis=0))

    magenta_coords_in = get_object_coords(input_grid, 6)
    gray_coords_in = get_object_coords(input_grid, 5)
    magenta_coords_out = get_object_coords(output_grid, 6)
    magenta_coords_pred = get_object_coords(predicted_grid, 6)

    analysis = {
        'magenta_coords_in': magenta_coords_in,
        'gray_coords_in': gray_coords_in,
        'magenta_coords_out': magenta_coords_out,
        'magenta_coords_pred': magenta_coords_pred,
        'center_in': calculate_center(magenta_coords_in),
        'center_out': calculate_center(magenta_coords_out),
        'center_pred': calculate_center(magenta_coords_pred),
        'output_equals_predicted': np.array_equal(output_grid, predicted_grid)
    }
    return analysis


def show_grid(grid_data, title):
    """
    formats and prints a grid
    """

    # Determine grid dimensions
    rows = len(grid_data)
    cols = len(grid_data[0]) if rows > 0 else 0

    # Create a formatted string for the grid
    grid_str = ""
    for i in range(rows):
        if i == 0:
            # top border
            grid_str += "┌" + "─" * (cols * 2) + "┐\n"

        grid_str += "│"
        for j in range(cols):
            grid_str += str(grid_data[i][j])
            if j < cols - 1:
                grid_str += " "  # Add space between elements

        grid_str += "│\n"
        if i == rows - 1:
            # bottom border
            grid_str += "└" + "─" * (cols * 2) + "┘\n"

    print(f"{title}\n{grid_str}")


# Example Usage (assuming input_grids, output_grids, and predicted_grids are defined)

task_examples = [
    {
        'input': [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 5, 0, 0, 0],
            [0, 0, 0, 5, 0, 0, 0],
            [0, 0, 0, 6, 6, 6, 0],
            [0, 0, 0, 0, 0, 0, 0],
        ],
        'output': [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 6, 0, 0, 0],
            [0, 0, 0, 6, 0, 0, 0],
            [0, 0, 0, 6, 0, 0, 0],
        ]
    },
     {
        'input': [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 5, 5, 0, 0, 0],
            [0, 0, 0, 6, 6, 6, 6, 0],
            [0, 0, 0, 6, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
        ],
        'output': [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 6, 6, 0, 0, 0],
            [0, 0, 0, 0, 6, 0, 0, 0],
            [0, 0, 0, 0, 6, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
        ]
    },
     {
        'input': [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 5, 0, 0, 0, 0, 0],
            [0, 5, 0, 0, 0, 0, 0],
            [0, 6, 6, 6, 0, 0, 0],
            [0, 6, 0, 0, 0, 0, 0],
            [0, 6, 0, 0, 0, 0, 0],
        ],
        'output': [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 6, 6, 6, 0, 0, 0],
            [0, 0, 0, 6, 0, 0, 0],
            [0, 0, 0, 6, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
        ]
    },
]

results = []
for ex in task_examples:
  input_grid = np.array(ex['input'])
  output_grid = np.array(ex['output'])
  predicted_grid = transform(input_grid)
  results.append( analyze_example(input_grid, output_grid, predicted_grid) )
  show_grid(ex['input'], "input")
  show_grid(ex['output'], "output")
  show_grid(predicted_grid, "predicted")

print(results)