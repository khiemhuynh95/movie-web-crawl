import requests
from bs4 import BeautifulSoup
import json
import time

#def get_phim_bo_list():

import requests

def get_html_content(url):
    # Create a session object
    session = requests.Session()

    # Enable keep-alive
    headers = {'Connection': 'keep-alive'}

    # Set timeouts for connect and read operations
    timeout = (3, 5)  # 3 seconds for connect, 5 seconds for read

    # Set a User-Agent header
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    headers['User-Agent'] = user_agent

    # Use the session to make a request
    response = session.get(url, headers=headers, timeout=timeout)

    # Process the response
    return response.content


def parse_a_phim_link(url):
    # response = requests.get(url)
    html_content = get_html_content(url)
    soup = BeautifulSoup(html_content, 'html.parser')
    film_info_wrapper = soup.find('div', {'class': 'film-info'})
    link = film_info_wrapper.find('a').get('href')
    img_src = film_info_wrapper.find('img').get('src')
    return link, img_src

def get_all_phim_le_by_a_page(url):
    movies_list = {}
    
    try:
        html_content = get_html_content(url)

        soup = BeautifulSoup(html_content, 'html.parser')
        for element in soup.find_all('li', {'class': 'item small'}):
            a_tag = element.find('a', title=True)
            title = a_tag['title']
            link, img_src = parse_a_phim_link(a_tag['href'])
            movie = {
                'link': link,
                'img_src': img_src
            }
            movies_list[title] = movie
        return movies_list
    except requests.exceptions.RequestException as e:
        print(e)
        return {}

def write_results_to_json(results, filename):

    # Open the file for writing
    with open(filename, 'w') as json_file:
        # Write the dictionary to the file
        json.dump(results, json_file)


def get_all_phim_le_by_page_range(start, end):
    start_time = time.time()


    final_results = {}
    for i in range(start, end+1):
        movies_by_page = get_all_phim_le_by_a_page(f'https://phimmoichillc.net/list/phim-le/page-{i}')
        final_results.update(movies_by_page)
        print(f"MOVIES FOR PAGE {i}, count: {len(movies_by_page)}")
    
    print("Total movies: " + str(len(final_results)))
    end_time = time.time()
    execution_time = end_time - start_time
    print('Execution time: {} seconds'.format(execution_time))
    return final_results


def main():
    #for movie in get_all_phim_le_by_page_range(1,7):
    write_results_to_json(get_all_phim_le_by_page_range(1,7), "results.json")

if __name__ == '__main__':
    main()