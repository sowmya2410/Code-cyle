import requests
from bs4 import BeautifulSoup
import re
import csv

# Step 1: Fetch the content from the URL
url = 'https://www.wikihow.com/Special:Randomizer'
response = requests.get(url)

# Step 2: Parse the HTML content with BeautifulSoup
html_content = response.content
soup = BeautifulSoup(html_content, 'html.parser')

# Extract the article title
article_title = soup.find('title').text.strip()
print(f"Article Title: {article_title}")

# Step 3: Extract subheadings and paragraphs
subheadings = []
paragraphs = []

steps = soup.find_all('div', {'class': 'step'})

for step in steps:
    subheading_element = step.find('b')
    
    if subheading_element is not None:
        subheading_text = subheading_element.text.strip().replace('\n', '')
        subheading_text = subheading_text.encode('ascii', errors='ignore').decode()
        subheading_text = re.sub(r'\s+', ' ', subheading_text)  # Replacing multiple spaces with a single space
        print(subheading_text)
        subheadings.append(subheading_text)
        
        # Remove the subheading element after extraction
        subheading_element.extract()
        
    # Remove span tags from the paragraph
    for span_tag in step.find_all('span'):
        span_tag.extract()

    # Extract and clean the paragraph text
    paragraph_text = step.text.strip().replace('\n', '').replace('  ', ' ')
    paragraph_text = paragraph_text.encode('ascii', errors='ignore').decode()
    paragraph_text = re.sub(r'\s+', ' ', paragraph_text)  # Replacing multiple spaces with a single space
    print(paragraph_text)
    paragraphs.append(paragraph_text)

# Step 4: Write subheadings and paragraphs to a CSV file
if len(subheadings):
    with open('wikiHow.csv', mode='a', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        for i in range(len(subheadings)):
            writer.writerow([article_title, subheadings[i], paragraphs[i]])  # Include the article title

