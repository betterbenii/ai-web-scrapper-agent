
from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
AUTH = 'brd-customer-hl_a5f468c1-zone-ai_scraper:d9revvqp2ael'
SBR_WEBDRIVER = f'https://{AUTH}@brd.superproxy.io:9515'
import time

def scrape_website(website):
    """
    Scrape the given website using Selenium and the Chrome webdriver.

    The function will navigate to the given website, wait for the Captcha to be solved,
    and then take a screenshot of the page. The page content will be returned as a string.

    Args:
        website (str): The URL of the website to scrape.

    Returns:
        str: The HTML content of the scraped website.
    """
    print("Launching Chrome...")
    sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, 'goog', 'chrome')
    with Remote(sbr_connection, options=ChromeOptions()) as driver:
        
        # Navigate to the given website
        driver.get(website)

        # Wait for the Captcha to be solved
        print('Waiting for Captcha to solve...')
        solve_res= driver.execute('executeCdpCommand', {'cmd': 'Captcha.waitForSolve', 'params': {'detectTimeout': 10000}})
        print("Captcha solve status: ", solve_res ['value'] ['status'])
        
        # Take a screenshot of the page
        print('Taking page screenshot to file page.png')
        driver.get_screenshot_as_file('./page.png')

        # Scrape the page content
        print('Navigated! Scraping page content...')
        html = driver.page_source
        print(html)
        return html


def extract_body_content(html_content):
    """
    Extract the body content from the given HTML content.

    This function takes the given HTML content and extracts the body content from it.
    If the body content is present, it will be returned as a string. Otherwise, an empty
    string is returned.

    Args:
        html_content (str): The HTML content of the page.

    Returns:
        str: The extracted body content of the page.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    
    # If the body content is present, return it as a string
    if body_content:
        return str(body_content)
    else:
        # Otherwise, return an empty string
        return ""



def clean_body_content(body_content):
    """
    Clean the given body content by extracting the text and removing any
    unnecessary tags and whitespace.

    This function takes the given body content and removes any unnecessary tags
    such as scripts and styles. It then extracts the text content and trims any
    leading or trailing whitespace from the lines.

    Args:
        body_content (str): The body content of the page.

    Returns:
        str: The cleaned body content of the page.
    """
    soup = BeautifulSoup(body_content, "html.parser")

    # Remove any unnecessary tags such as scripts and styles
    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()

    # Get text or further process the content
    cleaned_content = soup.get_text(separator="\n")

    # Trim any leading or trailing whitespace from the lines
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )

    return cleaned_content

#split the text into batches for token usage minimization for the LLM
def split_dom_content(dom_content, max_length=6000):
    """
    Split the given DOM content into batches based on the given maximum length.

    This function takes the given DOM content and splits it into batches of the
    given maximum length. The batches are returned as a list of strings, where
    each string represents a batch of the DOM content.

    The maximum length is set to 6000 by default, which is the maximum number of
    characters allowed in a single prompt for the LLM.

    Args:
        dom_content (str): The DOM content of the page.
        max_length (int): The maximum length of each batch. Defaults to 6000.

    Returns:
        list: A list of strings, where each string represents a batch of the DOM
            content.
    """
    return [
        dom_content[i:i+max_length] for i in range(0, len(dom_content), max_length)
    ]
