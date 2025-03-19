import numpy as np

def get_block_data(grid):
    """
    Identifies contiguous blocks of the same color in a grid.

    Returns:
        A dictionary where keys are colors and values are lists of (start_row, start_col, count) tuples
        representing contiguous blocks of that color.
    """
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    block_data = {}

    def dfs(row, col, color, count):
        if (
            row < 0
            or row >= rows
            or col < 0
            or col >= cols
            or visited[row, col]
            or grid[row, col] != color
        ):
            return count

        visited[row, col] = True
        count += 1

        count = dfs(row + 1, col, color, count)  # Down
        count = dfs(row - 1, col, color, count)  # Up
        count = dfs(row, col + 1, color, count)  # Right
        count = dfs(row, col - 1, color, count)  # Left
        return count

    for row in range(rows):
        for col in range(cols):
            if not visited[row, col]:
                color = grid[row, col]
                block_count = dfs(row, col, color, 0)
                if color not in block_data:
                    block_data[color] = []
                block_data[color].append(((row, col), block_count))

    return block_data

#display all available examples
for index in range(len(task.train)):

    input_grid = task.train[index]["input"]
    output_grid = task.train[index]["output"]

    # Get shape information
    input_shape = np.array(input_grid).shape
    output_shape = np.array(output_grid).shape

    # Get block data for input and output
    input_blocks = get_block_data(np.array(input_grid))
    output_blocks = get_block_data(np.array(output_grid))
    
    print(f"Example {index}:")
    print(f"  Input Shape: {input_shape}")
    print(f"  Output Shape: {output_shape}")
    print(f"  Input Blocks: {input_blocks}")
    print(f"  Output Blocks: {output_blocks}")    