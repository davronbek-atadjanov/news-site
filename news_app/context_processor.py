from .models import News,Category

def latest_news(request):
    latest_news = News.published.all().order_by('-publish_time')[:10]

    context = {
        'latest_news':latest_news,
        'categories': Category.objects.all()
    }
    return context