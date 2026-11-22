import csv
import matplotlib.pyplot as plt

# load results and sum them for each (n, p)
totals = {}
with open("results.csv") as f:
    for row in csv.DictReader(f):
        key = (int(row["n"]), float(row["p"]))
        if key not in totals:
            totals[key] = [0, 0, 0, 0]
        totals[key][0] += int(row["original_tx"])
        totals[key][1] += int(row["original_gas"])
        totals[key][2] += int(row["window_tx"])
        totals[key][3] += int(row["window_gas"])

batch_sizes = sorted({n for n, p in totals})
probs = sorted({p for n, p in totals})

# print a table with savings
print(f"{'n':>4} {'p':>5} {'saved tx %':>11} {'saved gas %':>12}")
for n in batch_sizes:
    for p in probs:
        original_tx, original_gas, window_tx, window_gas = totals[(n, p)]
        print(f"{n:>4} {p:>5.2f} {(original_tx - window_tx) / original_tx * 100:>11.1f} "
              f"{(original_gas - window_gas) / original_gas * 100:>12.1f}")

# plot: savings vs. share of revoked devices, one line per batch size
fig, (ax_tx, ax_gas) = plt.subplots(1, 2, figsize=(7, 2.8), sharey=True)
markers = ["o", "s", "^"]

for n, marker in zip(batch_sizes, markers):
    tx_saved, gas_saved = [], []
    for p in probs:
        original_tx, original_gas, window_tx, window_gas = totals[(n, p)]
        tx_saved.append((original_tx - window_tx) / original_tx * 100)
        gas_saved.append((original_gas - window_gas) / original_gas * 100)
    x = [p * 100 for p in probs]
    ax_tx.plot(x, tx_saved, marker=marker, label=f"n = {n}")
    ax_gas.plot(x, gas_saved, marker=marker, label=f"n = {n}")

ax_tx.set_title("Transactions")
ax_gas.set_title("Gas")
for ax in (ax_tx, ax_gas):
    ax.set_xlabel("Revoked devices [%]")
    ax.set_xticks([p * 100 for p in probs])
    ax.grid(alpha=0.3)
ax_tx.set_ylabel("Savings [%]")
ax_gas.legend()

plt.tight_layout()
plt.savefig("results.png", dpi=300)
print("Graph saved to results.png")