#!/usr/bin/env python3
"""
Daily Auto Project Generator
Generates a unique coding project every day and pushes to GitHub.
Uses Google Gemini AI for intelligent code generation with template fallback.

Author: Jay Singh (iamjaysingh)
"""

import os
import sys
import json
import random
import datetime
import subprocess
import hashlib
import argparse
import traceback

# ─── Configuration ────────────────────────────────────────────────────────────

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(SCRIPT_DIR, "config.json")
PROJECTS_DIR = os.path.join(SCRIPT_DIR, "projects")
TEMPLATES_DIR = os.path.join(SCRIPT_DIR, "templates")
STREAK_FILE = os.path.join(SCRIPT_DIR, "streak.json")


def load_config():
    """Load configuration from config.json"""
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)


def get_today():
    """Get today's date string"""
    return datetime.date.today().isoformat()


def get_streak_info():
    """Load and return streak information"""
    if os.path.exists(STREAK_FILE):
        with open(STREAK_FILE, "r") as f:
            return json.load(f)
    return {"total_projects": 0, "current_streak": 0, "last_date": None, "languages_used": {}}


def update_streak(language, project_type):
    """Update streak information after successful project creation"""
    streak = get_streak_info()
    today = get_today()
    yesterday = (datetime.date.today() - datetime.timedelta(days=1)).isoformat()

    streak["total_projects"] += 1

    if streak["last_date"] == yesterday:
        streak["current_streak"] += 1
    elif streak["last_date"] != today:
        streak["current_streak"] = 1

    streak["last_date"] = today
    streak["languages_used"][language] = streak["languages_used"].get(language, 0) + 1

    with open(STREAK_FILE, "w") as f:
        json.dump(streak, f, indent=2)

    return streak


# ─── AI Code Generation (Gemini) ─────────────────────────────────────────────

def generate_with_gemini(language, project_type):
    """Generate project code using Google Gemini AI"""
    api_key = os.environ.get("GEMINI_API_KEY", "")
    if not api_key:
        print("⚠️  No GEMINI_API_KEY found, falling back to templates...")
        return None

    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.0-flash")

        # Language-specific file info
        file_info = {
            "python": {"ext": ".py", "main": "main.py"},
            "javascript": {"ext": ".js", "main": "index.js"},
            "java": {"ext": ".java", "main": "Main.java"},
            "c": {"ext": ".c", "main": "main.c"},
            "go": {"ext": ".go", "main": "main.go"},
        }

        info = file_info.get(language, {"ext": ".txt", "main": "main.txt"})

        prompt = f"""Generate a complete, working {language} mini-project: {project_type}.

Requirements:
- Write ONLY the code, no explanations or markdown formatting
- The code must be complete, compilable/runnable, and well-commented
- Include meaningful logic (not just hello world)
- Add proper error handling
- Make it educational and demonstrate good coding practices
- The code should be between 40-120 lines
- Include a header comment with project name and brief description

The project type is: {project_type}
Language: {language}
"""

        response = model.generate_content(prompt)
        code = response.text.strip()

        # Clean up markdown code fences if present
        if code.startswith("```"):
            lines = code.split("\n")
            # Remove first and last lines (```language and ```)
            lines = lines[1:]
            if lines and lines[-1].strip() == "```":
                lines = lines[:-1]
            code = "\n".join(lines)

        if len(code) < 20:
            print("⚠️  AI returned too little code, falling back to templates...")
            return None

        return {info["main"]: code}

    except Exception as e:
        print(f"⚠️  Gemini AI error: {e}")
        print("   Falling back to templates...")
        return None


# ─── Template-Based Generation ────────────────────────────────────────────────

