# Hypothetical code_execution environment and helper functions
class MockCodeExecution:
    def __init__(self):
        pass
    
    def run_transform(self, input_grid, transform_func):
        return transform_func(input_grid)

    def compare_grids(self, grid1, grid2):
        return np.array_equal(grid1, grid2)

    def find_color_changes(self, input_grid, output_grid):
        changes = []
        for r in range(input_grid.shape[0]):
            for c in range(input_grid.shape[1]):
                if input_grid[r,c] != output_grid[r,c]:
                    changes.append( ((r,c), input_grid[r,c], output_grid[r,c]))
        return changes

    def get_adjacent_pixels(self, grid, r, c):
        #same as get_neighbors
        rows, cols = grid.shape
        neighbors = []
        if row > 0:
            neighbors.append((row - 1, col))  # Up
        if row < rows - 1:
            neighbors.append((row + 1, col))  # Down
        if col > 0:
            neighbors.append((row, col - 1))  # Left
        if col < cols - 1:
            neighbors.append((row, col + 1))  # Right
        return neighbors

code_execution = MockCodeExecution()

# Let's simulate running this on the provided examples (I'll use placeholders):

examples = [
  {"input": np.array([[8, 8, 8, 8, 8, 8, 8, 8], [8, 1, 1, 1, 1, 1, 1, 8], [8, 1, 1, 1, 1, 1, 1, 8], [8, 1, 1, 1, 1, 1, 1, 8], [8, 8, 8, 8, 8, 8, 8, 8]]), "output": np.array([[8, 8, 8, 8, 8, 8, 8, 8], [8, 3, 3, 3, 3, 3, 3, 8], [8, 3, 3, 3, 3, 3, 3, 8], [8, 3, 3, 3, 3, 3, 3, 8], [8, 8, 8, 8, 8, 8, 8, 8]])},
    {"input": np.array([[8, 8, 8, 8, 8, 8, 8, 8], [8, 2, 2, 2, 2, 2, 2, 8], [8, 2, 2, 2, 2, 2, 2, 8], [8, 2, 2, 2, 2, 2, 2, 8], [8, 8, 8, 8, 8, 8, 8, 8]]), "output": np.array([[8, 8, 8, 8, 8, 8, 8, 8], [8, 6, 6, 6, 6, 6, 6, 8], [8, 6, 6, 6, 6, 6, 6, 8], [8, 6, 6, 6, 6, 6, 6, 8], [8, 8, 8, 8, 8, 8, 8, 8]])},
    {"input": np.array([[8, 8, 8, 8, 8, 8], [8, 0, 0, 0, 0, 8], [8, 0, 0, 0, 0, 8],[8, 8, 8, 8, 8, 8]]), "output": np.array([[8, 8, 8, 8, 8, 8], [8, 5, 5, 5, 5, 8], [8, 5, 5, 5, 5, 8],[8, 8, 8, 8, 8, 8]])},
    {"input": np.array([[8, 8, 8, 8, 8], [8, 4, 4, 4, 8], [8, 4, 4, 4, 8], [8, 8, 8, 8, 8]]), "output": np.array([[8, 8, 8, 8, 8], [8, 1, 1, 1, 8], [8, 1, 1, 1, 8], [8, 8, 8, 8, 8]])}
]

results = []
for i, example in enumerate(examples):
    predicted_output = code_execution.run_transform(example["input"], transform)
    correct = code_execution.compare_grids(predicted_output, example["output"])
    changes = code_execution.find_color_changes(example["input"], example["output"])
    results.append({"example": i, "correct": correct, "changes": changes})

for result in results:
    print(result)