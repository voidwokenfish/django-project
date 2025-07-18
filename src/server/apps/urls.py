from django.urls import include, path

from server.apps.courses.urls import urlpatterns as courses_urls
from server.apps.mailing.urls import urlpatterns as mailing_urls
from server.apps.quizzes.urls import urlpatterns as quizzes_urls
from server.apps.transactions.urls import urlpatterns as transactions_urls
from server.apps.users.urls import urlpatterns as users_urls

urlpatterns = [
    path('', include(courses_urls)),
    path('', include(users_urls)),
    path('', include(quizzes_urls)),
    path('', include((mailing_urls, "server.apps.mailing",), namespace='mailing')),
    path('', include(transactions_urls)),
]
