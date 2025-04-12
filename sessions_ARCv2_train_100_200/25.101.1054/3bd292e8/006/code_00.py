# Tool Code for Refined Propagation Hypothesis (8-way seed, 4-way spread)
import numpy as np
from collections import deque

def _is_valid(r, c, height, width):
    """Checks if coordinates are within grid bounds."""
    return 0 <= r < height and 0 <= c < width

def solve_via_refined_propagation(input_grid):
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    output_np = np.full_like(input_np, -1) # Temp grid
    
    queue = deque()
    
    # Deltas for 8-way adjacency check (for seeding)
    deltas_8way = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    # Deltas for 4-way propagation
    deltas_4way = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # Step 1 & 2: Initialize Output and Identify Seed Gray Pixels (using 8-way check)
    for r in range(height):
        for c in range(width):
            if input_np[r, c] == 2: # Red pixel
                output_np[r, c] = 2
            elif input_np[r, c] == 7: # Orange pixel
                is_adjacent_to_red_8way = False
                # Check 8 neighbors in the *input* grid for Red
                for dr, dc in deltas_8way:
                    nr, nc = r + dr, c + dc
                    if _is_valid(nr, nc, height, width) and input_np[nr, nc] == 2:
                        is_adjacent_to_red_8way = True
                        break
                
                if is_adjacent_to_red_8way:
                    # This Orange pixel is 8-way adjacent to Red -> Seed Gray pixel
                    output_np[r, c] = 5 # Mark as Gray
                    queue.append((r, c)) # Add to propagation queue
                else:
                    # Not adjacent to Red -> Tentatively mark as Green
                    output_np[r, c] = 3 
            else:
                 # Copy any other colors directly
                 output_np[r, c] = input_np[r, c]

    # Step 3: Propagate Gray using BFS (using 4-way check)
    processed_for_propagation = set(queue) # Keep track of items added to queue to avoid duplicates

    while queue:
        r, c = queue.popleft() # Get coordinates of a Gray pixel
        
        # Examine 4 neighbors for propagation
        for dr, dc in deltas_4way:
            nr, nc = r + dr, c + dc
            neighbor_pos = (nr, nc)
            
            # Check if neighbor is valid, is currently marked as Green (3), 
            # and hasn't already been added to the queue
            if _is_valid(nr, nc, height, width) and output_np[nr, nc] == 3 and neighbor_pos not in processed_for_propagation:
                # Propagate Gray: Change Green neighbor to Gray
                output_np[nr, nc] = 5
                # Add the newly Gray pixel to the queue to continue propagation
                queue.append(neighbor_pos)
                processed_for_propagation.add(neighbor_pos)

    # Step 4: Final Output
    output_grid = output_np.tolist()
    return output_grid

# --- Test Cases ---
train_1_input = [[7, 7, 2, 7, 7, 7, 7], [7, 7, 2, 2, 2, 7, 7], [7, 7, 7, 7, 2, 7, 7], [2, 2, 7, 7, 2, 2, 2], [7, 2, 7, 7, 7, 7, 7], [7, 2, 2, 2, 2, 7, 7], [7, 7, 7, 7, 2, 7, 7]]
train_1_output_expected = [[3, 3, 2, 5, 5, 5, 5], [3, 3, 2, 2, 2, 5, 5], [3, 3, 3, 3, 2, 5, 5], [2, 2, 3, 3, 2, 2, 2], [5, 2, 3, 3, 3, 3, 3], [5, 2, 2, 2, 2, 3, 3], [5, 5, 5, 5, 2, 3, 3]]
train_2_input = [[2, 7, 7, 7, 7, 7, 7], [2, 7, 7, 7, 7, 7, 7], [2, 7, 7, 7, 7, 7, 7], [2, 2, 2, 7, 7, 7, 7], [7, 7, 2, 7, 7, 7, 7], [7, 7, 2, 2, 2, 7, 7], [7, 7, 7, 7, 2, 2, 2]]
train_2_output_expected = [[2, 3, 3, 3, 3, 3, 3], [2, 3, 3, 3, 3, 3, 3], [2, 3, 3, 3, 3, 3, 3], [2, 2, 2, 3, 3, 3, 3], [5, 5, 2, 3, 3, 3, 3], [5, 5, 2, 2, 2, 3, 3], [5, 5, 5, 5, 2, 2, 2]]
train_3_input = [[7, 7, 7, 7, 7, 2, 7, 7], [7, 7, 7, 7, 7, 2, 7, 7], [2, 2, 2, 2, 7, 2, 7, 7], [7, 7, 7, 2, 7, 2, 7, 7], [7, 7, 7, 2, 7, 2, 7, 7], [2, 2, 7, 2, 7, 2, 2, 7], [7, 2, 7, 2, 7, 7, 2, 2], [7, 2, 7, 2, 7, 7, 7, 7]]
train_3_output_expected = [[5, 5, 5, 5, 5, 2, 3, 3], [5, 5, 5, 5, 5, 2, 3, 3], [2, 2, 2, 2, 5, 2, 3, 3], [3, 3, 3, 2, 5, 2, 3, 3], [3, 3, 3, 2, 5, 2, 3, 3], [2, 2, 3, 2, 5, 2, 2, 3], [5, 2, 3, 2, 5, 5, 2, 2], [5, 2, 3, 2, 5, 5, 5, 5]]

# --- Verification ---
result_1 = solve_via_refined_propagation(train_1_input)
result_2 = solve_via_refined_propagation(train_2_input)
result_3 = solve_via_refined_propagation(train_3_input)

print(f"Ex 1 Match: {result_1 == train_1_output_expected}")
# print("Ex 1 Expected:", train_1_output_expected)
# print("Ex 1 Actual:  ", result_1)
print(f"Ex 2 Match: {result_2 == train_2_output_expected}")
# print("Ex 2 Expected:", train_2_output_expected)
# print("Ex 2 Actual:  ", result_2)
print(f"Ex 3 Match: {result_3 == train_3_output_expected}")
# print("Ex 3 Expected:", train_3_output_expected)
# print("Ex 3 Actual:  ", result_3)
