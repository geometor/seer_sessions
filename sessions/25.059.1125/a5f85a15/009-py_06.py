import numpy as np

def analyze_example(input_grid, output_grid):
    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)

    # Get center pixel coordinates
    rows, cols = input_grid.shape
    center_row = rows // 2
    center_col = cols // 2

    # Get center pixel colors
    input_center_color = input_grid[center_row, center_col]
    output_center_color = output_grid[center_row, center_col]

    #check for diffs
    differences = np.where(input_grid != output_grid)
    diff_coords = list(zip(differences[0], differences[1]))
    other_changes = [(r,c,input_grid[r,c], output_grid[r,c]) for r, c in diff_coords if (r != center_row or c != center_col) ]

    return {
        'input_center_color': int(input_center_color),
        'output_center_color': int(output_center_color),
        'other_changes': other_changes,
        'center_coords': (center_row, center_col)
    }

def pretty_print_analysis(analysis_results):
    input_center = analysis_results['input_center_color']
    output_center = analysis_results['output_center_color']
    other_changes = analysis_results['other_changes']
    center_coords = analysis_results['center_coords']
    print(f"  Center Pixel (Input): {input_center} {center_coords}")
    print(f"  Center Pixel (Output): {output_center}")
    print(f"  Other changes {other_changes}")

# Example data (replace with actual data from the task)
examples = [
    ([[0, 0, 8, 2, 8, 2, 3, 0, 0], [0, 2, 3, 0, 0, 3, 8, 0, 2], [8, 5, 0, 8, 0, 0, 8, 5, 3], [3, 0, 5, 3, 0, 8, 5, 0, 3], [8, 0, 0, 5, 0, 8, 0, 8, 2], [0, 0, 8, 2, 3, 0, 0, 0, 3], [0, 8, 5, 0, 5, 8, 3, 2, 2], [8, 0, 0, 8, 2, 5, 0, 0, 8], [5, 0, 5, 2, 0, 0, 3, 8, 3]], [[0, 0, 8, 2, 8, 2, 3, 0, 0], [0, 2, 3, 0, 0, 3, 8, 0, 2], [8, 5, 0, 8, 0, 0, 8, 5, 3], [3, 0, 5, 3, 0, 8, 5, 0, 3], [8, 0, 0, 5, 4, 8, 0, 8, 2], [0, 0, 8, 2, 3, 0, 0, 0, 3], [0, 8, 5, 0, 5, 8, 3, 2, 2], [8, 0, 0, 8, 2, 5, 0, 0, 8], [5, 0, 5, 2, 0, 0, 3, 8, 3]]),
    ([[0, 0, 0, 2, 0, 0, 0], [0, 0, 3, 5, 0, 8, 3], [0, 8, 5, 5, 8, 0, 0], [8, 5, 0, 3, 2, 2, 0], [0, 8, 0, 0, 8, 5, 0], [0, 0, 3, 8, 2, 0, 8], [8, 2, 0, 0, 2, 0, 0]], [[0, 0, 0, 2, 0, 0, 0], [0, 0, 3, 5, 0, 8, 3], [0, 8, 5, 5, 8, 0, 0], [8, 5, 0, 4, 2, 2, 0], [0, 8, 0, 0, 8, 5, 0], [0, 0, 3, 8, 2, 0, 8], [8, 2, 0, 0, 2, 0, 0]]),
    ([[0, 0, 0, 8, 5, 0, 3, 0, 0], [8, 0, 3, 2, 8, 8, 5, 0, 0], [0, 8, 0, 8, 5, 3, 0, 0, 0], [0, 0, 0, 2, 2, 0, 2, 3, 8], [3, 2, 8, 5, 0, 0, 8, 5, 0], [0, 0, 0, 0, 5, 8, 0, 0, 2], [5, 0, 3, 0, 0, 2, 0, 0, 8], [8, 5, 0, 0, 2, 0, 2, 8, 5], [0, 8, 3, 8, 5, 0, 0, 2, 0]], [[0, 0, 0, 8, 5, 0, 3, 0, 0], [8, 0, 3, 2, 8, 8, 5, 0, 0], [0, 8, 0, 8, 5, 3, 0, 0, 0], [0, 0, 0, 2, 2, 0, 2, 3, 8], [3, 2, 8, 5, 4, 0, 8, 5, 0], [0, 0, 0, 0, 5, 8, 0, 0, 2], [5, 0, 3, 0, 0, 2, 0, 0, 8], [8, 5, 0, 0, 2, 0, 2, 8, 5], [0, 8, 3, 8, 5, 0, 0, 2, 0]]),
]

for i, example in enumerate(examples):
    print(f"Example {i + 1}:")
    analysis_results = analyze_example(example[0], example[1])
    pretty_print_analysis(analysis_results)
    print("-" * 20)