from simulation import generate_scenario

NUM_DEV = 1000                      # number of devices
NUM_TIMEW = 100                     # number of time windows
BATCH_SIZES = [5, 10, 50]           # pseudonyms in one batch (n)
REVOKE_PROBS = [0.01, 0.05, 0.10]   # share of revoked devices (p)
REPETITIONS = 3                     # runs with different seeds


# number of entries in the single filter (original design) during window t
def original_filter_size(revoked, t):
    size = 0
    for device, window, k in revoked:
        last_window = window + k - 1
        if window <= t <= last_window:
            size += last_window - t + 1     # pseudonyms not expired yet
    return size


# number of entries in the filter of window t (proposed design)
def window_filter_size(revoked, t):
    size = 0
    for device, window, k in revoked:
        if window <= t <= window + k - 1:
            size += 1                       # one pseudonym per revoked device
    return size


for n in BATCH_SIZES:
    for p in REVOKE_PROBS:
        max_original = 0
        max_window = 0

        for seed in range(REPETITIONS):
            revoked = generate_scenario(NUM_DEV, NUM_TIMEW, n, p, seed)

            for t in range(NUM_TIMEW + n):
                max_original = max(max_original, original_filter_size(revoked, t))
                max_window = max(max_window, window_filter_size(revoked, t))

        print(f"n={n:3}  p={p:.2f}:  one filter {max_original:4} entries,  "f"window filter {max_window:3} entries")