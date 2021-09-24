from django.shortcuts import render, get_object_or_404, HttpResponse, HttpResponseRedirect
from .models import Post, Profile
from .forms import EmailForm, PostForm, CommentForm, UserRegistrationForm, ProfileEditForm, UserEditForm
import smtplib
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Изменения сохранены")
        else:
            messages.error(request, "Ошибка при редактировании профиля")
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'account/edit.html', {'user_form': user_form, 'profile_form': profile_form})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Создаем нового пользователя, но пока не сохраняем в базу данных.
            new_user = user_form.save(commit=False)
            # Задаем пользователю зашифрованный пароль.
            new_user.set_password(user_form.cleaned_data['pas1'])
            # Создание профиля пользователя.
            Profile.objects.create(user=new_user)
            # Сохраняем пользователя в базе данных.
            new_user.save()
            password = request.POST.get("pas1")
            email = request.POST.get("email")
            smtpObj = smtplib.SMTP('smtp.mail.ru', 587)
            smtpObj.starttls()
            smtpObj.login('test.django@inbox.ru', '123098qazxsw')
            smtpObj.sendmail("test.django@inbox.ru", email, str("Ваш пароль для сайта {0} ".format(password)))
            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
        return render(request, 'account/register.html', {'user_form': user_form})


@login_required
def dashboard(request):
    return render(request, 'registration/dashboard.html', {'section': 'dashboard'})


# Обработчик классов
class PostListView(ListView):
    queryset = Post.objects.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


def email_message(request):
    emailform = EmailForm()
    if request.method == 'POST':
        new = EmailForm(request.POST)
        if new.is_valid():
            new.save()
            message = request.POST.get("text")
            email = request.POST.get("email")
            name = request.POST.get("name")
            smtpObj = smtplib.SMTP('smtp.mail.ru', 587)
            smtpObj.starttls()
            smtpObj.login('test.django@inbox.ru', '123098qazxsw')
            smtpObj.sendmail("test.django@inbox.ru", email, str("От {0} \n {1}".format(name, message)))

            return render(request, 'blog/post/done.html')
    else:

        return render(request, 'blog/post/email.html', {'form': emailform})


def post_list(request):
    object_list = Post.objects.all()
    paginator = Paginator(object_list, 4)  # По 4 статьи на страницу
    page = request.GET.get('page')  # Указание на текущую страницу
    try:
        posts = paginator.page(
            page)  # получаем список объектов на нужной странице с помощью метода page() класса Paginator
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/post/list.html', {'page': page, 'posts': posts})



def post_detail(request, year, month, title, post):
    post = get_object_or_404(Post, slug=post, title=title, publish__year=year,
                             publish__month=month)
    # Созхдание активных комментариев для статьи
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        # Пользователь отправил комментарий
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)  # Создаем комментарий, но пока не сохраняем в базе данных.
            new_comment.post = post  # Привязываем комментарий к текущей статье.
            new_comment.save()  # Сохраняем комментарий в базе данных.
    else:
        comment_form = CommentForm()
    return render(request, 'blog/post/detail.html', {'post': post,
                                                     'comments': comments,
                                                     'new_comment': new_comment,
                                                     'comment_form': comment_form})


def past_form(request):
    form = PostForm()
    return render(request, 'blog/post/done.html', {'form': form})
