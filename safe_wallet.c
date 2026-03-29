#include <stdio.h>
#include <stdint.h>

int main() {

    uint8_t wallet_balance = 150;
    uint8_t token_price = 12;
    uint8_t tokens_requested = 25;

    uint16_t total_cost;   // Larger type prevents overflow

    printf("===== SecureChain Wallet v2.0 (Patched) =====\n");

    total_cost = (uint16_t)tokens_requested * token_price;

    if (total_cost <= wallet_balance) {
        wallet_balance -= total_cost;
        printf("Transaction Approved\n");
    } else {
        printf("Transaction Denied: Insufficient balance\n");
    }

    printf("Computed Cost: %u\n", total_cost);

    return 0;
}
