import numpy as np

def find_vertical_segments(grid, color):
    """Finds all contiguous vertical line segments of a specified color."""
    segments = []
    rows, cols = grid.shape
    for j in range(cols):
        in_segment = False
        start_row = -1
        for i in range(rows):
            if grid[i, j] == color:
                if not in_segment:
                    in_segment = True
                    start_row = i
            elif in_segment:
                in_segment = False
                segments.append(((start_row, j), (i - 1, j)))  # (start, end)
                start_row = -1
        if in_segment:  # Handle segment at the end of the column
            segments.append(((start_row, j), (rows - 1, j)))
    return segments

def analyze_example(input_grid, output_grid):
    """Analyzes a single example pair."""
    gray_segments = find_vertical_segments(input_grid, 5)
    segment_lengths = [(seg, (seg[1][0] - seg[0][0] + 1)) for seg in gray_segments]
    sorted_segments = sorted(segment_lengths, key=lambda x: x[1], reverse=True)

    print("Segment Analysis:")
    for (start, end), length in sorted_segments:
        color = output_grid[start[0], start[1]]
        print(f"  Segment: Start={start}, End={end}, Length={length}, Output Color={color}")
    print("---")


task_id = '6150a2bd'
train_input_paths = [
    f'data/training/{task_id}/input/{i}.npy' for i in range(5)
]

train_output_paths = [
    f'data/training/{task_id}/output/{i}.npy' for i in range(5)
]
# Loop through each example pair
for i in range(len(train_input_paths)):
    input_grid = np.load(train_input_paths[i])
    output_grid = np.load(train_output_paths[i])
    print(f"Example {i+1}:")
    analyze_example(input_grid, output_grid)
