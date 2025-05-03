# 🚀 GitHub Repo Fetcher

A lightweight Python script to fetch and display public repositories of any GitHub user using the [GitHub REST API](https://docs.github.com/en/rest).

## 📖 Description

This tool allows you to fetch up to 100 public repositories for any GitHub user and display:
- ✅ Repository Name
- 📄 Description
- 🔗 URL to the repository

It’s a great utility for:
- Developers showcasing their work.
- Recruiters evaluating candidates.
- Quick insights into open-source contributors.

---

## 📦 Features

- 🔍 Simple GitHub username-based lookup.
- 🧾 Clean output of repository details.
- 🌐 Uses Python's `requests` library and GitHub's public API.
- ✅ No authentication or API key required for public repos.

---

## 🛠️ Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/AyyanYe/github-repo-fetcher.git
cd github-repo-fetcher
````

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

* **Windows**:

  ```bash
  venv\Scripts\activate
  ```

* **macOS/Linux**:

  ```bash
  source venv/bin/activate
  ```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the script

```bash
python github_repos.py
```

📝 You can change the GitHub username in the script:

```python
username = "AyyanYe"
```

---

## 📂 Project Structure

```
github-repo-fetcher/
├── github_repos.py       # Main script
├── README.md             # Project documentation
└── requirements.txt      # Dependencies
```

---

## ✅ Requirements

* Python 3.6+
* `requests` library

To install the dependencies manually:

```bash
pip install requests
```

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 👤 Author

**Ayyan Ahmed**
🔗 [GitHub](https://github.com/AyyanYe)

---

⭐️ If you found this useful, feel free to star the repo!
