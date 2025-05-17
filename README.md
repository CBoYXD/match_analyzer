# Football Team Analytics

A Streamlit application for analyzing football team statistics using the football-data.org API. The application provides a user-friendly interface in Ukrainian for analyzing team performance across top European leagues.

> **Note**: This project was entirely generated using AI tools. For more information about the AI-assisted development process, see [VIBECODING.md](VIBECODING.md).

## Features

- View team statistics from top European leagues
- Analyze team performance metrics including:
  - Wins, draws, and losses
  - Goals scored and conceded
  - Match history with detailed results
- Interactive data visualization with charts
- Download match statistics in CSV format
- Auto-refresh data every 10 minutes
- Ukrainian language interface

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

The application will open in your default web browser. You can:
1. Select a league from the dropdown menu
2. Choose a team to analyze
3. Click "Показати статистику команди" to view detailed statistics
4. Download the match data using the "Завантажити статистику" button

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

## Project Structure

- `app.py` - Main Streamlit application
- `src/` - Source code directory
  - `api/` - API client implementation
  - `config/` - Configuration settings
  - `models/` - Data models
  - `services/` - Business logic services
- `tests/` - Test files
- `.streamlit/` - Streamlit configuration

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.