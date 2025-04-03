import numpy as np
from typing import List, Tuple, Optional

# --- find_pivot and find_movable_block functions as previously defined ---
def find_pivot(grid: np.ndarray, pivot_color: int = 9) -> Optional[int]:
    pivot_indices = np.where(grid == pivot_color)[0]
    if len(pivot_indices) == 1:
        return pivot_indices[0]
    elif len(pivot_indices) == 0: return None
    else: return None

def find_movable_block(grid: np.ndarray, background_color: int = 0, pivot_color: int = 9) -> Optional[Tuple[int, int, int]]:
    block_color = -1
    block_start_index = -1
    block_size = 0
    in_block = False
    for i, pixel in enumerate(grid):
        is_block_pixel = (pixel != background_color and pixel != pivot_color)
        if is_block_pixel and not in_block:
            block_color = pixel
            block_start_index = i
            block_size = 1
            in_block = True
        elif is_block_pixel and in_block:
            if pixel == block_color: block_size += 1
            else: break
        elif not is_block_pixel and in_block:
            break
    if block_start_index != -1: return block_color, block_start_index, block_size
    else: return None
# --- End of helper functions ---

examples = [
    { "input": [0, 3, 3, 3, 3, 3, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], "output": [0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 3, 3, 3, 3, 3, 0, 0, 0, 0] },
    { "input": [0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], "output": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 2, 2, 2, 2, 2, 2, 0, 0, 0] },
    { "input": [0, 0, 0, 0, 0, 0, 4, 4, 4, 4, 4, 4, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0], "output": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 4, 4, 4, 4, 4, 4, 0] }
]

metrics = []

for i, ex in enumerate(examples):
    input_np = np.array(ex["input"], dtype=int)
    grid_size = len(input_np)
    pivot_index = find_pivot(input_np)
    block_info = find_movable_block(input_np)

    if pivot_index is not None and block_info is not None:
        block_color, input_block_start_index, block_size = block_info
        input_block_end_index = input_block_start_index + block_size - 1
        # Ensure block is before pivot
        if input_block_end_index < pivot_index:
            separation_distance = pivot_index - (input_block_end_index + 1)
            output_block_start_index = pivot_index + 1 + separation_distance
            metrics.append({
                "example": i + 1,
                "grid_size": grid_size,
                "pivot_index": int(pivot_index), # Convert numpy int to standard int
                "block_color": int(block_color), # Convert numpy int to standard int
                "block_size": block_size,
                "input_block_start": input_block_start_index,
                "input_block_end": input_block_end_index,
                "separation_distance": int(separation_distance), # Convert numpy int to standard int
                "output_block_start": int(output_block_start_index), # Convert numpy int to standard int
            })
        else:
             metrics.append({
                 "example": i + 1,
                 "error": "Block not entirely before pivot"
             })
    else:
         metrics.append({
            "example": i + 1,
            "error": "Could not find pivot or block"
         })

print(metrics)