import numpy as np

# Function to safely get pixel color, returning -1 for Out Of Bounds (OOB)
def get_pixel(grid, r, c):
    h, w = grid.shape
    if 0 <= r < h and 0 <= c < w:
        return grid[r, c]
    return -1 # Indicate OOB

def analyze_white_pixel(r, c, input_np, output_np):
    """Analyzes a white input pixel and its expected output pattern."""
    input_height, input_width = input_np.shape
    output_height, output_width = output_np.shape
    
    # Only analyze white input pixels
    if input_np[r, c] != 0:
        return None 

    pixel_info = {
        "coord": (r, c),
        "expected_pattern": "Unknown",
        "all_cardinal_white": True,
        "all_moore_white": True,
    }

    # Determine Expected Output Pattern based on the ground truth output
    out_r, out_c = 2 * r, 2 * c
    # Check if the output block coordinates are valid
    if out_r + 1 < output_height and out_c + 1 < output_width:
        # Check for diagonal blue pattern [[1, 0], [0, 1]]
        if output_np[out_r, out_c] == 1 and output_np[out_r+1, out_c+1] == 1 and \
           output_np[out_r, out_c+1] == 0 and output_np[out_r+1, out_c] == 0:
            pixel_info["expected_pattern"] = "Blue"
        # Check for white block [[0, 0], [0, 0]]
        elif output_np[out_r, out_c] == 0 and output_np[out_r+1, out_c+1] == 0 and \
             output_np[out_r, out_c+1] == 0 and output_np[out_r+1, out_c] == 0:
             pixel_info["expected_pattern"] = "White"
        # If the pattern is neither, it might be part of an expanded non-white block, 
        # or the pattern is different. Mark as Unknown/Other for this analysis.
        else:
             pixel_info["expected_pattern"] = "Other/Overwritten"
             return None # Exclude these from neighbourhood analysis for Blue/White patterns

    else:
         # Handle cases where the 2x2 block would be partially out of bounds
         # (Shouldn't happen if output is always 2H x 2W)
         return None 

    # Analyze Neighbours in the input grid
    neighbour_coords = [
        # Cardinal
        (r-1, c), (r+1, c), (r, c-1), (r, c+1),
        # Diagonal
        (r-1, c-1), (r-1, c+1), (r+1, c-1), (r+1, c+1)
    ]
    
    cardinal_indices = {0, 1, 2, 3} # Indices corresponding to cardinal neighbours

    for i, (nr, nc) in enumerate(neighbour_coords):
        color = get_pixel(input_np, nr, nc)
        is_cardinal = (i in cardinal_indices)

        # Check if valid neighbour (not OOB) is non-white
        if color > 0: 
             pixel_info["all_moore_white"] = False
             if is_cardinal:
                 pixel_info["all_cardinal_white"] = False
        # OOB neighbours (color == -1) don't affect the 'all white' status
        
    return pixel_info

# --- Load Data ---
# Example 1
input_1 = np.array([[2, 0], [0, 0]])
output_1 = np.array([[2, 2, 0, 0], [2, 2, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
# Example 2
input_2 = np.array([[0,0,0,5,0],[0,5,0,0,0],[0,0,0,0,0],[0,5,0,0,0],[0,0,0,0,0]])
output_2 = np.array([[1,0,0,0,0,0,5,5,0,0],[0,1,0,0,0,0,5,5,0,0],[0,0,5,5,0,0,0,0,1,0],[0,0,5,5,0,0,0,0,0,1],[1,0,0,0,1,0,0,0,0,0],[0,1,0,0,0,1,0,0,0,0],[0,0,5,5,0,0,1,0,0,0],[0,0,5,5,0,0,0,1,0,0],[0,0,0,0,1,0,0,0,1,0],[0,0,0,0,0,1,0,0,0,1]])
# Example 3
input_3 = np.array([[0,0,0,0,0,3],[0,0,0,0,0,0],[0,3,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]])
output_3 = np.array([[0,0,0,0,0,0,0,0,0,0,3,3],[0,0,0,0,0,0,0,0,0,0,3,3],[1,0,0,0,0,0,0,0,0,0,0,0],[0,1,0,0,0,0,0,0,0,0,0,0],[0,0,3,3,0,0,0,0,0,0,0,0],[0,0,3,3,0,0,0,0,0,0,0,0],[0,0,0,0,1,0,0,0,0,0,0,0],[0,0,0,0,0,1,0,0,0,0,0,0],[0,0,0,0,0,0,1,0,0,0,0,0],[0,0,0,0,0,0,0,1,0,0,0,0],[0,0,0,0,0,0,0,0,1,0,0,0],[0,0,0,0,0,0,0,0,0,1,0,0]])

datasets = {
    "Ex1": (input_1, output_1),
    "Ex2": (input_2, output_2),
    "Ex3": (input_3, output_3)
}

# --- Analyze ---
results = {}
for name, (input_grid, output_grid) in datasets.items():
    h, w = input_grid.shape
    results[name] = []
    for r in range(h):
        for c in range(w):
             analysis = analyze_white_pixel(r, c, input_grid, output_grid)
             if analysis: # Add only if analysis resulted in Blue or White pattern
                 results[name].append(analysis)

# --- Report ---
print("White Pixel Analysis Summary (Based on Expected Outputs):")
for name, analyses in results.items():
    print(f"\n--- {name} ---")
    blue_pattern_pixels = [info for info in analyses if info["expected_pattern"] == "Blue"]
    white_block_pixels = [info for info in analyses if info["expected_pattern"] == "White"]

    print(f"  Pixels resulting in BLUE pattern ({len(blue_pattern_pixels)}):")
    print(f"    Coords: {[info['coord'] for info in blue_pattern_pixels]}")
    print(f"    All Cardinal White?: {[info['all_cardinal_white'] for info in blue_pattern_pixels]}")
    print(f"    All Moore White?:    {[info['all_moore_white'] for info in blue_pattern_pixels]}")
    
    print(f"  Pixels resulting in WHITE block ({len(white_block_pixels)}):")
    print(f"    Coords: {[info['coord'] for info in white_block_pixels]}")
    print(f"    All Cardinal White?: {[info['all_cardinal_white'] for info in white_block_pixels]}")
    print(f"    All Moore White?:    {[info['all_moore_white'] for info in white_block_pixels]}")

    # Highlight contradictions to the simple 'all cardinal white -> blue' rule
    blue_with_non_white_cardinal = [p['coord'] for p in blue_pattern_pixels if not p['all_cardinal_white']]
    white_with_all_white_cardinal = [p['coord'] for p in white_block_pixels if p['all_cardinal_white']]
    
    if blue_with_non_white_cardinal:
        print(f"    (!) CONTRADICTION: Blue pattern despite non-white Cardinal neighbour(s): {blue_with_non_white_cardinal}")
    if white_with_all_white_cardinal:
         print(f"    (!) CONTRADICTION: White block despite all Cardinal neighbours being white: {white_with_all_white_cardinal}")

    # Further detail on Moore neighbourhood status (as it also doesn't explain the pattern)
    blue_with_all_white_moore = [p['coord'] for p in blue_pattern_pixels if p['all_moore_white']]
    white_with_all_white_moore = [p['coord'] for p in white_block_pixels if p['all_moore_white']]
    if blue_with_all_white_moore:
        print(f"    (i) Note: Blue pattern occurred even when ALL Moore neighbours were white: {blue_with_all_white_moore}")
    if white_with_all_white_moore:
         print(f"    (i) Note: White block occurred even when ALL Moore neighbours were white: {white_with_all_white_moore}")
