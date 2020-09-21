from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from .models import Question
from .serializer import QuestionSerializer
from bs4 import BeautifulSoup
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
import requests
from rest_framework.pagination import PageNumberPagination
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle,AnonRateThrottle
# Create your views here.

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 1000


class StackOverFlowQuestionAPI(viewsets.ModelViewSet):
    
    queryset = Question.objects.all()
    pagination_class =  StandardResultsSetPagination
    serializer_class = QuestionSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('id','question','vote_count','views','tags',)
    http_method_names = ['get']
    throttle_classes = [UserRateThrottle,AnonRateThrottle]

    @method_decorator(cache_page(60))
    @method_decorator(vary_on_cookie)

    def latest(self,request):
        try:
            res = requests.get("https://stackoverflow.com/questions")

            soup = BeautifulSoup(res.text, "html.parser")

            questions = soup.select(".question-summary")
            for que in questions:
                q = que.select_one('.question-hyperlink').getText()
                vote_count = que.select_one('.vote-count-post').getText()
                views = que.select_one('.views').attrs['title']
                tags = [i.getText() for i in (que.select('.post-tag'))]

                question = Question()
                question.question = q
                question.vote_count = vote_count
                question.views = views
                question.tags = tags

                question.save()
          
        except e as Exception:
            return Response({'status':False,
                             'message':'Something went wrong !',
                             'data':[]})


