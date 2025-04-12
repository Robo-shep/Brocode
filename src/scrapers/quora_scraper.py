import requests
from bs4 import BeautifulSoup

def scrape_quora(topic, num_posts):
    url = f"https://www.quora.com/topic/{topic}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    data = []
    for question in soup.find_all('div', class_='q-text'):
        title = question.text.strip()
        link = "https://www.quora.com" + question.find('a')['href']
        
        # Fetch the content of the linked page
        response = requests.get(link)
        soup_content = BeautifulSoup(response.text, 'html.parser')
        text = soup_content.get_text()
        
        data.append({
            "title": title,
            "text": text
        })
    
    return data[:num_posts]

# Example usage
if __name__ == "__main__":
    topic = "python-programming"
    num_posts = 10
    quora_data = scrape_quora(topic, num_posts)
    print(quora_data)