def load_template(language, project_type):
    """Load a project template from the templates directory"""
    template_dir = os.path.join(TEMPLATES_DIR, language)
    # Convert project_type to filename: "cli-calculator" -> "cli_calculator"
    template_name = project_type.replace("-", "_")

    # Try exact match first
    for ext in [".py", ".js", ".java", ".c", ".go", ".txt"]:
        path = os.path.join(template_dir, template_name + ext)
        if os.path.exists(path):
            with open(path, "r") as f:
                content = f.read()
            # Determine the output filename
            file_map = {
                ".py": "main.py",
                ".js": "index.js",
                ".java": "Main.java",
                ".c": "main.c",
                ".go": "main.go",
            }
            return {file_map.get(ext, "main.txt"): content}

    # If no template found, use a generic one
    return generate_generic_template(language, project_type)


def generate_generic_template(language, project_type):
    """Generate a generic but meaningful template"""
    title = project_type.replace("-", " ").title()
    date = get_today()

    templates = {
        "python": {
            "main.py": f'''#!/usr/bin/env python3
"""
{title}
Generated on {date} by Daily Auto Project Generator
Author: Jay Singh (iamjaysingh)
"""

import sys
import os


def main():
    """Main entry point for {title}"""
    print("=" * 50)
    print(f"  {{' {title} ':=^48}}")
    print("=" * 50)
    print()

    # Project: {title}
    # This is a template - the AI version generates real logic!
    data = {{}}
    running = True

    while running:
        print("\\nOptions:")
        print("  1. Add item")
        print("  2. View items")
        print("  3. Remove item")
        print("  4. Exit")

        choice = input("\\nSelect option: ").strip()

        if choice == "1":
            key = input("Enter key: ").strip()
            value = input("Enter value: ").strip()
            data[key] = value
            print(f"✅ Added: {{key}} = {{value}}")
        elif choice == "2":
            if data:
                print("\\n📋 Current items:")
                for k, v in data.items():
                    print(f"   {{k}}: {{v}}")
            else:
                print("📭 No items yet.")
        elif choice == "3":
            key = input("Enter key to remove: ").strip()
            if key in data:
                del data[key]
                print(f"🗑️  Removed: {{key}}")
            else:
                print(f"❌ Key '{{key}}' not found.")
        elif choice == "4":
            running = False
            print("\\n👋 Goodbye!")
        else:
            print("❌ Invalid option.")


if __name__ == "__main__":
    main()
'''
        },
        "javascript": {
            "index.js": f'''/**
 * {title}
 * Generated on {date} by Daily Auto Project Generator
 * Author: Jay Singh (iamjaysingh)
 */

"use strict";

class MiniApp {{
    constructor(name) {{
        this.name = name;
        this.data = new Map();
        this.createdAt = new Date().toISOString();
    }}

    add(key, value) {{
        this.data.set(key, value);
        console.log(`✅ Added: ${{key}} = ${{value}}`);
    }}

    get(key) {{
        return this.data.get(key) || null;
    }}

    remove(key) {{
        if (this.data.has(key)) {{
            this.data.delete(key);
            console.log(`🗑️  Removed: ${{key}}`);
            return true;
        }}
        console.log(`❌ Key '${{key}}' not found.`);
        return false;
    }}

    list() {{
        if (this.data.size === 0) {{
            console.log("📭 No items yet.");
            return;
        }}
        console.log("\\n📋 Current items:");
        this.data.forEach((v, k) => {{
            console.log(`   ${{k}}: ${{v}}`);
        }});
    }}

    stats() {{
        return {{
            name: this.name,
            itemCount: this.data.size,
            createdAt: this.createdAt,
        }};
    }}
}}

// --- Main ---
const app = new MiniApp("{title}");
console.log("=".repeat(50));
console.log(`  {title}`);
console.log("=".repeat(50));

app.add("project", "{title}");
app.add("language", "JavaScript");
app.add("date", "{date}");
app.list();
console.log("\\n📊 Stats:", JSON.stringify(app.stats(), null, 2));
'''
        },
        "java": {
            "Main.java": f'''/**
 * {title}
 * Generated on {date} by Daily Auto Project Generator
 * @author Jay Singh (iamjaysingh)
 */

import java.util.*;

public class Main {{
    private Map<String, String> data;
    private String projectName;

    public Main(String name) {{
        this.projectName = name;
        this.data = new LinkedHashMap<>();
    }}

    public void add(String key, String value) {{
        data.put(key, value);
        System.out.println("✅ Added: " + key + " = " + value);
    }}

    public String get(String key) {{
        return data.getOrDefault(key, null);
    }}

    public boolean remove(String key) {{
        if (data.containsKey(key)) {{
            data.remove(key);
            System.out.println("🗑️  Removed: " + key);
            return true;
        }}
        System.out.println("❌ Key '" + key + "' not found.");
        return false;
    }}

    public void list() {{
        if (data.isEmpty()) {{
            System.out.println("📭 No items yet.");
            return;
        }}
        System.out.println("\\n📋 Current items:");
        for (Map.Entry<String, String> entry : data.entrySet()) {{
            System.out.println("   " + entry.getKey() + ": " + entry.getValue());
        }}
    }}

    public static void main(String[] args) {{
        System.out.println("=".repeat(50));
        System.out.println("  {title}");
        System.out.println("=".repeat(50));

        Main app = new Main("{title}");
        Scanner scanner = new Scanner(System.in);
        boolean running = true;

        while (running) {{
            System.out.println("\\nOptions: 1.Add  2.View  3.Remove  4.Exit");
            System.out.print("Select: ");
            String choice = scanner.nextLine().trim();

            switch (choice) {{
                case "1":
                    System.out.print("Key: ");
                    String key = scanner.nextLine().trim();
                    System.out.print("Value: ");
                    String value = scanner.nextLine().trim();
                    app.add(key, value);
                    break;
                case "2":
                    app.list();
                    break;
                case "3":
                    System.out.print("Key to remove: ");
                    app.remove(scanner.nextLine().trim());
                    break;
                case "4":
                    running = false;
                    System.out.println("\\n👋 Goodbye!");
                    break;
                default:
                    System.out.println("❌ Invalid option.");
            }}
        }}
        scanner.close();
    }}
}}
'''
        },
        "c": {
            "main.c": f'''/*
 * {title}
 * Generated on {date} by Daily Auto Project Generator
 * Author: Jay Singh (iamjaysingh)
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_ITEMS 100
#define MAX_LEN 256

typedef struct {{
    char key[MAX_LEN];
    char value[MAX_LEN];
}} Item;

typedef struct {{
    Item items[MAX_ITEMS];
    int count;
    char name[MAX_LEN];
}} DataStore;

void init_store(DataStore *store, const char *name) {{
    store->count = 0;
    strncpy(store->name, name, MAX_LEN - 1);
    store->name[MAX_LEN - 1] = '\\0';
}}

int add_item(DataStore *store, const char *key, const char *value) {{
    if (store->count >= MAX_ITEMS) {{
        printf("❌ Store is full!\\n");
        return -1;
    }}
    strncpy(store->items[store->count].key, key, MAX_LEN - 1);
    strncpy(store->items[store->count].value, value, MAX_LEN - 1);
    store->count++;
    printf("✅ Added: %s = %s\\n", key, value);
    return 0;
}}

void list_items(const DataStore *store) {{
    if (store->count == 0) {{
        printf("📭 No items yet.\\n");
        return;
    }}
    printf("\\n📋 Current items (%d):\\n", store->count);
    for (int i = 0; i < store->count; i++) {{
        printf("   %s: %s\\n", store->items[i].key, store->items[i].value);
    }}
}}

int main() {{
    DataStore store;
    init_store(&store, "{title}");

    printf("==================================================\\n");
    printf("  {title}\\n");
    printf("==================================================\\n");

    add_item(&store, "project", "{title}");
    add_item(&store, "language", "C");
    add_item(&store, "date", "{date}");
    list_items(&store);

    printf("\\n👋 Done!\\n");
    return 0;
}}
'''
        },
        "go": {
            "main.go": f'''/*
 * {title}
 * Generated on {date} by Daily Auto Project Generator
 * Author: Jay Singh (iamjaysingh)
 */

package main

import (
\t"fmt"
\t"strings"
\t"time"
)

type DataStore struct {{
\tName    string
\tItems   map[string]string
\tCreated time.Time
}}

func NewDataStore(name string) *DataStore {{
\treturn &DataStore{{
\t\tName:    name,
\t\tItems:   make(map[string]string),
\t\tCreated: time.Now(),
\t}}
}}

func (ds *DataStore) Add(key, value string) {{
\tds.Items[key] = value
\tfmt.Printf("✅ Added: %s = %s\\n", key, value)
}}

func (ds *DataStore) Get(key string) (string, bool) {{
\tval, ok := ds.Items[key]
\treturn val, ok
}}

func (ds *DataStore) Remove(key string) bool {{
\tif _, ok := ds.Items[key]; ok {{
\t\tdelete(ds.Items, key)
\t\tfmt.Printf("🗑️  Removed: %s\\n", key)
\t\treturn true
\t}}
\tfmt.Printf("❌ Key '%s' not found.\\n", key)
\treturn false
}}

func (ds *DataStore) List() {{
\tif len(ds.Items) == 0 {{
\t\tfmt.Println("📭 No items yet.")
\t\treturn
\t}}
\tfmt.Printf("\\n📋 Current items (%d):\\n", len(ds.Items))
\tfor k, v := range ds.Items {{
\t\tfmt.Printf("   %s: %s\\n", k, v)
\t}}
}}

func main() {{
\tfmt.Println(strings.Repeat("=", 50))
\tfmt.Println("  {title}")
\tfmt.Println(strings.Repeat("=", 50))

\tstore := NewDataStore("{title}")
\tstore.Add("project", "{title}")
\tstore.Add("language", "Go")
\tstore.Add("date", "{date}")
\tstore.List()

\tfmt.Println("\\n👋 Done!")
}}
'''
        },
    }

    return templates.get(language, templates["python"])


