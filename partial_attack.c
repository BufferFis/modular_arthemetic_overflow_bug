#include <stdio.h>
#include <stdint.h>

int main() {
    // We use 8-bit integers (max value 255) to easily demonstrate the overflow
    uint8_t user_balance = 100;    
    uint8_t item_price = 10;       
    
    // Attacker requests an impossibly large amount of items
    uint8_t num_items_to_buy = 26; 
    uint8_t total_cost;

    printf("--- Vulnerable Purchasing System ---\n");
    printf("Starting balance: %d coins\n", user_balance);
    printf("Item price: %d coins\n\n", item_price);
    
    // VULNERABILITY: The multiplication overflows the 8-bit limit (255)
    total_cost = num_items_to_buy * item_price; 
    
    printf("Attacker attempts to buy %d items...\n", num_items_to_buy);
    printf("System calculates total cost: %d * %d\n", num_items_to_buy, item_price);
    printf("Internal memory stores cost as: %d coins\n", total_cost); // This will print 4!
    
    // The security check evaluates based on the overflowed, wrapped-around value
    if (total_cost <= user_balance) {
        user_balance = user_balance - total_cost;
        
        printf("\n[!] TRANSACTION APPROVED [!]\n");
        printf("Items successfully purchased: %d\n", num_items_to_buy);
        printf("Remaining balance: %d coins\n", user_balance);
        printf("ATTACK SUCCESS: The attacker bought 26 items (worth 260) for only 4 coins!\n");
    } else {
        printf("\n[ERROR] Insufficient funds.\n");
    }

    return 0;
}