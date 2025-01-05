import requests
from bs4 import BeautifulSoup
from googlesearch import search

def scrape_bing_search(query, max_results=10, lang="en"):
    """
    Scrape Bing search results for a given query.

    Parameters:
    query (str): The search query.
    max_results (int): Maximum number of search results to retrieve (default is 10).
    lang (str): Language of the search query (default is 'en').

    Returns:
    list: A list of URLs from the search results.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    base_url = "https://www.bing.com/search"
    params = {
        "q": query,
        "count": max_results,
        "mkt": lang,
    }

    try:
        response = requests.get(base_url, headers=headers, params=params)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract URLs from the search results
        urls = []
        for result in soup.find_all("li", class_="b_algo"):
            link = result.find("a")
            if link and link.get("href"):
                urls.append(link["href"])

        # If no results are found, try an alternative class or structure
        if not urls:
            for result in soup.find_all("h2"):
                link = result.find("a")
                if link and link.get("href"):
                    urls.append(link["href"])

        return urls
    except Exception as e:
        print(f"An error occurred during Bing search scraping: {e}")
        return []

def find_website_rank(query, target_url, max_results=100, lang="en"):
    """
    Find the rank of a specific website for a given search query using both Google and Bing.

    Parameters:
    query (str): The search query.
    target_url (str): The URL of the website to find in search results.
    max_results (int): Maximum number of search results to retrieve (default is 100).
    lang (str): Language of the search query (default is 'en').

    Returns:
    tuple: A tuple containing the Google rank and Bing rank of the website.
           If the website is not found, the rank will be -1.
    """
    google_rank = -1
    bing_rank = -1

    # Search using Google
    try:
        for rank, url in enumerate(search(query, num_results=max_results, lang=lang), start=1):
            if target_url in url:
                google_rank = rank
                break  # Stop searching once the target URL is found
    except Exception as e:
        print(f"An error occurred during Google search: {e}")

    # Search using Bing (scraping)
    bing_results = scrape_bing_search(query, max_results=max_results, lang=lang)
    for rank, url in enumerate(bing_results, start=1):
        if target_url in url:
            bing_rank = rank
            break  # Stop searching once the target URL is found

    return google_rank, bing_rank

# Example usage
query = "tehranmusicacademy"
target_url = "tehranmusicacademy.com"

google_rank, bing_rank = find_website_rank(query, target_url)

if google_rank != -1:
    print(f"Website '{target_url}' is ranked #{google_rank} on Google for the query '{query}'.")
else:
    print(f"Website '{target_url}' was not found in the top {100} Google results for the query '{query}'.")

if bing_rank != -1:
    print(f"Website '{target_url}' is ranked #{bing_rank} on Bing for the query '{query}'.")
else:
    print(f"Website '{target_url}' was not found in the top {100} Bing results for the query '{query}'.")