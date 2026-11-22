import csv
from simulation import generate_scenario
from chain_sim import run_on_chain

NUM_DEV = 1000                      # number of devices
NUM_TIMEW = 100                     # number of time windows
BATCH_SIZES = [5, 10, 50]           # pseudonyms in one package (n)
REVOKE_PROBS = [0.01, 0.05, 0.10]   # share of revoked devices (p)
REPETITIONS = 3                     # runs with different seeds

with open("results.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["n", "p", "seed", "revoked", "original_tx", "original_gas", "window_tx", "window_gas"])
    for n in BATCH_SIZES:
        for p in REVOKE_PROBS:
            for seed in range(REPETITIONS):
                revoked = generate_scenario(NUM_DEV, NUM_TIMEW, n, p, seed)
                original_tx, original_gas, window_tx, window_gas = run_on_chain(revoked)

                writer.writerow([n, p, seed, len(revoked), original_tx, original_gas, window_tx, window_gas])
                f.flush()                   # save the row in instant

                print(f"n={n:3}  p={p:.2f}  seed={seed}:  "
                      f"original {original_tx:5} tx,  windows {window_tx:5} tx")

print("Done, results saved to results.csv")