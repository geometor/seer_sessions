import numpy as np

def analyze_example(input_grid, output_grid):
    inp = np.array(input_grid, dtype=int)
    out = np.array(output_grid, dtype=int)
    H_in, W_in = inp.shape
    H_out, W_out = out.shape if out.size > 0 else (0, 0)

    # --- Input Analysis ---
    S_in, cell_size_in, M_in, N_in = -1, -1, -1, -1
    key_colors_set = set()
    active_input_cols = []
    key_map = {} # {cell_col: key_color}

    # Find S (Separator distance)
    first_gray_row_idx = np.where(np.any(inp == 5, axis=1))[0]
    first_gray_col_idx = np.where(np.any(inp == 5, axis=0))[0]

    if len(first_gray_row_idx) > 0:
        S_in = first_gray_row_idx[0] + 1
    elif len(first_gray_col_idx) > 0:
        S_in = first_gray_col_idx[0] + 1
    # Add case for no gray lines later if needed, assume S=4 for now if not found?
    # Forcing S=4 if not found via gray lines, based on manual observation
    if S_in <= 0:
         S_in = 4 # Default based on observation if detection fails

    cell_size_in = S_in - 1

    if cell_size_in > 0:
        # Find M, N based on content (non-zero, non-gray)
        content_coords = np.argwhere((inp != 0) & (inp != 5))
        if content_coords.size > 0:
            last_content_r = content_coords[:, 0].max()
            last_content_c = content_coords[:, 1].max()
            M_in = (last_content_r // S_in) + 1
            N_in = (last_content_c // S_in) + 1
        else: # No content - infer from size?
             M_in = H_in // S_in if S_in > 0 else 1
             N_in = W_in // S_in if S_in > 0 else 1
             M_in = max(1, M_in)
             N_in = max(1, N_in)

        # Key detection (last row with any non-zero content)
        non_zero_rows = np.where(np.any(inp != 0, axis=1))[0]
        if len(non_zero_rows) > 0:
            last_row_idx = non_zero_rows[-1]
            key_row = inp[last_row_idx, :]
            key_indices = np.where(key_row != 0)[0]
            processed_cells = set()
            temp_active_cols = []
            for idx in key_indices:
                color = key_row[idx]
                cell_col = idx // S_in
                if cell_col < N_in and cell_col not in processed_cells:
                    key_colors_set.add(color)
                    temp_active_cols.append(cell_col)
                    key_map[cell_col] = color
                    processed_cells.add(cell_col)
            active_input_cols = sorted(temp_active_cols)

    # --- Output Analysis ---
    # Infer output cell size and dimensions
    output_cell_size = -1
    M_out, N_out = -1, -1
    if M_in > 0 and H_out > 0:
        M_out = M_in
        output_cell_size = H_out // M_out
    if len(active_input_cols) > 0 and W_out > 0 and output_cell_size > 0:
         N_out = len(active_input_cols)
         # Sanity check N' derived from active cols vs calculated from width/cell_size
         if N_out != (W_out // output_cell_size):
              pass # Discrepancy noted
    output_colors = set(np.unique(out[out != 0])) if out.size > 0 else set()


    # Determine Color Map Rule based on UKC
    ukc_tuple = tuple(sorted(list(key_colors_set)))
    color_map_rule_applied = "Unknown"
    if ukc_tuple == (1, 6, 7): color_map_rule_applied = "Map1={6:7, 7:1, 1:1}"
    if ukc_tuple == (3, 7, 9): color_map_rule_applied = "Map2={3:7, 7:3, 9:9}"
    if ukc_tuple == (3, 6, 8): color_map_rule_applied = "Map3={3:6, 8:8, 6:6}"


    return {
        "Input Size": f"{H_in}x{W_in}",
        "Output Size": f"{H_out}x{W_out}",
        "Input S": S_in,
        "Input Cell Size": cell_size_in,
        "Input Cells (MxN)": f"{M_in}x{N_in}" if M_in>0 and N_in>0 else "Unknown",
        "Keys Found": len(key_colors_set),
        "Key Colors UKC": sorted(list(key_colors_set)),
        "Active Input Cols (c)": active_input_cols,
        "Input Key Map {c: K}": key_map,
        "Color Map Rule": color_map_rule_applied,
        "Output Cell Size": output_cell_size if output_cell_size > 0 else "Unknown",
        "Output Cells (M'xN')": f"{M_out}x{N_out}" if M_out > 0 and N_out > 0 else "Unknown",
        "Output Colors": sorted(list(output_colors)),
    }

# Example Data (as provided in the prompt)
train_data = [
    { # train_1
        "input": [[2,2,2,5,1,1,1,5,4,4,4],[2,2,2,0,1,0,1,0,0,4,0],[2,2,2,5,1,1,1,5,4,4,4],[5,0,5,5,5,0,5,5,5,0,5],[0,0,0,5,0,4,4,5,1,0,0],[0,0,0,0,0,0,4,0,0,1,0],[2,0,0,5,0,0,0,5,0,0,1],[5,0,5,5,5,0,5,5,5,0,5],[0,0,0,5,0,0,0,5,0,0,0],[0,6,0,0,0,7,0,0,0,1,0]],
        "output": [[7,7,7,1,1,1,1,1,1],[7,0,7,0,1,0,0,1,0],[7,7,7,1,1,1,1,1,1],[0,0,0,7,7,7,1,1,1],[0,0,0,7,0,7,0,1,0],[0,0,0,7,7,7,1,1,1],[6,6,6,0,0,0,7,7,7],[6,6,6,0,0,0,7,0,7],[6,6,6,0,0,0,7,7,7]]
    },
    { # train_2
        "input": [[0,1,0,5,2,2,2,5,4,0,4],[1,1,1,0,2,0,2,0,4,4,4],[0,1,0,5,2,2,2,5,0,4,0],[5,0,5,5,5,0,5,5,5,0,5],[0,0,0,5,4,0,0,5,0,0,1],[0,0,0,0,4,0,0,0,0,0,1],[2,2,0,5,0,0,0,5,0,0,0],[5,0,5,5,5,0,5,5,5,0,5],[0,0,0,5,0,0,0,5,0,0,0],[0,7,0,0,0,9,0,0,0,3,0]],
        "output": [[3,0,3,0,0,0,0,7,0],[3,3,3,0,0,0,7,7,7],[0,3,0,0,0,0,0,7,0],[3,0,3,0,0,0,0,7,0],[3,3,3,0,0,0,7,7,7],[0,3,0,0,0,0,0,7,0],[9,9,9,9,9,9,0,0,0],[9,0,9,9,0,9,0,0,0],[9,9,9,9,9,9,0,0,0]]
    },
    { # train_3
        "input": [[1,1,1,0,1,5,2,2,2,2,2,5,0,4,0,0,4],[1,0,1,1,1,0,0,2,0,2,0,0,4,4,4,4,4],[1,1,1,0,1,5,2,0,2,0,2,5,0,4,0,0,4],[1,0,0,0,1,0,2,0,2,0,2,0,0,4,4,4,4],[1,1,1,1,1,5,2,2,2,2,2,5,4,4,0,4,4],[5,0,5,0,5,5,5,0,5,0,5,5,5,0,5,0,5],[4,0,0,0,0,5,0,0,0,0,0,5,0,2,2,2,2],[4,0,0,0,0,0,0,0,0,0,0,0,0,2,2,0,0],[4,4,0,0,0,5,0,0,0,0,0,0,0,0,0,0,0],[0,4,4,0,0,0,1,0,0,0,0,0,0,0,0,0,0],[0,0,4,0,0,5,1,1,0,0,0,5,0,0,0,0,0],[5,0,5,0,5,5,5,0,5,0,5,5,5,0,5,0,5],[0,0,0,0,0,5,0,0,0,0,0,5,0,0,0,0,0],[0,0,3,0,0,0,0,0,8,0,0,0,0,0,6,0,0]],
        "output": [[0,6,0,0,6,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8],[6,6,6,6,6,0,8,0,8,0,0,8,0,8,0,0,8,0,8,0,0,8,0,8,0],[0,6,0,0,6,8,0,8,0,8,8,0,8,0,8,8,0,8,0,8,8,0,8,0,8],[0,6,6,6,6,8,0,8,0,8,8,0,8,0,8,8,0,8,0,8,8,0,8,0,8],[6,6,0,6,6,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8],[0,6,0,0,6,8,8,8,8,8,8,8,8,8,8,0,0,0,0,0,0,0,0,0,0],[6,6,6,6,6,0,8,0,8,0,0,8,0,8,0,0,0,0,0,0,0,0,0,0,0],[0,6,0,0,6,8,0,8,0,8,8,0,8,0,8,0,0,0,0,0,0,0,0,0,0],[0,6,6,6,6,8,0,8,0,8,8,0,8,0,8,0,0,0,0,0,0,0,0,0,0],[6,6,0,6,6,8,8,8,8,8,8,8,8,8,8,0,0,0,0,0,0,0,0,0,0],[0,6,0,0,6,0,6,0,0,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[6,6,6,6,6,6,6,6,6,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,6,0,0,6,0,6,0,0,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,6,6,6,6,0,6,6,6,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[6,6,0,6,6,6,6,0,6,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[3,3,3,0,3,0,6,0,0,6,0,6,0,0,6,0,0,0,0,0,0,0,0,0,0],[3,0,3,3,3,6,6,6,6,6,6,6,6,6,6,0,0,0,0,0,0,0,0,0,0],[3,3,3,0,3,0,6,0,0,6,0,6,0,0,6,0,0,0,0,0,0,0,0,0,0],[3,0,0,0,3,0,6,6,6,6,0,6,6,6,6,0,0,0,0,0,0,0,0,0,0],[3,3,3,3,3,6,6,0,6,6,6,6,0,6,6,0,0,0,0,0,0,0,0,0,0],[3,3,3,0,3,3,3,3,0,3,0,6,0,0,6,0,0,0,0,0,0,0,0,0,0],[3,0,3,3,3,3,0,3,3,3,6,6,6,6,6,0,0,0,0,0,0,0,0,0,0],[3,3,3,0,3,3,3,3,0,3,0,6,0,0,6,0,0,0,0,0,0,0,0,0,0],[3,0,0,0,3,3,0,0,0,3,0,6,6,6,6,0,0,0,0,0,0,0,0,0,0],[3,3,3,3,3,3,3,3,3,3,6,6,0,6,6,0,0,0,0,0,0,0,0,0,0]]
    }
]

results = {}
for i, data in enumerate(train_data):
    results[f"train_{i+1}"] = analyze_example(data["input"], data["output"])

import json
print(json.dumps(results, indent=2)) # Use JSON for better readability with numpy types