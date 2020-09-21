from django.urls import path, include
from .views import StackOverFlowQuestionAPI
from rest_framework import routers


router = routers.SimpleRouter()
router.register("questions", StackOverFlowQuestionAPI)

urlpatterns = [
    path('', include(router.urls)),
]
