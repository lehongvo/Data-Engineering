"""
POPULAR PYTHON PACKAGES GUIDE
This guide demonstrates the usage of popular Python packages with practical examples.
"""

# 1. INTRODUCTION TO APIs AND REQUESTS
import requests
import os
from dotenv import load_dotenv


def api_example():
    """
    Demonstrates basic API usage with the requests package
    """
    # Basic GET request
    response = requests.get("https://api.github.com/users/python")
    print("Basic API Call:", response.json())

    # POST request with data
    data = {"key": "value"}
    response = requests.post("https://httpbin.org/post", json=data)
    print("POST Request:", response.json())


# 2. YELP API EXAMPLE
def yelp_api_example():
    """
    Example of using Yelp's Fusion API
    Requires: YELP_API_KEY in .env file
    """
    load_dotenv()
    api_key = os.getenv("YELP_API_KEY")
    headers = {"Authorization": f"Bearer {api_key}"}

    # Search for businesses
    params = {"term": "coffee", "location": "San Francisco", "limit": 3}
    response = requests.get(
        "https://api.yelp.com/v3/businesses/search", headers=headers, params=params
    )
    return response.json()


# 3. SMS MESSAGING WITH TWILIO
from twilio.rest import Client


def send_sms_example():
    """
    Example of sending SMS using Twilio
    Requires: TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN in .env file
    """
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body="Hello from Python!",
        from_="+1234567890",  # Your Twilio number
        to="+0987654321",  # Recipient's number
    )
    return message.sid


# 4. WEB SCRAPING WITH BEAUTIFULSOUP
import requests
from bs4 import BeautifulSoup


def web_scraping_example():
    """
    Demonstrates web scraping with BeautifulSoup
    """
    # Get webpage content
    url = "https://quotes.toscrape.com"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Extract quotes
    quotes = []
    for quote in soup.select(".quote"):
        quotes.append(
            {
                "text": quote.select_one(".text").get_text(),
                "author": quote.select_one(".author").get_text(),
            }
        )
    return quotes


# 5. BROWSER AUTOMATION WITH SELENIUM
from selenium import webdriver
from selenium.webdriver.common.by import By


def browser_automation_example():
    """
    Demonstrates browser automation with Selenium
    Requires: Chrome WebDriver
    """
    driver = webdriver.Chrome()
    try:
        # Navigate to website
        driver.get("https://www.python.org")

        # Find and interact with elements
        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys("python")
        search_box.submit()

        # Get results
        results = driver.find_elements(By.CSS_SELECTOR, ".list-recent-events li")
        return [result.text for result in results]
    finally:
        driver.quit()


# 6. WORKING WITH PDFs
from PyPDF2 import PdfReader, PdfWriter


def pdf_example():
    """
    Demonstrates PDF manipulation with PyPDF2
    """
    # Reading PDF
    reader = PdfReader("example.pdf")
    page = reader.pages[0]
    text = page.extract_text()

    # Creating PDF
    writer = PdfWriter()
    writer.add_page(page)
    with open("new_document.pdf", "wb") as output:
        writer.write(output)


# 7. WORKING WITH EXCEL
import pandas as pd


def excel_example():
    """
    Demonstrates Excel file manipulation with pandas
    """
    # Create sample data
    data = {
        "Name": ["John", "Anna", "Peter"],
        "Age": [28, 22, 35],
        "City": ["New York", "Paris", "London"],
    }

    # Create Excel file
    df = pd.DataFrame(data)
    df.to_excel("output.xlsx", index=False)

    # Read Excel file
    df_read = pd.read_excel("output.xlsx")
    return df_read


# 8. NUMPY EXAMPLES
import numpy as np


def numpy_examples():
    """
    Demonstrates NumPy array operations
    """
    # Create arrays
    arr1 = np.array([1, 2, 3, 4, 5])
    arr2 = np.array([6, 7, 8, 9, 10])

    # Basic operations
    print("Sum:", arr1 + arr2)
    print("Mean:", np.mean(arr1))
    print("Matrix multiplication:", np.dot(arr1, arr2))

    # Reshaping
    matrix = arr1.reshape(5, 1)
    print("Reshaped array:", matrix)

    # Statistical operations
    print("Standard deviation:", np.std(arr1))
    print("Maximum value:", np.max(arr1))


def main():
    """
    Main function to demonstrate all examples
    """
    print("\n1. Basic API Example:")
    api_example()

    print("\n2. Web Scraping Example:")
    quotes = web_scraping_example()
    print(f"Found {len(quotes)} quotes")

    print("\n3. NumPy Examples:")
    numpy_examples()

    # Note: Some examples are commented out as they require additional setup
    # print("\n4. Yelp API Example:")
    # yelp_results = yelp_api_example()

    # print("\n5. SMS Example:")
    # sms_result = send_sms_example()

    # print("\n6. Browser Automation Example:")
    # selenium_results = browser_automation_example()

    print("\n7. Excel Example:")
    excel_results = excel_example()
    print(excel_results)


if __name__ == "__main__":
    main()
