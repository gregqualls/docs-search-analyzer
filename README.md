# Documentation Search Analyzer

A configurable tool to analyze search results across different documentation sites. Currently supports analyzing search results from docs.upsun.com and docs.platform.sh, with the ability to add more sites through configuration.

## Features

- Automated search result analysis
- Configurable for multiple documentation sites
- Extracts search result titles, URLs, and sections
- Saves results to CSV files for analysis
- Headless browser operation
- Configurable delays and result limits
- Command-line interface for easy use

## Prerequisites

- Python 3.x
- Google Chrome browser
- pip (Python package installer)

## Installation

1. Clone this repository:
```bash
git clone [your-repo-url]
cd [repository-directory]
```

2. Create and activate a virtual environment:
```bash
# Create virtual environment
python3 -m venv venv

# Activate on macOS/Linux
source venv/bin/activate

# Activate on Windows
.\venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

## Configuration

### Search Phrases
Create or modify `search_phrases.txt` with one search phrase per line:
```
deployment process overview
supported programming languages
environment configuration settings
...
```

### Site Configuration
Site-specific settings are managed in `search_config.py`. Each site configuration includes:

```python
SITES = {
    "site_key": {
        "name": "Site Display Name",
        "base_url": "https://docs.example.com",
        "search_path": "/search.html",
        "search_query_param": "q",
        "selectors": {
            "result_container": "CSS selector for result container",
            "result_title": "CSS selector for result title",
            "result_url": "CSS selector for result URL"
        },
        "max_results": 5,
        "delay_between_searches": 1,
        "page_load_delay": 2
    }
}
```

#### Configuration Parameters:
- `name`: Display name for the documentation site
- `base_url`: Base URL of the documentation site
- `search_path`: Path to the search page
- `search_query_param`: URL parameter name for search queries
- `selectors`: CSS selectors for finding elements:
  - `result_container`: Container element for each search result
  - `result_title`: Element containing the result title
  - `result_url`: Element containing the result URL
- `max_results`: Maximum number of results to process per search
- `delay_between_searches`: Delay in seconds between searches
- `page_load_delay`: Additional delay after page load

## Usage

### Basic Usage
Run the analyzer with default settings (Upsun docs):
```bash
python3 analyze_search.py
```

### Specify a Different Site
```bash
python3 analyze_search.py --site platform
```

### Use Custom Search Phrases File
```bash
python3 analyze_search.py --phrases custom_phrases.txt
```

### Command Line Arguments
- `--site`: Which documentation site to analyze (default: upsun)
- `--phrases`: File containing search phrases (default: search_phrases.txt)

## Output

Results are saved to CSV files with the following naming pattern:
```
search_analysis_[site_name]_[timestamp].csv
```

The CSV files contain:
- date: Date of analysis
- site: Documentation site name
- search_phrase: Search phrase used
- result_url: URL of the result
- section: Section of the documentation
- page_title: Title of the page
- position: Position in search results (1-5)

## Adding New Sites

To add support for a new documentation site:

1. Add a new configuration to `search_config.py`
2. Verify the CSS selectors by inspecting the site's search results page
3. Test the configuration with a few search phrases

Example configuration template:
```python
"new_site": {
    "name": "New Site Docs",
    "base_url": "https://docs.newsite.com",
    "search_path": "/search",
    "search_query_param": "q",
    "selectors": {
        "result_container": "div.search-result",
        "result_title": "h3 a",
        "result_url": "h3 a"
    },
    "max_results": 5,
    "delay_between_searches": 1,
    "page_load_delay": 2
}
```

## Troubleshooting

1. **ChromeDriver Issues**:
   - Ensure Google Chrome is installed
   - Try running without headless mode for debugging
   - Check Chrome and ChromeDriver versions match

2. **No Results Found**:
   - Verify site selectors in `search_config.py`
   - Check if site requires JavaScript
   - Increase `page_load_delay` if site is slow

3. **Permission Errors**:
   - Ensure virtual environment is activated
   - Check file permissions for output directory

## Contributing

Contributions are welcome! Please feel free to submit pull requests with improvements or additional site configurations. 