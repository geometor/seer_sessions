def report(grid, label):
    print(f"  {label}:")
    print(f"    shape: {grid.shape}")
    # find unique values in grid and count them
    unique, counts = np.unique(grid, return_counts=True)
    print(f"    values: { {color: count for color, count in zip(unique, counts)} }")    

def find_vertical_lines(grid, color):
    lines = []
    for col in range(grid.shape[1]):
        if all(grid[:, col] == color):
            lines.append(col)
    return lines

def find_red_region(grid):
    red_region = []
    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == 2:
                red_region.append((row, col))
    
    if not red_region:
        return None, None, None

    red_row = red_region[0][0]
    min_col = min(c for r, c in red_region)
    max_col = max(c for r, c in red_region)

    return red_row, min_col, max_col

def summarize_example(input_grid, output_grid, transformed_grid):
    print("Input:")
    report(input_grid, "Input")

    print("\nExpected Output:")
    report(output_grid, "Output")

    print("\nTransformed Output:")
    report(transformed_grid, "Transformed")
    
    azure_lines = find_vertical_lines(input_grid, 8)
    print(f"\nAzure Lines: {azure_lines}")
    red_region = find_red_region(input_grid)
    print(f"Red Region: row={red_region[0]}, start_col={red_region[1]}, end_col={red_region[2]}" if red_region else "Red Region: None")

    print("\nDifferences (Transformed vs Expected):")
    if not np.array_equal(output_grid, transformed_grid):
        diff = (output_grid != transformed_grid)
        print(np.where(diff))
    else:
        print("No differences")

# Load the data and transform
import json
with open('data/training/6855a6e8.json', 'r') as f:
    task = json.load(f)

for i, example in enumerate(task["train"]):
    print(f"\nExample {i+1}:")
    input_grid = np.array(example['input'])
    output_grid = np.array(example['output'])
    transformed_grid = transform(input_grid)
    summarize_example(input_grid, output_grid, transformed_grid)
    input("Press Enter to continue...")
