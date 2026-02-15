/**
 * Mini Database
 * Generated on 2026-02-15 by Daily Auto Project Generator
 * Author: Jay Singh (iamjaysingh)
 */

"use strict";

class MiniApp {
    constructor(name) {
        this.name = name;
        this.data = new Map();
        this.createdAt = new Date().toISOString();
    }

    add(key, value) {
        this.data.set(key, value);
        console.log(`✅ Added: ${key} = ${value}`);
    }

    get(key) {
        return this.data.get(key) || null;
    }

    remove(key) {
        if (this.data.has(key)) {
            this.data.delete(key);
            console.log(`🗑️  Removed: ${key}`);
            return true;
        }
        console.log(`❌ Key '${key}' not found.`);
        return false;
    }

    list() {
        if (this.data.size === 0) {
            console.log("📭 No items yet.");
            return;
        }
        console.log("\n📋 Current items:");
        this.data.forEach((v, k) => {
            console.log(`   ${k}: ${v}`);
        });
    }

    stats() {
        return {
            name: this.name,
            itemCount: this.data.size,
            createdAt: this.createdAt,
        };
    }
}

// --- Main ---
const app = new MiniApp("Mini Database");
console.log("=".repeat(50));
console.log(`  Mini Database`);
console.log("=".repeat(50));

app.add("project", "Mini Database");
app.add("language", "JavaScript");
app.add("date", "2026-02-15");
app.list();
console.log("\n📊 Stats:", JSON.stringify(app.stats(), null, 2));
