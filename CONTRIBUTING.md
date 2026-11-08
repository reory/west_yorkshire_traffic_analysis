# Contributing to West Yorkshire Traffic Analysis

Thank you for taking the time to contribute.

Whether you're fixing a bug, improving documentation, or proposing a new feature, all contributions are welcome.

## 🕵🏼‍♀️ Reporting Issues

If you discover a bug or have an idea for an improvement:

1. Check existing issues before opening a new one.
2. Provide a clear description of the problem or suggestion.
3. Include screenshots, error messages, or reproduction steps where possible.

## 🛠️ Development Setup

Clone the repository:

```bash
git clone https://github.com/reory/west_yorkshire_traffic_analysis.git
cd west_yorkshire_traffic_analysis
```

Install dependencies:

```bash
uv sync
```

Run the dashboard:

```bash
streamlit run app.py
```

Run the test suite:

```bash
pytest
```

Generate a coverage report:

```bash
pytest --cov
```

## 🔀 Pull Requests

1. Fork the repository.
2. Create a feature branch.

```bash
git checkout -b feature/my-feature
```

3. Make your changes.
4. Add or update tests where appropriate.
5. Run the test suite and ensure all tests pass.
6. Submit a pull request with a clear description of the changes.

## 🧪 Testing

This project uses:

- pytest
- pytest-cov
- Hypothesis

New features should include tests where practical.

## 📝 Code Style

Please aim to:

- Keep functions focused and easy to read.
- Use descriptive variable and function names.
- Add docstrings to public functions.
- Keep comments concise and meaningful.
- Follow existing project conventions.

## 💡 Feature Ideas

Roadmap items can be found in the README.

If you'd like to work on a larger enhancement, please open an issue first so we can discuss the approach before significant development begins.

## 🙏 Thank You

Every contribution, whether it's a bug report, documentation improvement, test enhancement, or new feature, helps make the project better.