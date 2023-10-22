from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Board, User, Topic, Post
from .forms import NewTopicForm, PostForm
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.views.generic import UpdateView, ListView
from django.utils import timezone
from django.utils.decorators import method_decorator

# Create your views here.

# def home(request):
#     boards = Board.objects.all()
#     return render(request, 'home.html', {'boards':boards})

class BoardListView(ListView):
    model = Board
    context_object_name = 'boards'
    template_name = 'home.html'

def board_topics(request, id):
    board = get_object_or_404(Board, pk=id)
    topics = board.topics.order_by('-last_update').annotate(replies=Count('posts') - 1)
    return render(request, 'topics.html', {'board':board, 'topics':topics})

@login_required
def new_topic(request, id):
    board = get_object_or_404(Board, pk=id)
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = request.user
            topic.save()
            post = Post.objects.create(message = form.cleaned_data.get('message'), topic = topic, created_by = request.user)
            return redirect('topic_posts', id=id, topic_id=topic.pk) 
    else:
        form = NewTopicForm()
    return render(request, 'new_topic.html', {'board':board, 'form':form})


def topic_posts(request, id, topic_id):
    topic = get_object_or_404(Topic, board__pk = id, pk = topic_id)
    topic.views += 1
    topic.save()
    return render(request, 'topic_posts.html', {'topic':topic})

@login_required
def reply_topic(request, id, topic_id):
    topic = get_object_or_404(Topic, board__pk = id, pk = topic_id)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()
            return redirect('topic_posts', id=id, topic_id=topic_id)
    else:
        form = PostForm()
    return render(request, 'reply_topic.html', {'topic': topic, 'form': form})

@method_decorator(login_required, name='dispatch')
class PostUpdateView(UpdateView):
    model = Post
    fields = ('message',)
    template_name = 'edit_post.html'
    pk_url_kwarg = 'post_id'
    context_object_name = 'post'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)

    def form_valid(self, form):
        post = form.save()
        post.update_at = timezone.now()
        post.update_by = self.request.user
        post.save()
        return redirect('topic_posts', id=post.topic.board.pk, topic_id=post.topic.pk)
    
        

