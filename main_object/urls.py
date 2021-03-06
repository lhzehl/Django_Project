from django.urls import path
from .views import MainObjectListView, MainObjectCreateView,\
    MainObjectDetailView, ReviewCreateView, AddValueRankView,\
    MainObjectUpdateView
from .views import ProfileListView, ProfileDetailView


urlpatterns = [
    path('object/', MainObjectListView.as_view()),
    path('object/<int:pk>/', MainObjectDetailView.as_view()),
    path('object/<int:pk>/update', MainObjectUpdateView.as_view()),
    path('new/', MainObjectCreateView.as_view()),
    path('review/', ReviewCreateView.as_view()),
    path('rank/', AddValueRankView.as_view()),
    path('users/', ProfileListView.as_view()),
    path('users/<int:pk>/', ProfileDetailView.as_view()),

]
