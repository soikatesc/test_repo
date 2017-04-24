from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$',views.index),
	url(r'^createUser$',views.createUser),
	url(r'^login$',views.login),
	url(r'^books$',views.books),
	url(r'^logout$',views.logout),
	url(r'^bookadd$',views.addingbookandreviews),
	url(r'^bookaddpost',views.addingbookandreviewspost),
	url(r'^booksprofile/(?P<bookid>\d+)',views.booksprofile),
	url(r'^books/(?P<bookid>\d+)',views.bookspost),
	url(r'^deletereview/(?P<reviewid>\d+)',views.deletereview),
	url(r'^deletereviewfromhome/(?P<reviewid>\d+)',views.deletereviewfromhome),
	url(r'^userprofile/(?P<userid>\d+)',views.userprofile),

]
