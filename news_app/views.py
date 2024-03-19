from django.shortcuts import render, get_object_or_404,HttpResponse

from .forms import ContactForm
from .models import News, Category, Contact
from django.views.generic import ListView, DetailView, TemplateView,UpdateView,DeleteView,CreateView


# Create your views here.

# def news_list(request):
#     # news_list = News.objects.filter(status=News.Status.Published)
#     news_list = News.published.all()
#     context = {
#         "news_list":news_list
#     }
#
#     return render(request, "news/news_list.html",context)
def news_detail(reqeust,news):
    news = News.objects.get(slug=news,status=News.Status.Published)
    context = {
        'news':news
    }
    return render(reqeust, 'news/news_detail.html',context)

class NewsListView(ListView):
    model = News
    template_name = 'news/news_list.html'
    context_object_name = 'news_list'


# class NewsDetailView(DetailView):
#     model = News
#     template_name = 'news/news_detail.html'
#     context_object_name = 'news'

def homePageView(request):
    news_list = News.published.all().order_by('-publish_time')[:10]
    categories = Category.objects.all()
    local_one = News.published.filter(category__name='Mahalliy').order_by('-publish_time')[:1]
    local_news = News.published.all().filter(category__name='Mahalliy').order_by('-publish_time')[1:6]

    context = {
        "news_list":news_list,
        "categories":categories,
        'local_news':local_news,
        'local_one':local_one
    }
    return render(request, 'news/index.html',context)

class HomePageView(ListView):
    model = News
    template_name = 'news/index.html'
    context_object_name = 'news'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['news_list'] = News.published.all().order_by('-publish_time')[:5]
        context['local_news'] = News.published.all().filter(category__name='Mahalliy').order_by('-publish_time')[:5]
        context['fashion_news'] = News.published.all().filter(category__name='Xorij').order_by('-publish_time')[:5]
        context['sport_news'] = News.published.all().filter(category__name='Sport').order_by('-publish_time')[:5]
        context['technology_news'] = News.published.all().filter(category__name='Texnologiya').order_by('-publish_time')[:5]
        return context

# # ContactPageView
# def contactPageView(request):
#     print(request.POST)
#     form = ContactForm(request.POST or None)
#     if request.method == 'POST' and form.is_valid():
#         form.save()
#         return HttpResponse("Biz bog'langaningiz uchun raxmat!")
#     context = {
#         "form":form
#     }
#     return render(request, 'news/contact.html',context)
#
#

class ContactPageView(TemplateView):
    template_name = 'news/contact.html'
    def get(selfs,request,*args,**kwargs):
        form = ContactForm()
        context = {
            'form':form
        }
        return render(request,'news/contact.html',context)
    def post(self,request,*args,**kwargs):
        form = ContactForm(request.POST or None)
        if request.method == 'POST' and form.is_valid():
            form.save()
            return HttpResponse("<h2>Biz bilan bo'glanganigiz uchun raxmat!")
        context = {
            'form':form
        }
        return render(request,'news/contact.html',context)

# # Page404View
def page404View(request):
    context = {
    }
    return render(request, 'news/404.html',context)

def singlePageView(request):
    context = {

    }
    return render(request, 'news/single_page.html',context)

# # LocalNewsView
class LocalNewsView(ListView):
    model = News
    template_name = 'news/mahalliy.html'
    context_object_name = 'mahalliy_yangiliklar'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name='Mahalliy')
        return news

class ForeignNewsView(ListView):
    model = News
    template_name = 'news/xorij.html'
    context_object_name = 'xorij_yangiliklar'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name='Xorij')
        return news

class TechnologyNewsView(ListView):
    model = News
    template_name = 'news/texnologiya.html'
    context_object_name = 'texnologiya_yangiliklar'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name='Texnologiya')
        return news

class SportNewsView(ListView):
    model = News
    template_name = 'news/sport.html'
    context_object_name = 'sport_yangiliklar'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name='Sport')
        return news

class NewsUpdateView(UpdateView):
    model = News
    fields=('title','body','image','category','status')
    template_name='crud/news_edit.html'

class NewsDeleteView(DeleteView):
    model = News
    template_name = 'crud/news_delete.html'


