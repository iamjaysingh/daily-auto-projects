/*
 * Stack Array
 * Generated on 2026-02-15 by Daily Auto Project Generator
 * Author: Jay Singh (iamjaysingh)
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_ITEMS 100
#define MAX_LEN 256

typedef struct {
    char key[MAX_LEN];
    char value[MAX_LEN];
} Item;

typedef struct {
    Item items[MAX_ITEMS];
    int count;
    char name[MAX_LEN];
} DataStore;

void init_store(DataStore *store, const char *name) {
    store->count = 0;
    strncpy(store->name, name, MAX_LEN - 1);
    store->name[MAX_LEN - 1] = '\0';
}

int add_item(DataStore *store, const char *key, const char *value) {
    if (store->count >= MAX_ITEMS) {
        printf("❌ Store is full!\n");
        return -1;
    }
    strncpy(store->items[store->count].key, key, MAX_LEN - 1);
    strncpy(store->items[store->count].value, value, MAX_LEN - 1);
    store->count++;
    printf("✅ Added: %s = %s\n", key, value);
    return 0;
}

void list_items(const DataStore *store) {
    if (store->count == 0) {
        printf("📭 No items yet.\n");
        return;
    }
    printf("\n📋 Current items (%d):\n", store->count);
    for (int i = 0; i < store->count; i++) {
        printf("   %s: %s\n", store->items[i].key, store->items[i].value);
    }
}

int main() {
    DataStore store;
    init_store(&store, "Stack Array");

    printf("==================================================\n");
    printf("  Stack Array\n");
    printf("==================================================\n");

    add_item(&store, "project", "Stack Array");
    add_item(&store, "language", "C");
    add_item(&store, "date", "2026-02-15");
    list_items(&store);

    printf("\n👋 Done!\n");
    return 0;
}
