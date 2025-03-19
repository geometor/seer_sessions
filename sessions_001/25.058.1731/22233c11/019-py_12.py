import numpy as np

def calculate_metrics(input_grid, output_grid, predicted_grid):
    metrics = {
        "input_shape": input_grid.shape,
        "output_shape": output_grid.shape,
        "num_green_objects": len(get_objects(input_grid, 3)),
        "green_pixels_correct": np.sum((input_grid == 3) & (predicted_grid == 3) & (output_grid == 3)),
        "azure_pixels_correct": np.sum((output_grid == 8) & (predicted_grid == 8)),
        "azure_pixels_incorrect": np.sum((output_grid != 8) & (predicted_grid == 8)) + np.sum((output_grid == 8) & (predicted_grid != 8)),
        "other_errors": np.sum((output_grid != predicted_grid) & (output_grid != 8) & (output_grid !=3) & (predicted_grid != 8) & (predicted_grid != 3))
    }
    return metrics
# dummy grid data for testing only
def get_objects(grid, color):
    """
    Identifies contiguous objects of a specified color in the grid.
    Returns a list of sets, where each set contains the coordinates of an object's pixels.
    """
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    objects = []

    def is_valid(row, col, color):
        return 0 <= row < rows and 0 <= col < cols and grid[row, col] == color

    def dfs(row, col, current_object):
        if not is_valid(row, col, color) or visited[row, col]:
            return
        visited[row, col] = True
        current_object.add((row, col))

        # Explore adjacent cells (up, down, left, right)
        dfs(row + 1, col, current_object)
        dfs(row - 1, col, current_object)
        dfs(row, col + 1, current_object)
        dfs(row, col - 1, current_object)

    for i in range(rows):
        for j in range(cols):
            if grid[i, j] == color and not visited[i, j]:
                current_object = set()
                dfs(i, j, current_object)
                objects.append(current_object)
    return objects

input_grid1 = np.array([[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 3, 0], [0, 0, 0, 0, 3, 0], [0, 0, 0, 0, 3, 0], [0, 0, 0, 0, 0, 0]])
output_grid1 = np.array([[0, 0, 0, 0, 8, 0], [0, 0, 0, 0, 3, 0], [0, 0, 0, 0, 3, 0], [0, 0, 0, 0, 3, 0], [0, 0, 0, 0, 8, 0]])
predicted_grid1 = np.array([[0, 0, 0, 0, 8, 0], [0, 0, 0, 0, 3, 0], [0, 0, 0, 0, 3, 0], [0, 0, 0, 0, 3, 0], [0, 0, 0, 0, 8, 0]])

input_grid2 = np.array([[0, 0, 0, 0, 0, 0, 0, 0], [0, 3, 3, 3, 0, 0, 0, 0], [0, 3, 0, 3, 0, 0, 0, 0], [0, 3, 3, 3, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]])
output_grid2 = np.array([[0, 8, 8, 8, 0, 0, 0, 0], [0, 3, 3, 3, 0, 0, 0, 0], [0, 3, 0, 3, 0, 0, 0, 0], [0, 3, 3, 3, 0, 0, 0, 0], [0, 8, 8, 8, 0, 0, 0, 0]])
predicted_grid2 = np.array([[0, 8, 8, 8, 0, 0, 0, 0], [0, 3, 3, 3, 0, 0, 0, 0], [0, 3, 0, 3, 0, 0, 0, 0], [0, 3, 3, 3, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]])

input_grid3 = np.array([[0, 0, 0, 0, 0, 0], [0, 3, 3, 3, 3, 0], [0, 0, 0, 0, 0, 0]])
output_grid3 = np.array([[0, 8, 8, 8, 8, 0], [0, 3, 3, 3, 3, 0], [0, 8, 8, 8, 8, 0]])
predicted_grid3 = np.array([[0, 8, 8, 8, 8, 0], [0, 3, 3, 3, 3, 0], [0, 0, 0, 0, 0, 0]])
# end dummy grid data

metrics1 = calculate_metrics(input_grid1, output_grid1, predicted_grid1)
metrics2 = calculate_metrics(input_grid2, output_grid2, predicted_grid2)
metrics3 = calculate_metrics(input_grid3, output_grid3, predicted_grid3)
print(metrics1)
print(metrics2)
print(metrics3)