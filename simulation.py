import random

NUM_DEV = 1000    # number of devices
NUM_TIMEW = 100     # number of time windows
n = 10      # size of one package
p = 0.10    # probability of device being revoked


def generate_scenario(NUM_DEV, NUM_TIMEW, n, p, seed):
    revoked = []
    rng = random.Random(seed)
    for i in range(NUM_DEV):
        if rng.random() < p:
            rev_window = rng.randint(0, NUM_TIMEW-1)     # random window of revocation
            offset = rng.randint(0, n-1)                 # random shift of a package
            batch_start = rev_window - ((rev_window - offset) % n)      # where the batch starts
            batch_end = batch_start + n-1
            k = batch_end - rev_window+1                    # remaining pseudonyms
            revoked.append((i, rev_window, k))
    return revoked

def count_original(revoked):        # original design (Cui et al.)
    inserts = deletes = 0
    for i, r_w, k in revoked:
        inserts += k
        deletes = inserts

    return (inserts, deletes)

def count_windows(revoked):     # proposed design
    inserts = discards = 0
    used_windows = []
    for i, r_w, k in revoked:
        inserts += k

        for j in range(r_w, r_w+k):
            if j not in used_windows:
                used_windows.append(j)
    
    discards = len(used_windows)
    return inserts, discards


if __name__ == "__main__":
    rev = generate_scenario(NUM_DEV, NUM_TIMEW, n, p, seed=1)
    print("revocation: ", len(rev))
    print("base filter (insert, delete): ", count_original(rev))
    print("new filter (insert, discards): ", count_windows(rev))