# ─── Project File Generation ─────────────────────────────────────────────────

def generate_project_readme(language, project_type, date, streak_info):
    """Generate a README.md for the daily project"""
    title = project_type.replace("-", " ").title()
    lang_display = language.capitalize()

    emoji_map = {
        "python": "🐍",
        "javascript": "🟨",
        "java": "☕",
        "c": "⚙️",
        "go": "🐹",
    }
    emoji = emoji_map.get(language, "💻")

    readme = f"""# {emoji} {title}

> **Daily Auto Project** — Generated on {date}
> Language: **{lang_display}** | Project #{streak_info.get('total_projects', 0) + 1}

## 📖 About

This is an automatically generated mini-project as part of the **Daily Auto Projects** initiative.
Each day, a new project is created to practice coding across multiple languages.

## 🚀 How to Run

"""

    run_commands = {
        "python": f"```bash\npython3 main.py\n```",
        "javascript": f"```bash\nnode index.js\n```",
        "java": f"```bash\njavac Main.java && java Main\n```",
        "c": f"```bash\ngcc -o main main.c && ./main\n```",
        "go": f"```bash\ngo run main.go\n```",
    }

    readme += run_commands.get(language, "```bash\n# Run the main file\n```")

    readme += f"""

## 📊 Streak Info

- 🔥 Current Streak: **{streak_info.get('current_streak', 0)} days**
- 📁 Total Projects: **{streak_info.get('total_projects', 0)}**

---

*Generated by [Daily Auto Project Generator](https://github.com/iamjaysingh/daily-auto-projects)*
"""
    return readme


