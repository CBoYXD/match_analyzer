# Football Team Analytics

A Streamlit application for analyzing football team statistics using the football-data.org API.

## Features

- View team statistics from top 5 European leagues
- Analyze team performance metrics
- Track match history
- Download match statistics in CSV format
- Auto-refresh data every 10 minutes

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/football-analytics.git
cd football-analytics
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -e .
```

## Configuration

1. Create a `.streamlit/secrets.toml` file with your football-data.org API key:
```toml
football_api_key = "your-api-key-here"
```

## Usage

Run the application:
```bash
streamlit run app.py
```

## Development

Install development dependencies:
```bash
pip install -e ".[dev]"
```

Run tests:
```bash
pytest
```

Format code:
```bash
black src tests
isort src tests
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.