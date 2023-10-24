import requests
import json
import logging
from bs4 import BeautifulSoup

import os, django

logging.basicConfig(filename='app.log', filemode='a', format='%(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# 127.0.0.1:8000/scrap/quotes.toscrape.com+quotes.toscrape.com_login+admin+admin

def scrapper(url):
    
    url = url.split('+')
    print(f'SPLITTED URL: {url}')
    try:
        login_url = 'http://' + url[1] # quotes.toscrape.com/login
        login_url = login_url.replace('_', '/')
        login_data = {'username': url[2], 'password': url[3]}
    except:
        login_url = ''
        login_data = ''

    start_url = url[0]
    url = start_url

    with requests.Session() as session:
        if login_url and login_data:
            login(session, login_url, login_data)

        logging.info(f'PAGINATION INIT')
        quotes_data = []
        author_data = []

        while True:
            quotes, authors = fetch_content(session, url, start_url)
            if quotes:
                quotes_data.extend(quotes)
            if authors:
                author_data.extend(authors)

            response = session.get(url)
            soup = BeautifulSoup(response.text, 'lxml')

            next_page = soup.find('li', class_='next')
            logging.info(f'LOOKING FOR NEXT PAGE: {next_page}')
            if not next_page:
                logging.info('NEXT PAGE NOT FOUND!')
                break
            next_url = next_page.a['href']
            url = f'{start_url}{next_url}'
            logging.info(f'TAKING NEW URL: {url}')
            print(f'TAKING NEW URL: {url}')

        logging.info(f'FINAL QUOTES: {quotes_data}')
        logging.info(f'FINAL AUTHORS: {author_data}')

        quotes_prep_data = [json.loads(t) for t in {json.dumps(q, sort_keys=True) for q in quotes_data}]
        author_prep_data = [json.loads(t) for t in {json.dumps(a, sort_keys=True) for a in author_data}]

        from authorsapp.models import Author

        for record in author_prep_data:
            fullname = record['fullname']
            born_date = record['born_date']
            description = record['description']
            born_location = record['born_location']
            user_id = 1
            try:
                goodreads_url = record['goodreads_url']
            except:
                goodreads_url = None

            if not Author.objects.filter(fullname=fullname):
                author = Author(fullname=fullname, born_date=born_date, description=description, born_location=born_location, 
                                               goodreads_url=goodreads_url, user_id=user_id)
                author.save()

        logging.info('WRITING AUTHORS DONE')

        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quotes.settings')
        django.setup()
        from quotesapp.models import Tag, Quote

        for record in quotes_prep_data:
            quote = record['quote']
            print(f'QUOTE: {quote}')
            tags = record['tags']
            print(f'RAW TAGS: {tags}')
            author = record['author']
            print(f'GOT AUTHOR: {author}')

            tags_to_add = []
            for tag_data in tags:
                print(f'TAG DATA NAME: {tag_data}')
                tag, created = Tag.objects.get_or_create(name=tag_data)
                tags_to_add.append(tag)
            print(f'TAGS TO ADD: {tags_to_add}') 
            print(f'LOOKING FOR: {record["author"]}')
            
            local_author_id = Author.objects.filter(fullname=author)
            for item in local_author_id:
                local_author_id = item

            if local_author_id:
                author = local_author_id
            else:
                fullname = author
                born_date = ''
                description = ''
                born_location = ''
                user_id = 1
                goodreads_url = ''

                author = Author.objects.create(fullname=fullname, born_date=born_date, description=description, born_location=born_location, 
                                               goodreads_url=goodreads_url, user_id=user_id)
                author.save()

            if not Quote.objects.filter(quote=quote, author=author):
                new_quote = Quote.objects.create(quote=record['quote'], author=author)
                new_quote.save()

                for tag in tags_to_add:
                    print(f'ADDING TAG: {tag}')
                    new_quote.tags.add(tag)

            

def login(session, login_url, login_data):
    logging.info('TRYING TO LOG IN')
    response = session.post(login_url, data=login_data)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')
        is_logged = soup.select_one('a[href^="http://goodreads.com"]')
        logging.info(f'IF LOGIN SUCCESSFUL: {is_logged}')

def fetch_author(session, url, meta):
    logging.info(f'START FETCHING AUTHOR LINK: {url}')
    response = session.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')

        data = {'fullname': soup.find('h3', class_='author-title').text,
                'born_date': soup.find('span', class_='author-born-date').text,
                'born_location': soup.find('span', class_='author-born-location').text,
                'description': soup.find('div', class_='author-description').text.strip(),
                'goodreads_url': meta}
        
        logging.info(f'FETCHED AN AUTHOR: {data}')
        return data

def fetch_content(session, url, start_url):
    logging.info(f'START FETCHING: {url}')
    response = session.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')
        logging.info(f'INITIAL FETCH: {soup}')
        quotes = soup.find_all('span', class_='text')
        authors = soup.find_all('small', class_='author')
        tags = soup.find_all('div', class_='tags')
        author_pages = soup.select('a[href^="/author/"]')
        hrefs = [result['href'] for result in author_pages]
        externals = soup.select('a[href^="http://goodreads.com"]', class_='text')
        external_urls = [result['href'] for result in externals]
        author_data = []
        quotes_data = []

        for i in range(0, len(quotes)):
            quote = quotes[i].text
            author = authors[i].text
            tags_prep_quote = tags[i].find_all('a', class_='tag')
            tags_quote = []

            for tag in tags_prep_quote:
                tags_quote.append(tag.text)

            data = {
                "tags": tags_quote,
                "author": author,
                "quote": quote
            }

            logging.info(f'FETCHED A QUOTE: {data}')

            quotes_data.append(data)

            href = hrefs[i]
            logging.info(f'FETCHED THIS HREF: {href}')
            author_url = start_url + href

            meta = external_urls[i]
            logging.info(f'FETCHED THIS AUTHOR LINK: {author_url}, META = {meta}')
            author_data.append(fetch_author(session, url=author_url, meta=meta))

        logging.info(f'GOT QUOTES: {quotes_data}')
        logging.info(f'GOT AUTHORS: {author_data}')

        return tuple(quotes_data), tuple(author_data)