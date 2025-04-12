shift = (6 * v0) % 9 # Correct: for v0=3, shift=0. for v0=5, shift=3.
dist = abs(r - r0) + abs(c - c0) # Correct Manhattan distance
index = (dist + shift) % 9 # Correct index calculation
output[r, c] = BASE_SEQ[index] # Correct lookup