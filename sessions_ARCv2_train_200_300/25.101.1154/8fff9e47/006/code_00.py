import numpy as np
import math

# --- Data ---
# Example 1
input_1 = [[1, 3, 9, 4], [5, 5, 2, 8], [9, 8, 3, 1], [4, 0, 1, 4], [2, 3, 6, 5], [3, 9, 8, 0]]
expected_1 = [[6, 6, 6, 6, 6, 6, 5, 5, 5, 5, 5, 5], [6, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 5], [6, 2, 3, 3, 3, 3, 1, 1, 1, 1, 3, 5], [6, 2, 3, 9, 9, 9, 8, 8, 8, 1, 3, 5], [6, 2, 3, 9, 9, 9, 4, 4, 8, 1, 3, 5], [6, 2, 3, 9, 9, 1, 3, 4, 8, 1, 3, 5], [8, 3, 1, 4, 2, 5, 5, 8, 0, 4, 9, 0], [8, 3, 1, 4, 2, 2, 8, 8, 0, 4, 9, 0], [8, 3, 1, 4, 4, 4, 0, 0, 0, 4, 9, 0], [8, 3, 1, 1, 1, 1, 4, 4, 4, 4, 9, 0], [8, 3, 3, 3, 3, 3, 9, 9, 9, 9, 9, 0], [8, 8, 8, 8, 8, 8, 0, 0, 0, 0, 0, 0]]
# Example 2
input_2 = [[9, 1, 1, 7, 7, 9], [2, 0, 7, 7, 0, 3], [2, 8, 7, 7, 2, 1], [5, 3, 9, 7, 7, 8]]
expected_2 = [[2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1], [2, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 1], [2, 7, 2, 2, 2, 2, 8, 8, 8, 8, 7, 1], [2, 7, 2, 7, 7, 7, 9, 9, 9, 8, 7, 1], [2, 7, 2, 7, 1, 1, 7, 7, 9, 8, 7, 1], [2, 7, 2, 7, 1, 9, 1, 7, 9, 8, 7, 1], [7, 9, 5, 0, 7, 2, 0, 7, 3, 3, 7, 8], [7, 9, 5, 0, 7, 7, 7, 7, 3, 3, 7, 8], [7, 9, 5, 0, 0, 0, 3, 3, 3, 3, 7, 8], [7, 9, 5, 5, 5, 5, 3, 3, 3, 3, 7, 8], [7, 9, 9, 9, 9, 9, 7, 7, 7, 7, 7, 8], [7, 7, 7, 7, 7, 7, 8, 8, 8, 8, 8, 8]]

examples = {
    "Example 1": {"input": input_1, "expected": expected_1},
    "Example 2": {"input": input_2, "expected": expected_2}
}

