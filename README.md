# 🛠️ my-django-starter

A command-line helper tool to quickly scaffold, configure, and run Django projects using a clean, pluggable step-based pipeline system.

---

## 📁 Project Structure


---

## 🧩 Core Components

### ✅ Step (base class)

- Defined in: `builder/base.py`
- Abstract class defining the `execute(context)` method.
- All project steps inherit from this class.

### ✅ Concrete Steps

- Examples: `Banner`, `OSDetector`, `VenvCreator`, `DjangoInstaller`, `ServerRunner`, etc.
- Inherit from `Step` and implement `execute()`.
- Each step performs a single responsibility in the setup pipeline.

### ✅ Pipeline (composition)

- Holds a list of `Step` instances.
- Calls `execute(context)` for each step in sequence.
- Handles exceptions gracefully and displays error messages using `status_tag`.

### ✅ main.py (orchestration)

- Imports and arranges steps into a pipeline.
- Calls `pipeline.run()` to execute all steps.
- Optionally writes a `.success_marker` file after successful execution.

---

## 🔁 Relationships

| Concept       | Description                                                   |
|---------------|---------------------------------------------------------------|
| Inheritance   | All steps inherit from `Step`.                                |
| Composition   | `Pipeline` is composed of multiple `Step` instances.          |
| Reusability   | Steps are modular and easily swappable.                       |

---

## 🚀 Usage

```bash
$ python3 main.py
