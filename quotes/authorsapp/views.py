from django.shortcuts import render, redirect, get_object_or_404
from .forms import AuthorForm
from .models import Author

# Create your views here.
def author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            new_author = form.save(commit=False)
            new_author.user = request.user
            new_author.save()
            return redirect(to='quotesapp:main')
        else:
            return render(request, 'authorsapp/author.html', {'form': form})

    return render(request, 'authorsapp/author.html', {'form': AuthorForm()})


def detail(request, author_id):
    author = get_object_or_404(Author, pk=author_id)
    return render(request, 'authorsapp/author_detail.html', {"author": author})
