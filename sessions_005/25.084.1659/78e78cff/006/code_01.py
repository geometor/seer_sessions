        border_seeds = set()
        # Find background pixels on the border
        for c in range(width):
            if inp[0, c] == background_color: border_seeds.add((0, c))
            if inp[height - 1, c] == background_color: border_seeds.add((height - 1, c))
        for r in range(1, height - 1):
            if inp[r, 0] == background_color: border_seeds.add((r, 0))
            if inp[r, width - 1] == background_color: border_seeds.add((r, width - 1))