def create_project(config, dry_run=False):
    """Main function to create a daily project"""
    today = get_today()

    # Pick random language and project type
    language = random.choice(config["languages"])
    project_types = config["project_types"].get(language, ["mini-project"])
    project_type = random.choice(project_types)

    # Create unique project folder name
    project_name = f"{today}-{language}-{project_type}"
    project_path = os.path.join(PROJECTS_DIR, project_name)

    # Check if project already exists for today with this exact name
    if os.path.exists(project_path):
        # Add a random suffix
        suffix = hashlib.md5(str(random.random()).encode()).hexdigest()[:4]
        project_name = f"{today}-{language}-{project_type}-{suffix}"
        project_path = os.path.join(PROJECTS_DIR, project_name)

    print(f"\n{'='*60}")
    print(f"  🚀 Daily Auto Project Generator")
    print(f"{'='*60}")
    print(f"  📅 Date:     {today}")
    print(f"  💻 Language: {language}")
    print(f"  📦 Project:  {project_type}")
    print(f"  📂 Path:     {project_path}")
    print(f"{'='*60}\n")

    # Create project directory
    os.makedirs(project_path, exist_ok=True)

    # Try AI generation first
    files = None
    if config.get("use_ai", False):
        print("🤖 Attempting AI-powered code generation...")
        files = generate_with_gemini(language, project_type)
        if files:
            print("✅ AI generation successful!")
        else:
            print("📁 Using template-based generation...")

    # Fallback to templates
    if files is None:
        files = load_template(language, project_type)
        print("✅ Template loaded!")

    # Write project files
    for filename, content in files.items():
        filepath = os.path.join(project_path, filename)
        with open(filepath, "w") as f:
            f.write(content)
        print(f"  📝 Created: {filename}")

    # Generate README
    streak_info = get_streak_info()
    readme_content = generate_project_readme(language, project_type, today, streak_info)
    readme_path = os.path.join(project_path, "README.md")
    with open(readme_path, "w") as f:
        f.write(readme_content)
    print(f"  📝 Created: README.md")

    # Update streak
    streak = update_streak(language, project_type)
    print(f"\n🔥 Streak: {streak['current_streak']} days | Total: {streak['total_projects']} projects")

    if dry_run:
        print("\n🏃 DRY RUN — Skipping git operations")
        return project_name, project_path

    return project_name, project_path


