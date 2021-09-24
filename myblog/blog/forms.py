from django import forms
from .models import Post, Email, Comment, User, Profile


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('data_of_birth', 'photo')


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class UserRegistrationForm(forms.ModelForm):
    pas1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    pas2 = forms.CharField(label='Повторите ваш пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_pas2(self):
        cd = self.cleaned_data
        if cd['pas1'] != cd['pas2']:
            raise forms.ValidationError("Пароли не совпадают")
        return cd['pas2']


class EmailForm(forms.ModelForm):
    class Meta:
        model = Email
        fields = ('email', 'name', 'text')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')


# class EmailForm(forms.Form):
#     email = forms.EmailField(label="Адрес получателя", )
#     name = forms.CharField(label="Ваше имя")
#     text = forms.CharField(label="Сообщение", widget=forms.Textarea)


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'author', 'body')
