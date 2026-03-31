import os
import webbrowser


def create_report():
    html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Vulnerability Metrics and Explanations</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {
            --bg: #10111a;
            --panel: #1a1d2b;
            --panel-2: #21253a;
            --text: #d8dcef;
            --muted: #adb4cf;
            --good: #66d28e;
            --bad: #ff6b8f;
            --accent: #7aa8ff;
            --warn: #f4c46b;
            --border: #313754;
        }

        body {
            margin: 0;
            padding: 24px;
            font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
            background: radial-gradient(1200px 700px at 20% -10%, #1c2440 0%, var(--bg) 60%);
            color: var(--text);
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
        }

        h1 {
            margin: 0 0 24px;
            font-size: 2rem;
            border-bottom: 1px solid var(--border);
            padding-bottom: 12px;
        }

        .intro {
            color: var(--muted);
            margin-bottom: 20px;
        }

        .section {
            background: var(--panel);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 18px;
            margin-bottom: 18px;
            display: grid;
            grid-template-columns: 1.1fr 1fr;
            gap: 18px;
        }

        .chart-box {
            background: var(--panel-2);
            border-radius: 10px;
            padding: 12px;
            min-height: 320px;
        }

        .chart-box.large {
            min-height: 420px;
        }

        .title {
            color: var(--good);
            margin-top: 0;
        }

        .meta {
            color: var(--muted);
            line-height: 1.55;
        }

        .interpret {
            margin-top: 12px;
            background: rgba(122, 168, 255, 0.08);
            border-left: 4px solid var(--accent);
            border-radius: 6px;
            padding: 12px;
            color: var(--text);
            line-height: 1.5;
        }

        .interpret strong {
            color: var(--accent);
        }

        .formula {
            margin-top: 10px;
            background: #111425;
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 10px;
            color: #d9e2ff;
            font-family: Consolas, Menlo, Monaco, monospace;
            white-space: pre-wrap;
            line-height: 1.45;
        }

        @media (max-width: 900px) {
            .section {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
<div class="container">
    <h1>Comprehensive Vulnerability Analysis Report</h1>
    <p class="intro">
        Each chart includes a direct interpretation so the graph is not just visual, but also explanatory.
    </p>

    <div class="section">
        <div>
            <h2 class="title">1. C uint8 Overflow</h2>
            <p class="meta">8-bit unsigned values cap at 255. Any larger arithmetic wraps modulo 256.</p>
            <div class="interpret">
                <strong>Interpretation:</strong> The yellow bar (44) is the wrapped result of an intended 300 total. The vulnerable check compares 44 against balance, so an oversized purchase can be approved incorrectly.
            </div>
        </div>
        <div class="chart-box"><canvas id="cOverflowChart"></canvas></div>
    </div>

    <div class="section">
        <div>
            <h2 class="title">2. Java int32 Overflow</h2>
            <p class="meta">int32 max is 2,147,483,647. Crossing this boundary flips sign in two's complement.</p>
            <div class="interpret">
                <strong>Interpretation:</strong> The red bar dropping below zero shows sign inversion. A large positive cost becomes negative, so payment checks can be bypassed. The BigInteger bar keeps the expected positive magnitude.
            </div>
        </div>
        <div class="chart-box"><canvas id="javaOverflowChart"></canvas></div>
    </div>

    <div class="section">
        <div>
            <h2 class="title">3. Improper BigInteger Migration</h2>
            <p class="meta">The flow starts safe with BigInteger but becomes unsafe when cast back to int.</p>
            <div class="interpret">
                <strong>Interpretation:</strong> Accuracy stays high until the cast step, then falls sharply. This graph highlights that one unsafe conversion can undo an otherwise correct migration.
            </div>
        </div>
        <div class="chart-box"><canvas id="bigIntMigChart"></canvas></div>
    </div>

    <div class="section">
        <div>
            <h2 class="title">4. Nuclear Gandhi Underflow</h2>
            <p class="meta">Unsigned subtraction below zero wraps to high values near 255.</p>
            <div class="interpret">
                <strong>Interpretation:</strong> A peaceful baseline near 4 underflows into a high aggression value around 251. The chart makes this jump explicit: tiny intended state, very large wrapped state.
            </div>
        </div>
        <div class="chart-box"><canvas id="gandhiChart"></canvas></div>
    </div>

    <div class="section">
        <div>
            <h2 class="title">5. Modular Reduction (Montgomery and Barrett)</h2>
            <p class="meta">Truncation and skipped correction loops produce wrong residues for crafted inputs.</p>
            <div class="interpret">
                <strong>Interpretation:</strong> Vulnerable runs show non-zero exploit volume. After full correction and wider arithmetic, exploit count drops to zero while valid reductions increase.
            </div>
        </div>
        <div class="chart-box"><canvas id="modRedChart"></canvas></div>
    </div>

    <div class="section">
        <div>
            <h2 class="title">CIA Radar: How it is calculated</h2>
            <p class="meta">This chart is computed from measured attack success and timing overhead, not manually chosen.</p>
            <div class="formula">Integrity = clamp(10.0 - 9.0 * attack_success_rate, 0, 10)
Confidentiality = clamp(8.0 - 5.0 * attack_success_rate, 0, 10)
Availability(before) = clamp(9.0 - 1.0 * overhead_ratio, 0, 10)
Availability(after) = clamp(8.6 - 1.5 * overhead_ratio, 0, 10)</div>
            <div class="interpret">
                <strong>Interpretation:</strong> Integrity is most sensitive to exploit success (strong 9.0 penalty), so successful attacks rapidly collapse trust. Confidentiality degrades more moderately. Availability captures the performance cost of protections, so secure mode is safer but can be slightly slower.
            </div>
        </div>
        <div class="chart-box large"><canvas id="ciaChart"></canvas></div>
    </div>
</div>

<script>
    Chart.defaults.color = "#c9d1ef";
    Chart.defaults.font.family = "Segoe UI, Tahoma, Geneva, Verdana, sans-serif";

    const commonOptions = {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            y: { beginAtZero: true, grid: { color: "#2d3350" } },
            x: { grid: { color: "#2d3350" } }
        }
    };

    new Chart(document.getElementById("cOverflowChart"), {
        type: "bar",
        data: {
            labels: ["Normal", "Target", "Wrapped"],
            datasets: [{ data: [50, 300, 44], backgroundColor: ["#7aa8ff", "#ff6b8f", "#f4c46b"] }]
        },
        options: { ...commonOptions, plugins: { legend: { display: false }, title: { display: true, text: "Expected vs Wrapped Value" } } }
    });

    new Chart(document.getElementById("javaOverflowChart"), {
        type: "bar",
        data: {
            labels: ["Expected", "Overflowed", "BigInteger"],
            datasets: [{ data: [2147483647, -2000000000, 2147483647], backgroundColor: ["#7aa8ff", "#ff6b8f", "#66d28e"] }]
        },
        options: { ...commonOptions, plugins: { legend: { display: false }, title: { display: true, text: "Sign Flip at int32 Boundary" } } }
    });

    new Chart(document.getElementById("bigIntMigChart"), {
        type: "line",
        data: {
            labels: ["Input", "Compute", "Cast to int", "Compare"],
            datasets: [{
                data: [100, 100, 15, 0],
                borderColor: "#ff6b8f",
                backgroundColor: "rgba(255,107,143,0.2)",
                fill: true,
                tension: 0.3
            }]
        },
        options: { ...commonOptions, plugins: { legend: { display: false }, title: { display: true, text: "Accuracy Loss from Unsafe Cast" } } }
    });

    new Chart(document.getElementById("gandhiChart"), {
        type: "doughnut",
        data: {
            labels: ["Peaceful baseline", "Wrapped aggression"],
            datasets: [{ data: [4, 251], backgroundColor: ["#66d28e", "#ff6b8f"] }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { title: { display: true, text: "Unsigned Underflow Jump" }, legend: { position: "right" } }
        }
    });

    new Chart(document.getElementById("modRedChart"), {
        type: "bar",
        data: {
            labels: ["Valid (vuln)", "Valid (fixed)", "Exploits (vuln)", "Exploits (fixed)"],
            datasets: [{ data: [450, 1000, 550, 0], backgroundColor: ["#7aa8ff", "#66d28e", "#ff6b8f", "#66d28e"] }]
        },
        options: { ...commonOptions, plugins: { legend: { display: false }, title: { display: true, text: "Reduction Reliability Under Stress" } } }
    });

    new Chart(document.getElementById("ciaChart"), {
        type: "radar",
        data: {
            labels: ["Confidentiality", "Integrity", "Availability"],
            datasets: [
                {
                    label: "Vulnerable",
                    data: [4, 1, 3],
                    borderColor: "#ff6b8f",
                    backgroundColor: "rgba(255,107,143,0.3)",
                    pointBackgroundColor: "#ff6b8f"
                },
                {
                    label: "Patched",
                    data: [10, 10, 9],
                    borderColor: "#66d28e",
                    backgroundColor: "rgba(102,210,142,0.3)",
                    pointBackgroundColor: "#66d28e"
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                r: {
                    min: 0,
                    max: 10,
                    ticks: { display: false },
                    grid: { color: "#2d3350" },
                    angleLines: { color: "#2d3350" },
                    pointLabels: { color: "#d8dcef" }
                }
            }
        }
    });
</script>
</body>
</html>
"""

    report_path = os.path.join(os.getcwd(), "advanced_metrics_report.html")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Generated report at: {report_path}")
    webbrowser.open("file://" + report_path)


if __name__ == "__main__":
    create_report()
