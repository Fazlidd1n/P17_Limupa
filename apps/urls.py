from django.conf import urls
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import path

from apps.tasks import task_send_email
from apps.views import MainPageView, RegisterView, LoginPageView, BlogListView, BlogDetailView, EmailView
from root.settings import MEDIA_ROOT, MEDIA_URL

# def custom_view(request, email):
#     # response = task_send_email.delay('Temasi', 'xabari', ['aralovjavoxir@gmail.com'])
#     response = task_send_email('Temasi', 'xabari', ['aralovjavoxir@gmail.com'])
#     return JsonResponse({'status': 'success'})

urlpatterns = [
                  path('', MainPageView.as_view(), name='main_page'),
                  path('login-register', LoginPageView.as_view(), name='login_register'),
                  path('logout', LogoutView.as_view(next_page='main_page'), name='logout_register'),
                  path('register', RegisterView.as_view(), name='register'),
                  path('newslatters', EmailView.as_view(), name='newslatters'),
                  path('blog-list', BlogListView.as_view(), name='blog_list_page'),
                  path('blog-details-left/<uuid:pk>', BlogDetailView.as_view(), name='blog_details_left_sidebar_page'),

              ] + static(MEDIA_URL, document_root=MEDIA_ROOT)


def page_404(request, *args, **kwargs):
    return render(request, 'apps/404.html', status=404)


urls.handler404 = 'apps.urls.page_404'
