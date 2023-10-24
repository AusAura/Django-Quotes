from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.core.paginator import Paginator
from django.http import HttpResponse

from .forms import QuoteForm, TagForm
from .models import Tag, Quote
from authorsapp.models import Author
from .scrapper import scrapper


# Create your views here.
def main(request):
    quotes = Quote.objects.all()
    paginator = Paginator(quotes, 10)  # Показывать 10 цитат на каждой странице
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    top_tags = Tag.objects.annotate(num_quotes=Count('quote')*10).order_by('-num_quotes')[:10]
    return render(request, 'quotesapp/index.html', {"quotes": quotes, "top_tags": top_tags, 'page_obj': page_obj})

@login_required
def quote(request):
    tags = Tag.objects.all()
    authors = Author.objects.all()

    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            new_quote = form.save(commit=False)
            new_quote.user = request.user

            authors = request.POST.get('authors')  # Предположим, что имя автора передается через форму
            author, _ = Author.objects.get_or_create(fullname=authors)
            new_quote.author = author
            new_quote.save()

            choice_tags = Tag.objects.filter(name__in=request.POST.getlist('tags'))
            for tag in choice_tags.iterator():
                new_quote.tags.add(tag)

            choice_authors = Author.objects.filter(fullname__in=request.POST.getlist('authors'))
            print(f"I GOT THIS AUTHORS: {choice_authors}")
            for author in choice_authors.iterator():
                new_quote.author = author

            return redirect(to='quotesapp:main')
        else:
            return render(request, 'quotesapp/quote.html', {"tags": tags, 'authors': authors, 'form': form})

    return render(request, 'quotesapp/quote.html', {"tags": tags, 'authors': authors, 'form': QuoteForm()})

@login_required
def tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            tag = form.save(commit=False)
            tag.user = request.user
            tag.save()
            return redirect(to='quotesapp:main')
        else:
            return render(request, 'quotesapp/tag.html', {'form': form})

    return render(request, 'quotesapp/tag.html', {'form': TagForm()})

def find_tag(request, tag_name):
    quotes = Quote.objects.filter(tags__name=tag_name)
    return render(request, 'quotesapp/find_tag.html', {"quotes": quotes, "tag_name": tag_name})

def scrap_view(request, url):
    if request.user.is_authenticated and request.user.is_superuser:
        url = 'https://' + url
        print(url)
        scrapper(url)
        return HttpResponse(f'Scrapped: {url}')
    else:
        return HttpResponse('Unauthorized', status=401)