from django import forms
from .models import Message, Group, Friend, Good
from django.contrib.auth.models import User

# Messageのフォーム(未使用)
class MessageForm(forms.ModelForm):
    # テーブル定義のメタ情報。model用のフォームに関する情報が用意されている。
    # ここでは、modelで使用するモデルクラスを、またFieldsで用意するフィールドをそれぞれ設定している。
    class Meta:
        model = Message
        fields = ['owner', 'group', 'content']

# Groupのフォーム(未使用)
class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['owner', 'title']
        
# Friendのフォーム(未使用)
# formsクラスの中にあるModelsFormというクラス名を継承してサブクラス(FriendForm)を定期する
class FriendForm(forms.ModelForm):
    class Meta:
        model = Friend
        fields = ['owner', 'user', 'group']

# Goodのフォーム（未使用)
# formsクラスの中にあるModelformというクラス名を継承してサブクラスの(GoodForm)を定義する
class GoodForm(forms.ModelForm):
    class Meta:
        model = Good
        fields = ['owner', 'message']

# 検索フォーム
# formsクラスの中にあるFormというクラス名を継承してサブクラス(searchForm)を定義する　
class SearchForm(forms.Form):
    search = forms.CharField(max_length=100)
    
# Groupのチェックボックスフォーム
# fromsクラスの中にあるFormというクラス名を継承してサブクラス(GroupCheckForm)を定義する
class GroupCheckForm(forms.Form):
    def __init__(self, user, *args, **kwargs):
        super(GroupCheckForm, self).__init__(*args, **kwargs)
        public = User.objects.filter(username='public').first()
        self.fields['groups'] = forms.MultipleChoiceField(
            choices = [(item.title, item.title) for item in \
            Group.objects.filter(owner__in=[user, public])],
            widget=forms.CheckboxSelectMultiple(), 
        )

        
# Groupの選択メニューフォーム
# formsクラスの中にあるFormというクラス名を継承してサブクラス(GroupSelectForm)を定義する
class GroupSelectForm(forms.Form):
    def __init__(self, user, *args, **kwargs):
        super(GroupSelectForm, self).__init__(*args, **kwargs)
        self.fields['groups'] = forms.ChoiceField(
            choices=[('-', '-')] + [(item.title, item.title) \
                for item in Group.objects.filter(owner=user)],
        )

# Friendのチェックボックスフォーム
class FriendsForm(forms.Form):
    def __init__(self, user, friends=[], vals=[], *args, **kwargs):
        super(FriendsForm, self).__init__(*args, **kwargs)
        self.fields['friends'] = forms.MultipleChoiceField(
            choices=[(item.user, item.user) for item in friends],
            widget=forms.CheckboxSelectMultiple(),
            initial=vals
        )

# Group作成フォーム
# formsクラスの中にあるFormというクラス名を継承してサブクラス(GroupSelectForm)を定義する
class CreateGroupForm(forms.Form):
    group_name = forms.CharField(max_length=50)

# 投稿フォーム
# formsクラスの中にあるFormというクラス名を継承してサブクラス(PostForm)を定義する
class PostForm(forms.Form):
    content = forms.CharField(max_length=500, widget=forms.Textarea)
    def __init__(self, user, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        public = User.objects.filter(username='public').first()
        self.fields['groups'] = forms.ChoiceField(
            choices=[('-','-')] + [(item.title, item.title) \
            for item in Group.objects.filter(owner__in=[user,public])]
        )