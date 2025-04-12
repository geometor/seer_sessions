# Tool Code for Propagation Hypothesis
import numpy as np
from collections import deque

def solve_via_propagation(input_grid):
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    output_np = np.full_like(input_np, -1) # Temp grid
    
    q = deque()
    initial_gray_candidates = [] # Pixels that might start the gray propagation

    # Step 1 & 2: Initialize Output with Red, Mark initial Gray candidates, others potentially Green
    for r in range(height):
        for c in range(width):
            if input_np[r, c] == 2: # Red
                output_np[r, c] = 2
            elif input_np[r, c] == 7: # Orange
                # Check 8-way adjacency to Red
                is_adj_to_red = False
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0: continue
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < height and 0 <= nc < width and input_np[nr, nc] == 2:
                            is_adj_to_red = True
                            break
                    if is_adj_to_red: break
                
                if is_adj_to_red:
                    output_np[r, c] = 5 # Initial Gray
                    q.append((r, c)) # Add to propagation queue
                else:
                    output_np[r, c] = 3 # Potential Green
            else: # Other colors (if any)
                 output_np[r, c] = input_np[r, c] # Copy them

    # Step 3 & 4: Propagation BFS
    visited_prop = set(q) # Keep track of visited during propagation

    deltas = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    while q:
        r, c = q.popleft()
        
        for dr, dc in deltas:
            nr, nc = r + dr, c + dc
            
            # Check bounds and if the neighbor is a 'potential Green'
            if 0 <= nr < height and 0 <= nc < width and output_np[nr, nc] == 3:
                 neighbor_pos = (nr, nc)
                 # Check if visited in this propagation step to avoid cycles/redundancy
                 # Wait, we just need to check if it's Green(3) and change it.
                 # No need for visited_prop, just check output_np value.
                 output_np[nr, nc] = 5 # Change to Gray
                 q.append(neighbor_pos) # Add to queue to propagate further

    # Final check: any -1 left should not happen if all input pixels are handled
    # Convert potential Green (3) that were never turned Gray back to Green (3).
    # No, they are already 3. The process is complete.
    
    return output_np.tolist()

# --- Test Cases ---
# (Use the same test cases as before)
train_1_input = [[7, 7, 2, 7, 7, 7, 7], [7, 7, 2, 2, 2, 7, 7], [7, 7, 7, 7, 2, 7, 7], [2, 2, 7, 7, 2, 2, 2], [7, 2, 7, 7, 7, 7, 7], [7, 2, 2, 2, 2, 7, 7], [7, 7, 7, 7, 2, 7, 7]]
train_1_output_expected = [[3, 3, 2, 5, 5, 5, 5], [3, 3, 2, 2, 2, 5, 5], [3, 3, 3, 3, 2, 5, 5], [2, 2, 3, 3, 2, 2, 2], [5, 2, 3, 3, 3, 3, 3], [5, 2, 2, 2, 2, 3, 3], [5, 5, 5, 5, 2, 3, 3]]
train_2_input = [[2, 7, 7, 7, 7, 7, 7], [2, 7, 7, 7, 7, 7, 7], [2, 7, 7, 7, 7, 7, 7], [2, 2, 2, 7, 7, 7, 7], [7, 7, 2, 7, 7, 7, 7], [7, 7, 2, 2, 2, 7, 7], [7, 7, 7, 7, 2, 2, 2]]
train_2_output_expected = [[2, 3, 3, 3, 3, 3, 3], [2, 3, 3, 3, 3, 3, 3], [2, 3, 3, 3, 3, 3, 3], [2, 2, 2, 3, 3, 3, 3], [5, 5, 2, 3, 3, 3, 3], [5, 5, 2, 2, 2, 3, 3], [5, 5, 5, 5, 2, 2, 2]]
train_3_input = [[7, 7, 7, 7, 7, 2, 7, 7], [7, 7, 7, 7, 7, 2, 7, 7], [2, 2, 2, 2, 7, 2, 7, 7], [7, 7, 7, 2, 7, 2, 7, 7], [7, 7, 7, 2, 7, 2, 7, 7], [2, 2, 7, 2, 7, 2, 2, 7], [7, 2, 7, 2, 7, 7, 2, 2], [7, 2, 7, 2, 7, 7, 7, 7]]
train_3_output_expected = [[5, 5, 5, 5, 5, 2, 3, 3], [5, 5, 5, 5, 5, 2, 3, 3], [2, 2, 2, 2, 5, 2, 3, 3], [3, 3, 3, 2, 5, 2, 3, 3], [3, 3, 3, 2, 5, 2, 3, 3], [2, 2, 3, 2, 5, 2, 2, 3], [5, 2, 3, 2, 5, 5, 2, 2], [5, 2, 3, 2, 5, 5, 5, 5]]

result_1 = solve_via_propagation(train_1_input)
result_2 = solve_via_propagation(train_2_input)
result_3 = solve_via_propagation(train_3_input)

print(f"Ex 1 Match: {result_1 == train_1_output_expected}")
print(f"Ex 2 Match: {result_2 == train_2_output_expected}")
print(f"Ex 3 Match: {result_3 == train_3_output_expected}")
