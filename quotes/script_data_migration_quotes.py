import os
import django
from pymongo import MongoClient

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quotes.settings')
django.setup()

from quotesapp.models import Tag, Quote
from authorsapp.models import Author

# Подключение к MongoDB
mongo_client = MongoClient('mongodb+srv://amarakheo:AYwoHw8KHtGl9rgx@cluster0.wun00kb.mongodb.net/?retryWrites=true&w=majority')
mongo_db = mongo_client['library_app']
mongo_collection = mongo_db['quote']
mongo_authors = mongo_db['author']

# Извлечение данных из MongoDB и загрузка их в PostgreSQL
for record in mongo_collection.find():
    quote = record['quote']
    print(f'QUOTE: {quote}')
    tags = record['tags']
    print(f'RAW TAGS: {tags}')

    tags_to_add = []
    for tag_data in tags:
        tag, created = Tag.objects.get_or_create(name=tag_data['name'])
        tags_to_add.append(tag)
    print(f'TAGS TO ADD: {tags_to_add}')
    
    print(f'LOOKING FOR: {record["author"]}')
    author_from_mongo = mongo_authors.find_one({'_id': record['author']})
    print(f'AUTHOR: {author_from_mongo["fullname"]}')

    local_author_id = Author.objects.filter(fullname=author_from_mongo["fullname"])
    for item in local_author_id:
        local_author_id = item.id
    if local_author_id:
        author = Author.objects.get(id=local_author_id)
    else:
        author = Author.objects.create(fullname=author_from_mongo["fullname"], born_date=author_from_mongo['born_date'], born_location=author_from_mongo['born_location'], 
                                       description=author_from_mongo['description'], goodreads_url = author_from_mongo['goodreads_url'] if author_from_mongo['goodreads_url'] else None)
        author.save()


    new_quote = Quote.objects.create(quote=record['quote'], author=author)
    new_quote.save()

    for tag in tags_to_add:
        print(f'ADDING TAG: {tag}')
        new_quote.tags.add(tag)
