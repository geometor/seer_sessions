import numpy as np

def count_pixel_colors(grid):
    unique, counts = np.unique(grid, return_counts=True)
    return dict(zip(unique, counts))

def find_all_2x2_red_blocks(grid):
    rows, cols = grid.shape
    blocks = []
    for i in range(rows - 1):
        for j in range(cols - 1):
            if (grid[i, j] == 2 and grid[i + 1, j] == 2 and
                grid[i, j + 1] == 2 and grid[i + 1, j + 1] == 2):
                blocks.append((i, j))
    return blocks
# These are not real results - for illustration only
examples = [
    {
        'input': np.array([[0, 0, 0], [0, 2, 2], [0, 2, 2]]),
        'output': np.array([[0, 0, 0], [0, 1, 0], [0, 0, 0]]),
        'predicted': np.array([[0, 0, 0], [0, 1, 0], [0, 0, 0]]),
    },
        {
        'input': np.array([[2, 2, 0], [2, 2, 2], [0, 2, 2]]),
        'output': np.array([[1, 0, 0], [0, 0, 2], [0, 1, 0]]),
        'predicted': np.array([[1, 0, 0], [0, 0, 0], [0, 0, 0]]),
    },
        {
        'input': np.array([[2, 2, 2, 2], [2, 2, 2, 2], [0,0,0,0], [2, 2, 2, 2], [2, 2, 2, 2]]),
        'output': np.array([[1, 0, 1, 0], [0, 0, 0, 0],[0,0,0,0], [1, 0, 1, 0], [0, 0, 0, 0]]),
        'predicted': np.array([[1, 0, 0, 0], [0, 0, 0, 0],[0,0,0,0], [0, 0, 0, 0], [0, 0, 0, 0]]),
    },
]

for i, example in enumerate(examples):
    input_colors = count_pixel_colors(example['input'])
    output_colors = count_pixel_colors(example['output'])
    predicted_colors = count_pixel_colors(example['predicted'])
    red_blocks_input = find_all_2x2_red_blocks(example['input'])
    red_blocks_output = find_all_2x2_red_blocks(example['output'])
    red_blocks_predicted = find_all_2x2_red_blocks(example['predicted'])

    print(f"Example {i+1}:")
    print(f"  Input Colors: {input_colors}")
    print(f"  Output Colors: {output_colors}")
    print(f"  Predicted Colors: {predicted_colors}")
    print(f"  Red Blocks in Input: {red_blocks_input}")
    print(f"  Red Blocks in Output: {red_blocks_output}")
    print(f"  Red Blocks in Predicted: {red_blocks_predicted}")