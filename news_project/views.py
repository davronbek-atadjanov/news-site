from django.shortcuts import render, get_object_or_404,HttpResponse
from hitcount.utils import get_hitcount_model
from hitcount.views import HitCountDetailView, HitCountMixin

from news_app.forms import ContactForm, CommentForm
from news_app.models import News, Category, Contact
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView,UpdateView,DeleteView,CreateView

from django.contrib.auth.mixins import LoginRequiredMixin
from news_project.custom_permissions import OnlyLoggedSuperUser
# Create your views here.

# def news_list(request):
#     # news_list = News.objects.filter(status=News.Status.Published)
#     news_list = News.published.all()
#     context = {
#         "news_list":news_list
#     }
#
#     return render(request, "news/news_list.html",context)

def news_detail(request,news):
    news = News.objects.get(slug=news,status=News.Status.Published)
    context = {}
    # hitcount logic
    hit_count = get_hitcount_model().objects.get_for_object(news)
    hits = hit_count.hits
    hitcontext=context['hitcount'] = {'pk': hit_count.pk}
    hit_count_response= HitCountMixin.hit_count(request, hit_count)
    if hit_count_response.hit_counted:
        hits = hits + 1
        hitcontext['hit_counted'] = hit_count_response.hit_counted
        hitcontext['hit_message'] = hit_count_response.hit_message
        hitcontext['total_hits'] = hits


    comments = news.comments.filter(active=True)
    comment_count = comments.count()
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # yangi comment objectni yaratamiz lekin db ga saqlamaymiz
            news_comment = comment_form.save(commit=False)
            news_comment.news = news
            # comment izoh egasini so'rov yuborayotgan userga bog'ladik
            news_comment.user = request.user
            # ma'lumotlar bazasiga saqlaymiz
            news_comment.save()
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()
    context = {
        'news':news,
        'comments':comments,
        'new_comment':new_comment,
        'comment_form':comment_form,
        'comment_count':comment_count
    }
    return render(request, 'news/news_detail.html',context)

# # Clas ga o'tirish kerak bo'lgan qism

# class NewsDetailView(DetailView):
#
#     def __init__(self,news):
#         super().__init__(news)
#     ef get
#     def get(self):
#         comment_form = CommentForm()
#     def post(self):
#         comment_form = CommentForm()
#         if comment_form.is_valid():
#             # yangi comment objectni yaratamiz lekin db ga saqlamaymiz
#             news_comment = comment_form.save(commit=False)
#             news_comment.news = news
#             # comment izoh egasini so'rov yuborayotgan userga bog'ladik
#             news_comment.user = user
#             # ma'lumotlar bazasiga saqlaymiz
#             news_comment.save()
#             comment_form = CommentForm()
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

class NewsUpdateView(OnlyLoggedSuperUser,UpdateView):
    model = News
    fields=('title','body','image','category','status')
    template_name='news/crud/news_edit.html'

class NewsDeleteView(OnlyLoggedSuperUser,DeleteView):
    model = News
    template_name = 'news/crud/news_delete.html'
    success_url = reverse_lazy('home_page')

class NewsCreateView(OnlyLoggedSuperUser,CreateView):
    model = News
    template_name = 'news/crud/news_create.html'
    fields = ('title', 'title_uz', 'title_en', 'title_ru' ,'slug','body', 'body_uz', 'body_en','body_ru' ,'image','category','status')
    
