import os

# Colour codes for terminal output 
GREEN = "\033[92m" 
YELLOW = "\033[93m" 
BLUE = "\033[94m" 
RED = "\033[91m" 
RESET = "\033[0m"

TEMPLATE_FILE = "readme_template.md"

# Helper: Ask user with default
def ask(prompt, default=""):
    value = input(f"{prompt} [{default}]: ").strip()
    return value or default



# Auto-detect project structure
def detect_structure():
    items = []
    for name in os.listdir("."):
        if name.startswith("."):
            continue
        if name in ("README.md", "readme_template.md", "generate_readme.py"):
            continue
        if os.path.isdir(name):
            items.append(f"{name}/")
        else:
            items.append(name)
    return "\n".join(items) if items else "No files detected."


# Auto-suggest run command
def guess_run_command():
    files = os.listdir(".")

    if "main.py" in files:
        return "python main.py"
    if "api.py" in files:
        return "python api.py"
    if "run.py" in files:
        return "python run.py"
    if "manage.py" in files:
        return "python manage.py runserver"
    if "app.py" in files:
        return "python app.py"

    # fallback
    return "python <your_file>.py"


# Auto-detect technologies
def detect_technologies():
    tech = []

    # Python projects
    if os.path.exists("requirements.txt"):
        tech.append("Python 3.x")

        with open("requirements.txt", "r", encoding="utf-8") as f:
            reqs = f.read().lower()

            if "flask" in reqs:
                tech.append("Flask")
            if "django" in reqs:
                tech.append("Django")
            if "fastapi" in reqs:
                tech.append("FastAPI")

    if os.path.exists("pyproject.toml"):
        tech.append("Python (pyproject.toml)")

    # Node.js
    if os.path.exists("package.json"):
        tech.append("Node.js")

    if not tech:
        return "- Python 3.x"

    return "- " + "\n- ".join(tech)


# Main generator logic
def main():
    print(f"{BLUE}=== README generator (smart version) ==={RESET}")

    project_name = ask("Project name")
    short_description = ask("Short description", "A small Python project.")
    repo_url = ask("Git repo URL", "<add-later>")
    project_folder = ask("Project folder name", project_name or "project")

    # Smart defaults
    run_command = ask("Run command", guess_run_command())
    project_structure = ask("Project structure", detect_structure())
    technologies = ask("Technologies used", detect_technologies())

    notes = ask("Notes", "None yet.")
    features = ask("Features (bullet list, use - ...)", "- First feature\n- Second feature")

    # Load template
    with open(TEMPLATE_FILE, "r", encoding="utf-8") as f:
        template = f.read()

    # Fill template
    content = template.format(
        project_name=project_name,
        short_description=short_description,
        repo_url=repo_url,
        project_folder=project_folder,
        run_command=run_command,
        features=features,
        project_structure=project_structure,
        technologies=technologies,
        notes=notes,
    )

    # Write README.md
    output_path = os.path.join(os.getcwd(), "README.md")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"\n{GREEN}README.md created at: {output_path}{RESET}")


if __name__ == "__main__":
    main()
