# Modular Arithmetic Overflow & Integer Attacks Lab

An interactive, visual educational lab demonstrating classic and cryptographic integer overflow vulnerabilities, underflows, and modular arithmetic truncation flaws. This project includes a fully interactive graphical user interface (GUI) and generates advanced web-based analytics to visualize memory boundaries and their exploitation.

## 🚀 What Is It?
This project simulates real-world software security failures caused by inadequate memory handling and flawed arithmetic logic. It allows users to actively execute "Attacks" (triggering exploits) and then apply "Prevention" (running patched algorithms) across various languages (C, Java, Python). 

The lab calculates a derived **CIA Triad (Confidentiality, Integrity, Availability) Security Score** based on attack success rates and latency overheads.

## 🛡️ Vulnerabilities Explored

1. **C `uint8` Overflow (The Shopping Cart Bypass):** Exploiting 8-bit unsigned integer wrap-around to bypass financial constraints.
2. **Java `int32` Overflow (Negative Cost):** Passing the 2.14 billion 32-bit signed integer boundary to flip bits and generate negative transaction totals.
3. **Java `BigInteger` Improper Migration:** Demonstrating how safe massive variables are instantly crushed back into vulnerabilities using improper type-casting (`.intValue()`).
4. **Nuclear Gandhi (8-bit Underflow):** Dropping an unsigned integer below 0 forces a reverse wrap to maximum capacities (Demonstrating logic behavioral breaks).
5. **Modular Reduction (Montgomery/Barrett):** Specialized cryptographic vulnerabilities where calculation speed optimization (approximation/truncation loops) causes residues to fail modulo congruence checks.

## ⚙️ Prerequisites

To run the interactive UI and backend tests, ensure you have the following installed on your system:
- **Python 3.x** (with standard `tkinter` library)
- **GCC** (for compiling C examples)
- **Java JDK** (for compiling Java BigInteger examples)
- A modern web browser (for viewing analytical charts)

## 🎮 How to Run

You can launch the entire interactive experience using the provided shell script:

```bash
# Provide executable permissions if necessary
chmod +x run.sh

# Run the project (Compiles C/Java and launches Python UI)
./run.sh
```

Alternatively, you can skip compilation and directly launch the Graphical Interface:
```bash
python3 main_ui.py
```

## 🖥️ Using the Interface

1. **Select Scenario:** Choose one of the 5 vulnerabilities from the dropdown.
2. **1. Generate 10 Test Cases:** Populates random but targeted boundary variables for the attack vector.
3. **2. Run Attack (Vulnerable):** Executes the unpatched logic, intentionally demonstrating how the exploit bypasses application rules.
4. **3. Apply Prevention (Secure):** Executes the corrected memory logic (using `BigInteger`, `size_t`, or explicit boundary checks) to successfully block the exploits.
5. **4. Show Advanced Graphs:** Dynamically generates `advanced_metrics_report.html`, opens it in your browser, and presents beautiful Chart.js data visualizing the data arrays, boundary limits, and resulting CIA Security assessment.

## 📖 Deep Documentation

For a highly specific mathematical breakdown of the cryptographic algorithms (Montgomery and Barrett Reductions) and their exact algebraic failure states, please read `scenario4.md` and `reduction_attack_demo.md` included in this repository.
