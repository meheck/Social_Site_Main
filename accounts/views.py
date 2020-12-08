from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.models import User
from django.views.generic import TemplateView,CreateView, DetailView, RedirectView
from accounts.forms import UserCreateForm
from django.urls import reverse_lazy,reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile
from django.db.models import Q
# Create your views here.


class HomePage(TemplateView):
    template_name='index.html'


class SignUp(CreateView):
    form_class=UserCreateForm
    success_url=reverse_lazy('login')
    template_name='accounts/signup.html'

class CreateProfile(LoginRequiredMixin,CreateView):
    model = Profile
    fields = ('contact','gender','profile_pic')
    template_name = 'Profile/profile_form.html'

    def form_valid(self, form):
        if Profile.objects.filter(user = self.request.user).exists():
            return redirect('accounts:profile', username=self.request.user.username,pk=Profile.objects.filter(user = self.request.user)[0].pk)
        profile = form.save(commit=False)
        profile.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        username = self.kwargs.get('username')
        pk = self.object.pk
        return reverse_lazy('accounts:profile', kwargs={'username':username,'pk':pk})

class DetailProfile(LoginRequiredMixin,DetailView):
    model = Profile
    template_name = 'Profile/profile_detail.html'

def VerifyProfile(request, username):
    try:
        profile = Profile.objects.get(user__username=username)
    except:
        return redirect('accounts:createprofile', username=username)
    return redirect('accounts:profile', username=username,pk=profile.pk)

class FollowToggle(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            slug = self.kwargs.get("slug")
            print (slug)
            profile_instance = get_object_or_404(Profile, slug=slug)
            url_ = profile_instance.get_absolute_url()
            user_ = get_object_or_404(Profile, user=self.request.user)
            if profile_instance.user in user_.followers.all():
                user_.followers.remove(profile_instance.user)
            else:
                user_.followers.add(profile_instance.user)
            print (user_.user)
            print (user_.followers.all())
            return url_
        else:
            return "/login"

def search(request):
    #model=Profile
    #template_name= 'search/search_profiles.html'
    if (request.user.is_authenticated):
        query = request.GET.get("search")
        user_ = get_object_or_404(Profile, user=request.user)
        print (query)
        query_list = None
        if query:
            query_list = Profile.objects.filter(
                Q(user__username__icontains=query) |
                #Q(interests__icontains=query) |
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query)
            ).distinct()
        print (query_list)
        context = {
            'users': query_list,
            'user_': user_,
            'all_users': Profile.objects.all(),
        }

        return render(request, "search/search_profiles.html", context)
    else:
        return redirect("login")
