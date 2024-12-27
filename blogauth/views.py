import string
import random
from django.http.response import JsonResponse
from django.shortcuts import render, redirect, reverse,HttpResponse
from django.core.mail import send_mail
from .models import CaptchaModel
from django.views.decorators.http import require_http_methods
from .formers import RegisterForm, LoginForm
from django.contrib.auth import get_user_model, login,logout

User = get_user_model()


# Create your views here.
@require_http_methods(['GET', 'POST'])
def mylogin(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            remember = form.cleaned_data.get('remember')
            user = User.objects.filter(email=email).first()
            # print(user)
            # print(user.check_password(password))
            if user and user.check_password(password):

                # 登录
                login(request, user)
                # 判断是否需要记住我
                if not remember:
                    # 如果没有点击记住我，那么就要设置过期时间为0，即浏览器关闭后就会过期
                    request.session.set_expiry(0)
                # 如果点击了，那么就什么都不做，使用默认的2周的过期时间
                return redirect('/')
            else:
                return redirect(reverse('blogauth:login'))
        else:
            print('邮箱或密码错误！')
            # form.add_error('email', '邮箱或者密码错误！')
            # return render(request, 'login.html', context={"form": form})
            return redirect(reverse('blogauth:login'))
        # else:
        #     return redirect(reverse('blogauth:login'))


@require_http_methods(['GET', 'POST'])
def register(request):
    if request.method == 'GET':
        return render(request, template_name='register.html')
    else:
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            User.objects.create_user(username=username, email=email, password=password)
            return redirect(reverse('blog:index'))
        else:
            print(form.errors)
            return redirect(reverse('blogauth:register'))
            # re


def send_email_captcha(request):
    email = request.GET.get('email')
    if not email:
        return JsonResponse({'code': 400, 'msg': '必须填入邮箱！'})
    captcha = "".join(random.sample(string.digits, 4))
    CaptchaModel.objects.update_or_create(email=email, defaults={'captcha': captcha})
    send_mail("我的博客注册验证码", message=f'注册验证码为{captcha}', recipient_list=[email], from_email=None)

    return JsonResponse({'code': 200, 'msg': '邮箱验证码发送成功！'})

def mylogout(request):
    logout(request)
    return redirect('/')