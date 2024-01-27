from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView, ListView, DetailView

from apps.forms import RegisterForm, LoginForm, EmailForm
from apps.mixins import NotLoginRequiredMixin
from apps.models import Blog, Category


class MainPageView(TemplateView):
    template_name = 'apps/index.html'


class RegisterView(FormView):
    template_name = 'apps/login-register.html'
    form_class = RegisterForm
    success_url = 'register'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class LoginPageView(NotLoginRequiredMixin, FormView):
    template_name = 'apps/login-register.html'
    form_class = LoginForm
    success_url = reverse_lazy('main_page')

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, username=username, password=password)
        print(user)
        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            form.add_error(None, "Invalid username or password")
            return self.form_invalid(form)


class BlogListView(ListView):
    template_name = 'apps/blogs/blog-list.html'
    queryset = Blog.objects.order_by('-created_at')
    context_object_name = 'blogs'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        if search := self.request.GET.get("search"):
            return queryset.filter(name__icontains=search)
        return queryset


class BlogDetailView(DetailView):
    template_name = 'apps/blogs/blog-details-left-sidebar.html'
    queryset = Blog.objects.all()
    context_object_name = 'blog'
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_blogs'] = self.get_queryset()[:3]
        context['categories'] = Category.objects.all()
        return context


class EmailView(FormView):
    template_name = 'apps/base.html'
    form_class = EmailForm
    success_url = '.'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return redirect('.', self.get_context_data(form=form))
