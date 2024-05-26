from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import HttpResponse  # Xatolik bo'lganda bizga ko'rsatish uchun kerak bo'ladi
from django.contrib.auth import authenticate, login, logout  # Tayyor foydalanuvchini tekshirish uchun kerak
from django.contrib.auth.forms import UserCreationForm  # foydalanuvchini yaratish formasi
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from django.views.generic import CreateView, View, ListView  # Foydalanuvchini viewni yuklab olamiz generic dan
from django.urls import reverse_lazy
from .models import Profile
from news_app.models import News


# Create your views here.

def user_login(request):
    if request.method == "POST":  # bu yerda ma'lumotlar post bo'lsa ishlaydi
        form = LoginForm(request.POST)  # loginformdangi ma'lumotni formga yuklaymiz
        if form.is_valid():  # form bo'sh bo'lmasliki kerak
            data = form.cleaned_data  # form.cleaned_data oraqali form ichidagi ma'lumotlarni data ga yuklaymiz
            print(data)  # bu test uchun edi chunki ma'lumotlarni qabul qilishini teshira yotgandik
            user = authenticate(request,
                                username=data['username'],
                                password=data['password'])
            # print(user)
            # foydalanuvchini ma'lumotlarni authenticate ni teshiramiz ya'ni sqldan ma'lumotlan
            # bilan teng bo'lsa kirishi mumkin bo'ladi
            if user is not None:  # foydalanuvchi bo'lsa ishlaydi
                if user.is_active:  # va foydalanuvchi active bo'lishi kerak ya'ni admin panelda foydalanuvchini adcounti unactive bo'lmasligi kerak
                    login(request, user)
                    return HttpResponse('Muffaqiyatli login amalga oshirildi')
                else:
                    return HttpResponse('Sizning profilingiz faol holatda emas')
            else:
                return HttpResponse('Login va parolda xatolik bor!')
        else:
            return HttpResponse("Iltimos barcha ma'lumotlarni kiriting")
    else:
        form = LoginForm()
        context = {
            'form': form
        }
    return render(request, 'registration/login.html', context)


@login_required
def dashboard_view(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    print(profile)
    context = {
        "user": user,
        "profile": profile
    }
    return render(request, 'pages/user_profile.html', context)


def user_register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(
                user_form.cleaned_data['password']
            )
            new_user.save()
            Profile.objects.create(user=new_user)
            context = {
                'news_user': new_user
            }
            return render(request, 'account/register_done.html', context)
    else:
        user_form = UserRegistrationForm()
        context = {
            'user_form': user_form
        }
        return render(request, 'account/register.html', context)


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy(
        'login')  # kommetga olingani sabab Profile modeli bilan birgan chiqarmoqchimiz Signup view ni
    template_name = "account/register.html"


@login_required
def edit_user(request):
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user,
                                 # instance bu yerada ayni qaysi userni ma'lumotini edit qilishini so'raydi bizlar bu yerda so'rov jo'natayotga user deyabmiz
                                 data=request.POST)  # bu yerda esa yuqorilayotgan ma'lumotni ayatamiz
        profile_form = ProfileEditForm(instance=request.user.profile,  # bu yerda ham shunda bo'ladi yuqoridagi dek
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('user_profile')
    else:  # bu yerda request get bo'lgani uchun ma'lumot bizga yuborilayotgani yoq faqat ma'lumotlarni ko'rishmoqchi
        user_form = UserEditForm(instance=request.user)  # bu yerda faqat ma'lumotlani ko'rishi mumkin bo'ladi
        profile_form = ProfileEditForm(
            instance=request.user.profile)  # bu yerda faqat ma'lumotarni ko'rish mumkin bo'ladi

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'account/profile_edit.html', context)


class EditUserView(LoginRequiredMixin, View):
    def get(self, request):
        user_form = UserEditForm(instance=request.user)  # bu yerda faqat ma'lumotlani ko'rishi mumkin bo'ladi
        profile_form = ProfileEditForm(
            instance=request.user.profile)  # bu yerda faqat ma'lumotarni ko'rish mumkin bo'ladi

        context = {
            'user_form': user_form,
            'profile_form': profile_form
        }
        return render(request, 'account/profile_edit.html', context)

    def post(self, request):
        user_form = UserEditForm(instance=request.user,
                                 # instance bu yerada ayni qaysi userni ma'lumotini edit qilishini so'raydi bizlar bu yerda so'rov jo'natayotga user deyabmiz
                                 data=request.POST)  # bu yerda esa yuqorilayotgan ma'lumotni ayatamiz
        profile_form = ProfileEditForm(instance=request.user.profile,  # bu yerda ham shunda bo'ladi yuqoridagi dek
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('user_profile')


@login_required
# super user ga dekarator yozib olamiz
@user_passes_test(lambda u:u.is_superuser)
def admin_page_view(request):
    admin_users = User.objects.filter(is_superuser=True)

    context = {
        'admin_users': admin_users
    }
    return render(request, 'pages/admin_page.html', context)

class SearchResultsList(ListView):
    model = News
    template_name = 'news/search_result.html'
    context_object_name = 'barcha_yangiliklar'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return News.objects.filter(
            Q(title__icontains=query) | Q(body__icontains=query)

        )

