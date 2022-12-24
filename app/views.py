from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, HttpResponse
from .models import Networker, Profile, DepositPaymentMethod, WithdrawalRequest
from .form import SignupForm, LoginForm, ProfileForm, form_validation_error,\
    DepositConfirmationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView, DetailView, CreateView
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormMixin, ModelFormMixin
from django.urls import reverse


# Create your views here.

# -------------------------------
#                                |
#           Signup View
#                                |
# -------------------------------

@csrf_protect
def signup_view(request):
    profile_id = request.session.get('ref_profile')
    print('profile_id', profile_id)
    form = SignupForm(request.POST or None)
    if form.is_valid():
        if profile_id is not None:
            recommended_by_profile = Networker.objects.get(id=profile_id)

            instance = form.save()
            registered_user = User.objects.get(id=instance.id)
            registered_profile = Networker.objects.get(user=registered_user)
            registered_profile.recommended_by = recommended_by_profile.user
            registered_profile.save()
        else:
            form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('crypto')
    context = {
        'form': form
    }
    return render(request, 'profile/signup/register.html', context)


def check_username(request):
    username = request.POST.get('username')
    if get_user_model().objects.filter(username=username).exists():
        return HttpResponse("This user already exists")
    else:
        return HttpResponse("This username is available")


@csrf_protect
def login_view(request):
    form = LoginForm(request.POST or None)
    context = {"form": form}
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect("/crypto/")
            else:
                messages.error(request, 'Your account is not active yet.')
                return render(request, 'profile/signup/login.html', context)
        else:
            print("Invalid login details: {0}, {1}".format(username, password))
            messages.error(request, 'Username or Password is not correct.')
            return render(request, 'profile/signup/login.html', context)
    else:
        return render(request, 'profile/signup/login.html', context)


@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/')


# -------------------------------
#                                |
#           Main HomePage View
#                                |
# -------------------------------
def main_view(request, *args, **kwargs):
    code = str(kwargs.get('ref_code'))
    try:
        profile = Networker.objects.get(code=code)
        request.session['ref_profile'] = profile.id
        print('id', profile.id)
    except:
        pass
    # print(request.session.get_expiry_date())
    return render(request, 'index/index.html')


# -------------------------------
#                                |
#     Dashboard View - Referral
#                                |
# -------------------------------
def my_recommendations_view(request):
    total_network = Networker.objects.all()
    print('------------Total Parents **************')
    all_parents = []
    for parent in total_network:
        if parent.recommended_by is None:
            print(all_parents.append(parent))
            print(parent)
    print(all_parents)
    print('------------Total Network* *************')
    print(total_network)
    # all_parent_profile = Profile.objects.get(user=user)
    profile = Networker.objects.get(user=request.user)
    print("--------------Current Profile--------------")
    print(profile)
    my_recs =  profile.get_recommended_profiles()
    context = {
        'my_recs': my_recs,
        'parents': all_parents,
    }
    print('---------------ALl Recommendations------------------')
    print(context)
    return render(request, 'index/recommendations.html', context)


# -------------------------------
#                                |
#     Dashboard View - Profile Update
#                                |
# -------------------------------
@method_decorator(login_required(login_url='/signin/'), name='dispatch')
class ProfileView(View):
    profile = None

    def dispatch(self, request, *args, **kwargs):
        self.profile, __ = Profile.objects.get_or_create(user=request.user)
        return super(ProfileView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        context = {'profile': self.profile, 'segment': 'profile'}
        return render(request, 'profile/dashboard/author-profile.html', context)

    def post(self, request):
        form = ProfileForm(request.POST, request.FILES, instance=self.profile)

        if form.is_valid():
            profile = form.save()
            profile.user.first_name = form.cleaned_data.get('first_name')
            profile.user.last_name = form.cleaned_data.get('last_name')
            profile.user.email = form.cleaned_data.get('email')
            profile.user.save()

            messages.success(request, 'Profile saved successfully')
        else:
            messages.error(request, form_validation_error(form))
        return redirect('profile')


@login_required(login_url='/signin/')
def dashboard(request):
    return render(request, 'profile/dashboard/index.html')


@login_required(login_url='/signin/')
def cryptocurrency(request):
    return render(request, 'profile/dashboard/index-crypto.html')


# -------------------------------
#                                |
#     Deposit View
#                                |
# -------------------------------
# @login_required(login_url='/signin/')
class DepositPaymentMethodView(ListView):
    model = DepositPaymentMethod
    # paginate_by = 6
    # template_name = 'profile/dashboard/testprofile.html'
    template_name = 'profile/deposit/pricing.html'


class DepositPaymentMethodDetailView(ModelFormMixin, DetailView):
    model = DepositPaymentMethod
    template_name = 'profile/deposit/dtest.html'
    form_class = DepositConfirmationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        self.object = self.get_object()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('deposit-payment-method-detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.investor_user_name = self.request.user
        self.object.save()
        return super(ModelFormMixin, self).form_valid(form)


@login_required(login_url='/signin/')
def deposit_confirmation_view(request):
    form = DepositConfirmationForm(request.POST or None)
    context = {
        'form': form
    }
    if form.is_valid():
        confirm = form.save(commit=False)
        confirm.investor_user_name = request.user
        confirm.save()
        messages.success(request, 'Confirmation Send')
        return redirect(deposit_confirmation_view)
    return render(request, 'profile/deposit/dconfi.html', context)


class WithdrawalRequestView(LoginRequiredMixin, CreateView):
    model = WithdrawalRequest
    fields = ['amount', 'currency_selected', 'currency_address',]
    template_name = 'profile/withdrawal/withdrawal-request.html'

    def form_valid(self, form):
        form.instance.investor_user_name = self.request.user
        return super().form_valid(form)


