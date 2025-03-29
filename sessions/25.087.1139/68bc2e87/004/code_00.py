import numpy as np
import collections # Import collections here

# Using the provided task data structure
task_data = {
    "train": [
        {"input": [[8,8,8,8,8],[8,1,1,1,8],[8,1,2,1,8],[8,1,1,1,8],[8,8,8,8,8]], "output": [[2]]},
        {"input": [[8,8,8,8],[8,3,3,8],[8,3,3,8],[8,8,8,8]], "output": []},
        {"input": [[8,8,8,8,8,8],[8,4,4,4,4,8],[8,4,8,8,4,8],[8,4,8,2,4,8],[8,4,4,4,4,8],[8,8,8,8,8,8]], "output": [[2]]},
        {"input": [[1,1,1],[1,5,1],[1,1,1]], "output": []}
    ]
}

results = ["Error: list index out of range"] * 4 # From user prompt

print("| Example | Input Shape | Input Colors        | Output      | Border Azure (8)? | Red (2) in Input? | Red (2) in Path? (Revised) | Code Result                   | Matches Expected? |")
print("|---------|-------------|---------------------|-------------|-------------------|-------------------|----------------------------|-------------------------------|-------------------|")

for i, example in enumerate(task_data['train']):
    input_grid = np.array(example['input'])
    output_grid = example['output']
    rows, cols = input_grid.shape
    unique_colors = sorted(list(np.unique(input_grid)))

    # Check for Azure (8) connected to border
    border_azure = False
    q = collections.deque()
    visited = np.zeros_like(input_grid, dtype=bool)
    azure_color = 8

    coords_to_check = []
    if rows > 0 and cols > 0:
        # Ensure unique coords, handle 1xN or Nx1 grids
        potential_coords = set()
        for r in range(rows):
            potential_coords.add((r, 0))
            potential_coords.add((r, cols-1))
        for c in range(cols):
            potential_coords.add((0, c))
            potential_coords.add((rows-1, c))
        coords_to_check = list(potential_coords)


    for r, c in coords_to_check:
         # Check bounds just in case (though construction should be safe)
         if 0 <= r < rows and 0 <= c < cols:
             if input_grid[r,c] == azure_color and not visited[r,c]:
                 q.append((r,c))
                 visited[r,c] = True
                 border_azure = True # Found at least one
                 break # Optimization: Found one, enough for check

    red_present_in_input = 2 in unique_colors

    # Determine the sequence of frame colors based on the refined understanding
    # This is a manual trace based on the logic derived earlier
    frame_color_sequence = []
    if i == 0: # Ex 1: 8 (border) -> 1 (frame) -> 2 (inner pixel/region)
        frame_color_sequence = [1] # Only the blue frame color
    elif i == 1: # Ex 2: 8 (border) -> 3 (frame)
        frame_color_sequence = [3] # Only the green frame color
    elif i == 2: # Ex 3: 8 (border) -> 4 (frame) -> 8 (inner frame/region) -> 2 (inner pixel/region)
        # The inner '8' acts as a separator/frame before the '2'
        frame_color_sequence = [4, 8] # Yellow frame, then inner Azure frame
    elif i == 3: # Ex 4: No azure border
         frame_color_sequence = []

    red_in_frame_sequence = 2 in frame_color_sequence

    output_val_str = "[[2]]" if output_grid == [[2]] else "[]"
    code_result_str = results[i]
    # Correct comparison: Check if the code's output matches the *expected* output
    expected_output_str = output_val_str
    if code_result_str == expected_output_str:
        matches_str = "Yes"
    elif "Error" in code_result_str:
         matches_str = "No (Error)"
    else:
         matches_str = f"No (Got {code_result_str})"


    print(f"| {i+1:<7} | {f'{rows}x{cols}':<11} | {str(unique_colors):<19} | {output_val_str:<11} | {str(border_azure):<17} | {str(red_present_in_input):<17} | {str(red_in_frame_sequence):<26} | {code_result_str:<29} | {matches_str:<17} |")