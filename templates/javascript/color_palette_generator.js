/**
 * Color Palette Generator
 * Generates harmonious color palettes with various color theory rules.
 * Author: Jay Singh (iamjaysingh)
 * Run: node index.js
 */

"use strict";

class Color {
    constructor(h, s, l) {
        this.h = h % 360;
        this.s = Math.max(0, Math.min(100, s));
        this.l = Math.max(0, Math.min(100, l));
    }

    toHSL() {
        return `hsl(${this.h}, ${this.s}%, ${this.l}%)`;
    }

    toRGB() {
        const s = this.s / 100;
        const l = this.l / 100;
        const c = (1 - Math.abs(2 * l - 1)) * s;
        const x = c * (1 - Math.abs(((this.h / 60) % 2) - 1));
        const m = l - c / 2;

        let r, g, b;
        if (this.h < 60) [r, g, b] = [c, x, 0];
        else if (this.h < 120) [r, g, b] = [x, c, 0];
        else if (this.h < 180) [r, g, b] = [0, c, x];
        else if (this.h < 240) [r, g, b] = [0, x, c];
        else if (this.h < 300) [r, g, b] = [x, 0, c];
        else[r, g, b] = [c, 0, x];

        return {
            r: Math.round((r + m) * 255),
            g: Math.round((g + m) * 255),
            b: Math.round((b + m) * 255),
        };
    }

    toHex() {
        const { r, g, b } = this.toRGB();
        return `#${r.toString(16).padStart(2, "0")}${g.toString(16).padStart(2, "0")}${b.toString(16).padStart(2, "0")}`;
    }

    display() {
        const hex = this.toHex();
        const { r, g, b } = this.toRGB();
        // ANSI color block
        const block = `\x1b[48;2;${r};${g};${b}m      \x1b[0m`;
        return `${block} ${hex.toUpperCase()}  HSL(${this.h}, ${this.s}%, ${this.l}%)`;
    }
}

// Palette generation strategies
function complementary(baseHue) {
    return [
        new Color(baseHue, 70, 50),
        new Color(baseHue, 70, 65),
        new Color(baseHue, 30, 90),
        new Color((baseHue + 180) % 360, 70, 50),
        new Color((baseHue + 180) % 360, 70, 65),
    ];
}

function analogous(baseHue) {
    return [
        new Color((baseHue - 30 + 360) % 360, 65, 50),
        new Color((baseHue - 15 + 360) % 360, 65, 60),
        new Color(baseHue, 70, 50),
        new Color((baseHue + 15) % 360, 65, 60),
        new Color((baseHue + 30) % 360, 65, 50),
    ];
}

function triadic(baseHue) {
    return [
        new Color(baseHue, 70, 45),
        new Color(baseHue, 50, 70),
        new Color((baseHue + 120) % 360, 70, 45),
        new Color((baseHue + 120) % 360, 50, 70),
        new Color((baseHue + 240) % 360, 70, 45),
    ];
}

function splitComplementary(baseHue) {
    return [
        new Color(baseHue, 70, 45),
        new Color(baseHue, 40, 75),
        new Color((baseHue + 150) % 360, 60, 50),
        new Color((baseHue + 180) % 360, 30, 85),
        new Color((baseHue + 210) % 360, 60, 50),
    ];
}

function monochromatic(baseHue) {
    return [
        new Color(baseHue, 80, 25),
        new Color(baseHue, 70, 40),
        new Color(baseHue, 65, 55),
        new Color(baseHue, 55, 70),
        new Color(baseHue, 40, 85),
    ];
}

function displayPalette(name, colors) {
    console.log(`\n  🎨 ${name}`);
    console.log("  " + "─".repeat(50));
    colors.forEach((color) => console.log("  " + color.display()));
}

// Main
function main() {
    console.log("=".repeat(55));
    console.log("  🎨 Color Palette Generator");
    console.log("=".repeat(55));

    const baseHue = Math.floor(Math.random() * 360);
    console.log(`\n  Base Hue: ${baseHue}°`);

    const palettes = {
        "Complementary": complementary(baseHue),
        "Analogous": analogous(baseHue),
        "Triadic": triadic(baseHue),
        "Split-Complementary": splitComplementary(baseHue),
        "Monochromatic": monochromatic(baseHue),
    };

    for (const [name, colors] of Object.entries(palettes)) {
        displayPalette(name, colors);
    }

    // Generate CSS variables
    console.log(`\n  📋 CSS Variables (Complementary):`);
    console.log("  " + "─".repeat(50));
    const compColors = palettes["Complementary"];
    compColors.forEach((color, i) => {
        console.log(`    --color-${i + 1}: ${color.toHex()};`);
    });

    console.log(`\n  ✨ Generated ${Object.keys(palettes).length} palettes!`);
}

main();