# ─── Git Operations ──────────────────────────────────────────────────────────

def git_commit_and_push(project_name):
    """Commit and push changes to GitHub"""
    config = load_config()
    prefix = config.get("commit_message_prefix", "🚀 Daily Project")

    try:
        print("\n📦 Git operations...")

        # We operate from the repo root
        os.chdir(SCRIPT_DIR)

        # Configure git user (needed in GitHub Actions)
        subprocess.run(["git", "config", "user.name", "Jay Singh"], check=True)
        subprocess.run(["git", "config", "user.email", "jayrakeshsingh8796@gmail.com"], check=True)

        # Add all new files
        subprocess.run(["git", "add", "-A"], check=True)
        print("  ✅ Added files to staging")

        # Commit with unique message
        today = get_today()
        commit_msg = f"{prefix}: {project_name} ({today})"
        result = subprocess.run(
            ["git", "commit", "-m", commit_msg],
            capture_output=True, text=True
        )

        if result.returncode == 0:
            print(f"  ✅ Committed: {commit_msg}")
        else:
            if "nothing to commit" in result.stdout or "nothing to commit" in result.stderr:
                print("  ⚠️  Nothing to commit (already up to date)")
                return True
            else:
                print(f"  ❌ Commit failed: {result.stderr}")
                return False

        # Push
        result = subprocess.run(
            ["git", "push"],
            capture_output=True, text=True
        )

        if result.returncode == 0:
            print("  ✅ Pushed to GitHub!")
        else:
            print(f"  ❌ Push failed: {result.stderr}")
            # Try setting upstream
            result = subprocess.run(
                ["git", "push", "-u", "origin", "main"],
                capture_output=True, text=True
            )
            if result.returncode == 0:
                print("  ✅ Pushed to GitHub (set upstream)!")
            else:
                print(f"  ❌ Push failed again: {result.stderr}")
                return False

        return True

    except Exception as e:
        print(f"  ❌ Git error: {e}")
        traceback.print_exc()
        return False


