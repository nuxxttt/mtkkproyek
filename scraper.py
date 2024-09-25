import requests
from bs4 import BeautifulSoup
import time

def scrape_major_data(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    
    # Send a GET request to the URL with headers
    response = requests.get(url, headers=headers)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find university name
        university_name = soup.find('a', class_='panel-title').get_text(strip=True)
        
        # Find all table rows
        rows = soup.find_all('tr')
        
        # Initialize an empty list to store the scraped data
        major_data = []
        
        # Iterate over each row, skipping the header row
        for row in rows[1:]:
            # Extract relevant data from the row
            cells = row.find_all('td')

            # Check if the row has enough cells
            if len(cells) >= 6:
                major_name = cells[2].get_text().strip()  # Adjusted indexing here
                
                # Check if the major name matches "HUKUM"
                if major_name == "ILMU HUKUM":
                    applicants = int(cells[5].get_text().strip().replace('.', ''))
                    available_seats = int(cells[4].get_text().strip())
                    
                    # Calculate the ratio of applicants to available seats
                    ratio = applicants / available_seats
                    
                    # Append the extracted data to the list
                    major_data.append({
                        'University': university_name,
                        'Major': major_name,
                        'Ratio': ratio
                    })
        print(major_data)
        return major_data
    
    else:
        print("Failed to retrieve data. Status code:", response.status_code)
        return None


def scrape_ptn_data():
    url = "https://sidata-ptn-snpmb.bppp.kemdikbud.go.id/ptn_sb.php"
    
    # Send a GET request to the URL
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    
    response = requests.get(url, headers=headers)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all table rows
        rows = soup.find_all('tr')
        
        # Initialize an empty list to store the scraped data
        scraped_data = []
        
        # Iterate over each row, skipping the first one as it contains headers
        for row in rows[1:]:
            # Extract relevant data from the row
            cells = row.find_all('td')
            ptn_rank = cells[0].get_text().strip()
            ptn_id = cells[1].a['href'].split('=')[-1]
            ptn_name = cells[2].a.get_text().strip()
            ptn_website = cells[2].a['href']
            
            # Scrape major data for the university
            major_url = f"https://sidata-ptn-snpmb.bppp.kemdikbud.go.id/ptn_sb.php?ptn={ptn_id}"
            major_data = scrape_major_data(major_url)
            
            # Append the extracted data to the list
            scraped_data.append({
                'Rank': ptn_rank,
                'ID': ptn_id,
                'Name': ptn_name,
                'Website': ptn_website,
                'MajorData': major_data
            })
            
            # Delay between requests to avoid being blocked
            time.sleep(1)
        
        return scraped_data
    
    else:
        print("Failed to retrieve data. Status code:", response.status_code)
        return None

# Test the function
result = scrape_ptn_data()
if result:
    for data in result:
        print("University:", data['Name'])
        print("Website:", data['Website'])
        print("Major Data:")
        for major in data['MajorData']:
            print("\tMajor:", major['Major'])
            print("\tRatio (Applicants/Seats):", major['Ratio'])
        print()
