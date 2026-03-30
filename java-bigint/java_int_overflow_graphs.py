import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv("results.csv")

# Convert booleans to int
df["success"] = df["success"].astype(int)
df["overflow_detected"] = df["overflow_detected"].astype(int)

# -----------------------------------
# Graph 1 — Attack Success Rate
# -----------------------------------
success_rate = df.groupby(["input_size", "method"])["success"].mean().unstack()

plt.figure()
for method in success_rate.columns:
    plt.plot(success_rate.index, success_rate[method], marker='o', label=method)

plt.title("Attack Success Rate vs Input Size")
plt.xlabel("Input Size")
plt.ylabel("Success Rate")
plt.legend()
plt.grid()
plt.savefig("graph1_success_rate.png")

# -----------------------------------
# Graph 2 — Performance
# -----------------------------------
time_avg = df.groupby(["input_size", "method"])["time_ns"].mean().unstack()

plt.figure()
for method in time_avg.columns:
    plt.plot(time_avg.index, time_avg[method], marker='o', label=method)

plt.title("Performance: Time vs Input Size")
plt.xlabel("Input Size")
plt.ylabel("Time (ns)")
plt.legend()
plt.grid()
plt.savefig("graph2_performance.png")

# -----------------------------------
# Graph 3 — CIA Security Score
# -----------------------------------
grouped = df.groupby("method").agg({
    "success": "mean",
    "overflow_detected": "mean"
})

# CIA scoring
grouped["confidentiality"] = 1.0
grouped["integrity"] = 1 - grouped["success"]
grouped["availability"] = 1 - grouped["overflow_detected"]

grouped["CIA_score"] = (
    grouped["confidentiality"] +
    grouped["integrity"] +
    grouped["availability"]
) / 3

plt.figure()
plt.bar(grouped.index, grouped["CIA_score"])
plt.title("CIA Security Score Comparison")
plt.ylabel("Score (0–1)")
plt.xticks(rotation=30)
plt.savefig("graph3_cia_score.png")

# -----------------------------------
# Graph 4 — Latency Overhead
# -----------------------------------
baseline = time_avg["attack_int"]

plt.figure()
for method in time_avg.columns:
    if method != "attack_int":
        overhead = time_avg[method] - baseline
        plt.plot(time_avg.index, overhead, marker='o', label=method)

plt.title("Latency Overhead vs Input Size")
plt.xlabel("Input Size")
plt.ylabel("Overhead (ns)")
plt.legend()
plt.grid()
plt.savefig("graph4_latency_overhead.png")

plt.show()
