# Project Guidelines

## Code Style
- Use C99-compatible code and keep examples minimal, readable, and educational.
- Prefer fixed-width integer types from `stdint.h` (for example `uint8_t`, `uint16_t`) to make overflow behavior explicit.
- When writing secure variants, use wider intermediate types for arithmetic and cast before multiplication.
- Keep stdout messages clear and deterministic so behavior can be verified by comparing output text.

## Architecture
- This repository is an educational security lab about modular arithmetic overflow.
- `vulnerable_cart.c` and `partial_attack.c` intentionally demonstrate exploitable 8-bit overflow behavior.
- `safe_wallet.c` demonstrates the patched approach using safe type promotion.
- `example_output.md` contains expected output for the vulnerable attack scenario.
- Files are standalone programs; there are no shared headers or libraries.

## Build And Test
- Compile and run with direct `gcc` commands (no build system):
  - `gcc -std=c99 -Wall -Wextra -o vulnerable_cart vulnerable_cart.c && ./vulnerable_cart`
  - `gcc -std=c99 -Wall -Wextra -o partial_attack partial_attack.c && ./partial_attack`
  - `gcc -std=c99 -Wall -Wextra -o safe_wallet safe_wallet.c && ./safe_wallet`
- When changing vulnerable examples, preserve the intentional bug unless the task explicitly asks to patch it.
- When changing patched examples, ensure the arithmetic result does not wrap silently.

## Conventions
- Treat this repository as demonstration code, not production infrastructure.
- Document whether a file is intentionally vulnerable or intentionally patched.
- If adding new demos, include one vulnerable case and one safe counterpart where practical.
- Keep numeric values small and explicit so overflow math is easy to reason about.
