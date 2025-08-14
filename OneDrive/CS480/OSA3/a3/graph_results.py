import pandas as pd
import matplotlib.pyplot as plt

# Load the performance data
df = pd.read_csv("performance.csv")

# Calculate interval for x-axis ticks (every Nth point)
tick_interval = 10  # change to 5 or 20 if needed
xticks = df["Step"][::tick_interval]

# Plot 1: Avg Fragments Over Time
plt.figure(figsize=(10, 5))
plt.plot(df["Step"], df["FF_Fragments"], label="First Fit", linestyle="--", marker='o')
plt.plot(df["Step"], df["BF_Fragments"], label="Best Fit", linestyle="-", marker='x')
plt.title("Average External Fragments Over Time")
plt.xlabel("Requests")
plt.ylabel("Avg Fragments")
plt.legend()
plt.grid(True)
plt.xticks(xticks)
plt.tight_layout()
plt.savefig("fragments_over_time.png")
plt.show()

# Plot 2: Avg Nodes Traversed Over Time
plt.figure(figsize=(10, 5))
plt.plot(df["Step"], df["FF_Nodes"], label="First Fit", linestyle="--", marker='o')
plt.plot(df["Step"], df["BF_Nodes"], label="Best Fit", linestyle="-", marker='x')
plt.title("Average Nodes Traversed Over Time")
plt.xlabel("Requests")
plt.ylabel("Avg Nodes")
plt.legend()
plt.grid(True)
plt.xticks(xticks)
plt.tight_layout()
plt.savefig("nodes_over_time.png")
plt.show()

# Plot 3: Denial Rate Over Time
plt.figure(figsize=(10, 5))
plt.plot(df["Step"], df["FF_Denial"], label="First Fit", linestyle="--", marker='o')
plt.plot(df["Step"], df["BF_Denial"], label="Best Fit", linestyle="-", marker='x')
plt.title("Denial Rate (%) Over Time")
plt.xlabel("Requests")
plt.ylabel("Denial Rate (%)")
plt.legend()
plt.grid(True)
plt.xticks(xticks)
plt.tight_layout()
plt.savefig("denials_over_time.png")
plt.show()
