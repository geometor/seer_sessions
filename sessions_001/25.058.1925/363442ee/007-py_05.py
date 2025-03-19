import numpy as np

def analyze_example(input_grid, output_grid):
    """Analyzes a single input-output pair."""

    print("Input Grid:")
    print(input_grid)
    print("Output Grid:")
    print(output_grid)


    def find_bar(grid):
        """Finds the column index of a vertical  bar or -1."""
        rows, cols = grid.shape
        #check for vertical
        for c in range(cols):
            first_val = grid[0,c]
            if all(grid[r, c] == first_val for r in range(rows)):
                return c, 'vertical'
        #check for horizontal
        for r in range(rows):
          first_val = grid[r, 0]
          if all(grid[r,c] == first_val for c in range(cols)):
            return r, 'horizontal'

        return -1, None  # Return -1 if no bar is found

    def find_shape(grid, bar_col, bar_type):
        """Finds the coordinates of a shape defined by non-blue pixels."""
        rows, cols = grid.shape
        shape_coords = []
        for r in range(rows):
            for c in range(cols):
                if grid[r, c] != 1:
                    shape_coords.append((r, c))
        return shape_coords

    bar_col, bar_type = find_bar(input_grid)
    print(f"Bar Position: {bar_col}, Bar Type: {bar_type}")

    shape1_coords = find_shape(input_grid, bar_col, bar_type)
    print(f"Shape1 Coordinates (Input): {shape1_coords}")

    shape2_coords = find_shape(output_grid, None, None)
    print(f"Shape2 Coordinates (Output): {shape2_coords}")
    

    print("-" * 20)


# Load the example data (replace with actual data loading)
examples = task_data['train']

for i, example in enumerate(examples):
    print(f"Analyzing Example {i + 1}")
    analyze_example(np.array(example['input']), np.array(example['output']))
