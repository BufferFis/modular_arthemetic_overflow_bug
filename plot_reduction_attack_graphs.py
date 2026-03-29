#!/usr/bin/env python3
import csv
import math
from pathlib import Path

import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
MONT_FILE = ROOT / "montgomery_attack_results.csv"
BARR_FILE = ROOT / "barrett_attack_results.csv"
OUT_DIR = ROOT / "graphs"


def read_csv_rows(path):
    with path.open("r", newline="") as f:
        return list(csv.DictReader(f))


def to_float(row, key):
    return float(row[key])


def to_int(row, key):
    return int(float(row[key]))


def avg(values):
    return sum(values) / len(values) if values else 0.0


def clamp(v, lo, hi):
    return max(lo, min(v, hi))


def cia_scores(attack_rate_before, attack_rate_after, overhead_ratio):
    before_c = clamp(8.0 - 5.0 * attack_rate_before, 0.0, 10.0)
    before_i = clamp(10.0 - 9.0 * attack_rate_before, 0.0, 10.0)
    before_a = clamp(9.0 - 1.0 * overhead_ratio, 0.0, 10.0)

    after_c = clamp(8.8 - 1.5 * attack_rate_after, 0.0, 10.0)
    after_i = clamp(10.0 - 9.0 * attack_rate_after, 0.0, 10.0)
    after_a = clamp(8.6 - 1.5 * overhead_ratio, 0.0, 10.0)

    return {
        "before": {"C": before_c, "I": before_i, "A": before_a},
        "after": {"C": after_c, "I": after_i, "A": after_a},
    }


def grouped(values, keys):
    grouped_data = {}
    for row in values:
        group_key = tuple(row[k] for k in keys)
        grouped_data.setdefault(group_key, []).append(row)
    return grouped_data


def plot_attack_success_rate(method_rows):
    methods = []
    before = []
    after = []

    for method, rows in method_rows.items():
        methods.append(method)
        before.append(100.0 * avg([to_int(r, "attack_success_before") for r in rows]))
        after.append(100.0 * avg([to_int(r, "attack_success_after") for r in rows]))

    x = range(len(methods))
    width = 0.35

    plt.figure(figsize=(8, 5))
    plt.bar([i - width / 2 for i in x], before, width=width, label="Before Prevention")
    plt.bar([i + width / 2 for i in x], after, width=width, label="After Prevention")
    plt.xticks(list(x), [m.title() for m in methods])
    plt.ylabel("Attack Success Rate (%)")
    plt.title("Graph 1 - Attack Success Rate Before vs After Prevention")
    plt.ylim(0, 100)
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUT_DIR / "graph1_attack_success_rate.png", dpi=160)
    plt.close()


def plot_performance_vs_input_size(rows):
    grouped_data = grouped(rows, ["method", "input_size_bits"])

    method_points = {}
    for (method, input_bits), rows_for_point in grouped_data.items():
        x = int(input_bits)
        t_before = avg([to_float(r, "time_ns_before") for r in rows_for_point])
        t_after = avg([to_float(r, "time_ns_after") for r in rows_for_point])
        method_points.setdefault(method, {"before": [], "after": []})
        method_points[method]["before"].append((x, t_before))
        method_points[method]["after"].append((x, t_after))

    plt.figure(figsize=(9, 5))
    for method, data in method_points.items():
        b = sorted(data["before"])
        a = sorted(data["after"])
        plt.plot([p[0] for p in b], [p[1] for p in b], marker="o", label=f"{method.title()} before")
        plt.plot([p[0] for p in a], [p[1] for p in a], marker="s", linestyle="--", label=f"{method.title()} after")

    plt.xlabel("Input Size (bits)")
    plt.ylabel("Time per Operation (ns)")
    plt.title("Graph 2 - Performance: Time vs Input Size")
    plt.legend()
    plt.grid(alpha=0.25)
    plt.tight_layout()
    plt.savefig(OUT_DIR / "graph2_performance_time_vs_input_size.png", dpi=160)
    plt.close()


