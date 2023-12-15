"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from django.db import models
from .models import Comment
from .models import Blog

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Логин'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Пароль'}))


class feedbackForm(forms.Form):
    name = forms.CharField(label='Имя', min_length=2, max_length=100)
    city = forms.CharField(label='Город', min_length=2, max_length=100,
                           required=False)
    phone = forms.CharField(label='Телефон', min_length=11, max_length=16)
    email = forms.EmailField(label='E-mail', min_length=7, max_length=70)
    message = forms.CharField(label='Комментарий',
                              widget=forms.Textarea(attrs={'rows':7,'cols':60}),
                              required=False)
    callback = forms.ChoiceField(label='Как вы хотите получить ответ?',
                                 choices=[('1', 'По телефону'), ('2', 'По почте')],
                                 widget=forms.RadioSelect, initial=1)
    issue = forms.ChoiceField(label='Какой вопрос вы хотите решить', 
                              choices=(('1', 'Не хватает товаров в заказе'),
                                       ('2', 'Товар не соотвестует качеству'),
                                       ('3', 'Получить гарантийный талон или инструкцию'),
                                       ('4', 'Другой вопрос')), initial=1)
    notice = forms.BooleanField(label='Я принимаю условия пользовательского соглашения и даю согласие на обработку персональных данных', initial=False)
  
    
class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog                                                # используемая модель
        fields = ('title', 'description', 'content', 'image',)      # заполняемые поля
        labels = {'title': "Заголовок", 'description': "Краткое содержание", 'content': "Полное содержание", 'image': "Картинка" } # метки к полям формы
        
class CommentForm (forms.ModelForm):
    class Meta:
        model = Comment                     # используемая модель
        fields = ('text',)                  # требуется заполнить только поле text
        labels = {'text': "Комментарий"}    # метка к полю формы text
# author будет автоматически выбран в зависимости от авторизованного пользователя
# date автоматически дообавляется в момент создания записи