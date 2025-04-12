import requests
from bs4 import BeautifulSoup

def scrape_hackernews(num_posts):
    url = "https://news.ycombinator.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    data = []
    for item in soup.find_all('tr', class_='athing'):
        title = item.find('a', class_='storylink').text
        link = item.find('a', class_='storylink')['href']
        
        # Fetch the content of the linked page
        if link.startswith('https://'):
            response = requests.get(link)
            soup_content = BeautifulSoup(response.text, 'html.parser')
            text = soup_content.get_text()
        else:
            text = "No content available"
        
        data.append({
            "title": title,
            "text": text
        })
    
    return data[:num_posts]

# Example usage
if __name__ == "__main__":
    num_posts = 10
    hackernews_data = scrape_hackernews(num_posts)
    print(hackernews_data)