# ─── Update Root README ──────────────────────────────────────────────────────

def update_root_readme():
    """Update the root README with latest project info"""
    streak = get_streak_info()
    today = get_today()

    # Count projects by language
    lang_stats = streak.get("languages_used", {})
    total = streak.get("total_projects", 0)

    # List recent projects (last 10)
    recent_projects = []
    if os.path.exists(PROJECTS_DIR):
        dirs = sorted(os.listdir(PROJECTS_DIR), reverse=True)
        for d in dirs[:10]:
            if os.path.isdir(os.path.join(PROJECTS_DIR, d)):
                recent_projects.append(d)

    readme = f"""# 🚀 Daily Auto Projects

> Automatically generated coding projects — one every day!
> Built by **Jay Singh** ([iamjaysingh](https://github.com/iamjaysingh))

## 📊 Stats

| Metric | Value |
|--------|-------|
| 🔥 Current Streak | **{streak.get('current_streak', 0)} days** |
| 📁 Total Projects | **{total}** |
| 📅 Last Updated | **{today}** |

## 🗂️ Languages Used

"""

    for lang, count in sorted(lang_stats.items(), key=lambda x: x[1], reverse=True):
        emoji_map = {"python": "🐍", "javascript": "🟨", "java": "☕", "c": "⚙️", "go": "🐹"}
        emoji = emoji_map.get(lang, "💻")
        bar = "█" * min(count * 2, 30)
        readme += f"| {emoji} {lang.capitalize()} | {bar} **{count}** |\n"

    readme += """
## 📂 Recent Projects

"""

    for proj in recent_projects:
        readme += f"- [`{proj}`](./projects/{proj}/)\n"

    readme += """
## ⚙️ How It Works

This repository is powered by **GitHub Actions** that run daily:

1. ⏰ **Cron trigger** at 9:00 AM IST (3:30 AM UTC)
2. 🤖 **AI generates** a unique mini-project using Google Gemini
3. 📁 **Falls back** to high-quality templates if AI is unavailable
4. 📦 **Auto-commits** and pushes to this repository

## 🛠️ Setup

1. Fork this repository
2. Add your `GEMINI_API_KEY` as a repository secret
3. Enable GitHub Actions
4. Projects will be generated daily!

---

*Powered by [Daily Auto Project Generator](https://github.com/iamjaysingh/daily-auto-projects)* ✨
"""

    readme_path = os.path.join(SCRIPT_DIR, "README.md")
    with open(readme_path, "w") as f:
        f.write(readme)
    print("  📝 Updated root README.md")


# ─── Main Entry Point ────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Daily Auto Project Generator")
    parser.add_argument("--dry-run", action="store_true", help="Generate project without git operations")
    parser.add_argument("--no-ai", action="store_true", help="Skip AI generation, use templates only")
    parser.add_argument("--language", type=str, help="Force a specific language")
    args = parser.parse_args()

    # Load config
    config = load_config()

    if args.no_ai:
        config["use_ai"] = False

    if args.language:
        config["languages"] = [args.language]

    # Ensure projects directory exists
    os.makedirs(PROJECTS_DIR, exist_ok=True)

    try:
        # Generate the project
        project_name, project_path = create_project(config, dry_run=args.dry_run)

        # Update root README
        update_root_readme()

        if not args.dry_run:
            # Git commit and push
            success = git_commit_and_push(project_name)
            if success:
                print(f"\n🎉 Success! Project '{project_name}' created and pushed!")
            else:
                print(f"\n⚠️  Project created but push failed. Check git configuration.")
                sys.exit(1)
        else:
            print(f"\n🎉 Dry run complete! Project created at: {project_path}")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
