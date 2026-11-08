# Contributing
1. Open an issue with problem and proposed behavior.
2. Create a focused branch.
3. Add tests with code changes.
4. Run `pytest`, `ruff check backend tests`, and `cd frontend && npm run build`.
5. Update docs and scenario expectations.
6. Submit a pull request with test results.

New detection rules need positive and benign negative tests, rule ID and severity rationale. Do not commit secrets or live exploit targets.
