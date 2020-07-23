from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.hashers import make_password
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import TemplateView, CreateView, UpdateView, ListView, View, FormView, DetailView, DeleteView
from .models import Blog
from .forms import Register_form, Loginform, BlogForm
from django.contrib import messages

User = get_user_model()


class Base(TemplateView):
    template_name = 'blog/base.html'


class Homepage(ListView):
    template_name = 'blog/home.html'
    queryset = Blog.objects.all()
    context_object_name = 'blog_list'


class Register(CreateView):
    template_name = 'blog/register.html'
    form_class = Register_form
    success_url = '/login'

    def form_valid(self, form):
        model = form.save(commit=False)
        model.is_active = False
        model.password = make_password(form.cleaned_data['password'])
        model.save()

        subject = 'User registration'
        from_email = 'admin@blog.com'
        recipient = form.cleaned_data['email']

        current_site = get_current_site(self.request)

        message = render_to_string('blog/activate.html', {
            'user': form.cleaned_data['first_name'],
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(form.cleaned_data['email']))
        })
        send_mail(subject, message, from_email, [recipient])
        messages.success(self.request, "check your mail")

        return super().form_valid(form)


class Login(FormView):
    template_name = 'blog/login.html'
    form_class = Loginform
    success_url = '/profile'

    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']

        user = authenticate(username=email, password=password)

        print("USer check", user, email, password)
        if user is not None:
            login(self.request, user)
            messages.success(self.request, "logged in successfully")
        else:
            messages.error(self.request, "invalid credentials")
            return redirect('/login')

        return super().form_valid(form)


class Profile(ListView):
    template_name = 'blog/profile.html'
    # queryset = Blog.objects.all()
    context_object_name = 'blogs'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            queryset = Blog.objects.filter(user=self.request.user)
        else:
            queryset = Blog.objects.none()
        return queryset

    # def get(self, request, *args, **kwargs):
    #     context = {
    #         'blogs': Blog.objects.allI()
    #     }
    #     return render(request, 'blog/profile.html', context=context)


class Profileupdate(UpdateView):
    model = User
    template_name = 'blog/update.html'
    form_class = Register_form
    success_url = '/profile'

    def form_valid(self, form):
        model = form.save(commit=False)
        model.password = make_password(form.cleaned_data['password'])

        print("password",form.cleaned_data)
        model.save()

        return super().form_valid(form)

class Activate(View):
    def get(self, request, uid):
        uids = urlsafe_base64_decode(uid).decode()
        user = User.objects.get(email=uids)
        if user is not None:
            user.is_active = True
            user.save()
            messages.success(self.request, "successful activated")
            return redirect('/login')


class Blogdetail(DetailView):
    model = Blog
    template_name = 'blog/blog-detail.html'
    context_object_name = 'blog'


class Createblog(CreateView):
    model = Blog
    form_class = BlogForm
    template_name = 'blog/create.html'
    success_url = '/profile'

    def form_valid(self, form):
        model = form.save(commit=False)
        model.user = self.request.user
        model.save()
        return super().form_valid(form)


class BlogEdit(UpdateView):
    model = Blog
    form_class = BlogForm
    template_name = 'blog/create.html'
    success_url = '/profile'


class BlogDelete(DeleteView):
    model = Blog
    success_url = '/profile'