def plot_cia_security_scores(method_rows):
    methods = []
    before_cia = []
    after_cia = []

    for method, rows in method_rows.items():
        methods.append(method)

        attack_rate_before = avg([to_int(r, "attack_success_before") for r in rows])
        attack_rate_after = avg([to_int(r, "attack_success_after") for r in rows])

        avg_before = avg([to_float(r, "time_ns_before") for r in rows])
        avg_after = avg([to_float(r, "time_ns_after") for r in rows])

        overhead_ratio = (avg_after - avg_before) / avg_before if avg_before > 0 else 0.0
        scores = cia_scores(attack_rate_before, attack_rate_after, overhead_ratio)

        before_cia.append(scores["before"])
        after_cia.append(scores["after"])

    categories = ["C", "I", "A"]

    plt.figure(figsize=(10, 5))
    bar_width = 0.18

    for i, method in enumerate(methods):
        for j, cat in enumerate(categories):
            x_before = i * 1.0 + (j - 1.5) * bar_width
            x_after = i * 1.0 + (j - 1.5) * bar_width + bar_width * 0.5

            plt.bar(
                x_before,
                before_cia[i][cat],
                width=bar_width,
                color=["#4C78A8", "#F58518", "#54A24B"][j],
                alpha=0.55,
            )
            plt.bar(
                x_after,
                after_cia[i][cat],
                width=bar_width,
                color=["#4C78A8", "#F58518", "#54A24B"][j],
                alpha=0.95,
                hatch="//",
            )

    plt.xticks([i for i in range(len(methods))], [m.title() for m in methods])
    plt.ylabel("CIA Score (0-10)")
    plt.ylim(0, 10)
    plt.title("Graph 3 - CIA Security Score Comparison")

    legend_labels = [
        "Confidentiality",
        "Integrity",
        "Availability",
        "After Prevention (hatched)",
    ]
    legend_handles = [
        plt.Rectangle((0, 0), 1, 1, color="#4C78A8", alpha=0.8),
        plt.Rectangle((0, 0), 1, 1, color="#F58518", alpha=0.8),
        plt.Rectangle((0, 0), 1, 1, color="#54A24B", alpha=0.8),
        plt.Rectangle((0, 0), 1, 1, color="#777777", hatch="//", fill=False),
    ]
    plt.legend(legend_handles, legend_labels, loc="lower right")

    plt.tight_layout()
    plt.savefig(OUT_DIR / "graph3_cia_security_score_comparison.png", dpi=160)
    plt.close()


def plot_latency_overhead(rows):
    labels = [f"{r['method'][0].upper()}-{r['test_case']}" for r in rows]
    overheads = [to_float(r, "latency_overhead_ns") for r in rows]

    plt.figure(figsize=(12, 5))
    plt.bar(range(len(labels)), overheads, color="#7A5195")
    plt.axhline(0, color="black", linewidth=0.8)
    plt.xticks(range(len(labels)), labels, rotation=45, ha="right")
    plt.ylabel("Safe - Vulnerable Latency (ns/op)")
    plt.title("Graph 4 - Latency Overhead Per Test Case")
    plt.tight_layout()
    plt.savefig(OUT_DIR / "graph4_latency_overhead_per_testcase.png", dpi=160)
    plt.close()


def write_cia_table(method_rows):
    out_csv = OUT_DIR / "cia_scores.csv"
    with out_csv.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["method", "phase", "confidentiality", "integrity", "availability"])

        for method, rows in method_rows.items():
            attack_rate_before = avg([to_int(r, "attack_success_before") for r in rows])
            attack_rate_after = avg([to_int(r, "attack_success_after") for r in rows])
            avg_before = avg([to_float(r, "time_ns_before") for r in rows])
            avg_after = avg([to_float(r, "time_ns_after") for r in rows])
            overhead_ratio = (avg_after - avg_before) / avg_before if avg_before > 0 else 0.0

            scores = cia_scores(attack_rate_before, attack_rate_after, overhead_ratio)
            writer.writerow([method, "before", scores["before"]["C"], scores["before"]["I"], scores["before"]["A"]])
            writer.writerow([method, "after", scores["after"]["C"], scores["after"]["I"], scores["after"]["A"]])


def main():
    if not MONT_FILE.exists() or not BARR_FILE.exists():
        raise SystemExit("Run both C demos first to generate montgomery_attack_results.csv and barrett_attack_results.csv")

    OUT_DIR.mkdir(exist_ok=True)

    mont = read_csv_rows(MONT_FILE)
    barr = read_csv_rows(BARR_FILE)
    all_rows = mont + barr
    method_rows = {
        "montgomery": mont,
        "barrett": barr,
    }

    plot_attack_success_rate(method_rows)
    plot_performance_vs_input_size(all_rows)
    plot_cia_security_scores(method_rows)
    plot_latency_overhead(all_rows)
    write_cia_table(method_rows)

    print("Generated graphs in:", OUT_DIR)
    print("- graph1_attack_success_rate.png")
    print("- graph2_performance_time_vs_input_size.png")
    print("- graph3_cia_security_score_comparison.png")
    print("- graph4_latency_overhead_per_testcase.png")
    print("- cia_scores.csv")


if __name__ == "__main__":
    main()
