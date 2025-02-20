"""
Configuration settings for different documentation sites.
Add new sites by creating new configuration dictionaries.
"""

SITES = {
    "upsun": {
        "name": "Upsun Docs",
        "base_url": "https://docs.upsun.com",
        "search_path": "/search.html",
        "search_query_param": "q",
        # CSS Selectors for finding elements
        "selectors": {
            "result_container": "ul li.mb-4",
            "result_title": "h3 a.text-skye-dark",
            "result_url": "h3 a.text-skye-dark",
        },
        # Maximum number of results to process per search
        "max_results": 5,
        # Delay in seconds between searches
        "delay_between_searches": 1,
        # Additional delay after page load
        "page_load_delay": 2
    },
    "platform": {
        "name": "Platform.sh Docs",
        "base_url": "https://docs.platform.sh",
        "search_path": "/search.html",
        "search_query_param": "q",
        # CSS Selectors for finding elements (these need to be verified for Platform.sh)
        "selectors": {
            "result_container": "ul li.mb-4",                        # Example - needs verification
            "result_title": "h3 a.text-skye-dark",                   # Example - needs verification
            "result_url": "h3 a.text-skye-dark",                    # Example - needs verification
        },
        "max_results": 5,
        "delay_between_searches": 1,
        "page_load_delay": 2
    }
    # Add more sites here as needed
} 