# --- Analysis Function ---
def derive_map_and_boundary(input_grid, expected_output, scale_h, scale_w, block_shape_str):
    input_np = np.array(input_grid)
    expected_np = np.array(expected_output)
    H_in, W_in = input_np.shape
    H_out, W_out = 12, 12

    possible_maps = {}
    oob_trigger_cases = [] # Cases where expected value requires looking OOB based on preliminary map

    # First pass: find potential offsets for each relative position based on in-bounds matches
    for r in range(H_out):
        for c in range(W_out):
            if H_in == 0 or W_in == 0: continue # Skip if input is empty
            i = r // scale_h
            j = c // scale_w
            # Ensure i, j are valid indices for input_np - crucial if H_in/W_in are not divisors of 12
            # But problem statement implies they are. Add check just in case.
            if not (0 <= i < H_in and 0 <= j < W_in):
                print(f"Warning: Calculated input index ({i},{j}) is out of bounds for input shape ({H_in},{W_in}). Skipping output pixel ({r},{c}).")
                continue

            rel_r = r % scale_h
            rel_c = c % scale_w
            expected_val = expected_np[r, c]
            current_key = (rel_r, rel_c)

            possible_offsets_for_this_pixel = set()
            match_found_in_bounds = False
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    nr, nc = i + dr, j + dc
                    if 0 <= nr < H_in and 0 <= nc < W_in:
                        neighbor_val = input_np[nr, nc]
                        if neighbor_val == expected_val:
                            possible_offsets_for_this_pixel.add((dr, dc))
                            match_found_in_bounds = True
            
            # Store the possibilities for refining the map
            if match_found_in_bounds:
                 if current_key not in possible_maps:
                     possible_maps[current_key] = possible_offsets_for_this_pixel.copy()
                 else:
                     possible_maps[current_key].intersection_update(possible_offsets_for_this_pixel)
            else:
                 # If no in-bounds neighbor matches, this case *must* involve boundary handling
                 oob_trigger_cases.append({'r': r, 'c': c, 'i': i, 'j': j, 'rel': current_key, 'expected': expected_val, 'center': input_np[i,j]})

    # Refine map: find unique offset for each relative position
    final_map = {}
    ambiguous_keys = {}
    for key, offsets in possible_maps.items():
       if len(offsets) == 1:
           final_map[key] = list(offsets)[0]
       else:
           # Keep unresolved ones - maybe boundary cases resolve them
           ambiguous_keys[key] = offsets

    # Analyze boundary cases
    boundary_rule_hypothesis = "Unknown"
    consistent = True
    
    # Combine cases: those where no in-bounds neighbor matched, 
    # AND those where the derived unique map points OOB.
    all_boundary_candidates = oob_trigger_cases[:]
    
    for r in range(H_out):
         for c in range(W_out):
            if H_in == 0 or W_in == 0: continue
            i = r // scale_h
            j = c // scale_w
            if not (0 <= i < H_in and 0 <= j < W_in): continue
            rel_r = r % scale_h
            rel_c = c % scale_w
            key = (rel_r, rel_c)
            expected_val = expected_np[r,c]
            
            if key in final_map:
                dr, dc = final_map[key]
                nr, nc = i + dr, j + dc
                if not (0 <= nr < H_in and 0 <= nc < W_in):
                    # Check if this wasn't already caught by oob_trigger_cases
                    is_new = True
                    for case in oob_trigger_cases:
                        if case['r'] == r and case['c'] == c:
                            is_new = False
                            break
                    if is_new:
                         all_boundary_candidates.append({'r': r, 'c': c, 'i': i, 'j': j, 'rel': key, 'expected': expected_val, 'center': input_np[i,j], 'mapped_offset': final_map[key]})

    if not all_boundary_candidates:
         boundary_rule_hypothesis = "Not Applicable (No OOB cases)"
    else:
        # Check if all boundary cases match the center pixel
        all_match_center = True
        for case in all_boundary_candidates:
             if case['expected'] != case['center']:
                 all_match_center = False
                 break
        if all_match_center:
             boundary_rule_hypothesis = "Use Center Pixel"
        else:
             # Check if they match a fixed color (less likely)
             first_oob_color = all_boundary_candidates[0]['expected']
             all_match_fixed = True
             for case in all_boundary_candidates:
                 if case['expected'] != first_oob_color:
                     all_match_fixed = False
                     break
             if all_match_fixed:
                 boundary_rule_hypothesis = f"Use Fixed Color {first_oob_color}"
             else:
                 boundary_rule_hypothesis = "Inconsistent/Complex"

    # Check if boundary analysis resolved ambiguous keys
    resolved_ambiguities = {}
    still_ambiguous = {}
    for key, offsets in ambiguous_keys.items():
        possible_resolved_offsets = set()
        # Find output pixels with this rel key
        for r in range(H_out):
            for c in range(W_out):
                if H_in == 0 or W_in == 0: continue
                i = r // scale_h
                j = c // scale_w
                if not (0 <= i < H_in and 0 <= j < W_in): continue
                rel_r = r % scale_h
                rel_c = c % scale_w
                
                if (rel_r, rel_c) == key:
                    expected_val = expected_np[r,c]
                    center_val = input_np[i,j]
                    
                    current_pixel_possible = set()
                    for dr, dc in offsets: # Check only the remaining ambiguous offsets
                         nr, nc = i + dr, j + dc
                         if 0 <= nr < H_in and 0 <= nc < W_in:
                             if input_np[nr,nc] == expected_val:
                                 current_pixel_possible.add((dr, dc))
                         elif boundary_rule_hypothesis == "Use Center Pixel":
                             if center_val == expected_val:
                                 current_pixel_possible.add((dr, dc)) # This offset works if OOB maps to center
                         # Add other boundary rules here if needed
                         
                    if not possible_resolved_offsets:
                         possible_resolved_offsets = current_pixel_possible.copy()
                    else:
                         possible_resolved_offsets.intersection_update(current_pixel_possible)
                         
        if len(possible_resolved_offsets) == 1:
             resolved_ambiguities[key] = list(possible_resolved_offsets)[0]
        else:
             still_ambiguous[key] = offsets # Still couldn't resolve

    final_map.update(resolved_ambiguities)

    print(f"\n--- Analysis for Block Shape {block_shape_str} ---")
    print(f"Derived Neighbor Offset Map:")
    # Print map sorted by relative coordinates for clarity
    for r in range(scale_h):
        row_str = []
        for c in range(scale_w):
            key = (r,c)
            offset = final_map.get(key, "???")
            row_str.append(f"({r},{c})->{offset}")
        print("  " + " | ".join(row_str))
        
    if still_ambiguous:
        print("Still Ambiguous Mappings:")
        for key, offsets in still_ambiguous.items():
             print(f"  {key}: {offsets}")
    print(f"Boundary Handling Rule Hypothesis: {boundary_rule_hypothesis}")
    # print("Boundary Cases Considered:")
    # for case in all_boundary_candidates:
    #     print(f"  Out({case['r']},{case['c']}) Rel:{case['rel']} Exp:{case['expected']} Ctr:{case['center']}")


# --- Run Analysis ---
# Example 1
H1, W1 = np.array(input_1).shape
scale_h1, scale_w1 = 12 // H1, 12 // W1
derive_map_and_boundary(input_1, expected_1, scale_h1, scale_w1, f"({scale_h1}x{scale_w1})")

# Example 2
H2, W2 = np.array(input_2).shape
scale_h2, scale_w2 = 12 // H2, 12 // W2
derive_map_and_boundary(input_2, expected_2, scale_h2, scale_w2, f"({scale_h2}x{scale_w2})")
