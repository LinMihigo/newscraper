from django.shortcuts import render,redirect
from .scraper import scrape_newtimes



def search_articles(request):
    query = request.GET.get('query', '')
    results = []
    if query:
        results = scrape_newtimes(query)
    return render(request, 'search_results.html', {'query': query, 'results': results})

def home(request):
    return redirect('search_articles')