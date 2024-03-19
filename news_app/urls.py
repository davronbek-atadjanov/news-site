from django.urls import path
from .views import NewsListView,news_detail,HomePageView,ContactPageView,page404View,singlePageView, \
    LocalNewsView,ForeignNewsView,TechnologyNewsView,SportNewsView
urlpatterns = [
    path('',HomePageView.as_view(),name='home_page'),
    path('news/',NewsListView.as_view(), name='all_news_list'),
    path('news/<slug:news>/',news_detail,name='news_detail_page'),
    path('contact-us/',ContactPageView.as_view(),name='contact_page'),
    path('page-404/',page404View,name='page_404'),
    path('single-page/',singlePageView,name='single_page_view'),
    path('local/',LocalNewsView.as_view(),name='local_news_page'),
    path('foreign/',ForeignNewsView.as_view(),name='foreign_news_page'),
    path('technology/',TechnologyNewsView.as_view(),name='technology_news_page'),
    path('sport/',SportNewsView.as_view(),name='sport_news_page'),
]
