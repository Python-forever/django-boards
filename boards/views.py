from django.shortcuts import render, redirect, get_object_or_404, reverse
from .forms import NewTopicForm, PostForm
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseForbidden
from .models import Board, Topic, Post, UserGender
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView
from django.utils import timezone


def home(request):
    boards = Board.objects.all()
    return render(request, 'home.html', {'boards': boards, 'tests': {1: 2,3: 4}})


def board_topics(request, pk):
    board = get_object_or_404(Board, pk=pk)
    topics = board.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
    return render(request, 'topics.html', {'board': board, 'topics': topics})


# def new_topic(request, pk):
#     board = get_object_or_404(Board, pk=pk)
#     if request.method == 'POST':
#         subject = request.POST['subject']
#         message = request.POST['message']
#         user = User.objects.first()  # TODO: get the currently logged in user
#
#         topic = Topic.objects.create(
#             subject=subject,
#             board=board,
#             starter=user
#         )
#
#         post = Post.objects.create(
#             message=message,
#             topic=topic,
#             created_by=user
#         )
#         return redirect('board_topics', pk=board.pk)  # TODO: redirect to the created topic page
#
#     return render(request, 'new_topic.html', {'board': board})

# @login_required
# def new_topic(request, pk):
#     board = get_object_or_404(Board, pk=pk)
#     #user = User.objects.first()  # TODO: get the currently logged in user
#     if request.method == 'POST':
#         form = NewTopicForm(request.POST)
#         if form.is_valid():
#             topic = form.save(commit=False)
#             topic.board = board
#             topic.starter = request.user
#             topic.save()
#             post = Post.objects.create(
#                 message=form.cleaned_data.get('message'),
#                 topic=topic,
#                 created_by=request.user
#             )
#             #return redirect('board_topics', pk=board.pk)  # TODO: redirect to the created topic page
#             return redirect('topic_posts', pk=pk, topic_pk=topic.pk)
#     else:
#         form = NewTopicForm()
#     return render(request, 'new_topic.html', {'board': board, 'form': form})


#Class based view of new_topic
@method_decorator(login_required, name='dispatch')
class NewTopic(View):
    # def __init__(self, pk):
    #     self.board = get_object_or_404(Board, pk=pk)
    #@method_decorator(login_required)
    def post(self, request, pk):
        board = get_object_or_404(Board, pk=pk)
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = request.user
            topic.save()
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=request.user
            )
            #return redirect('board_topics', pk=board.pk)  # TODO: redirect to the created topic page
            return redirect('topic_posts', pk=pk, topic_pk=topic.pk)

    #@method_decorator(login_required)
    def get(self, request, pk):
        board = get_object_or_404(Board, pk=pk)
        form = NewTopicForm()
        return render(request, 'new_topic.html', {'board': board, 'form': form})


# def edit(request, id=None):
#     if id:
#         topic = get_object_or_404(Topic, pk=id)
#         #topic1 = Topic.objects.all()
#     form = NewTopicForm(request.POST or None, instance=topic)
#     if request.POST and form.is_valid():
#         topic = form.save(commit=False)
#         post = topic.posts.get(topic=topic.id)
#         post = Post.objects.get(message = post.message)
#         post.message = form.cleaned_data.get('message')
#         post.save()
#         topic.save()
#
#
#         # Save was successful, so redirect to another page
#         return redirect('board_topics', pk=topic.board.id)
#
#     return render(request, 'topic_edit_template.html', {'topic': topic, 'form': form})


#This view is for looking the topic i.e subject of a Board
def topic_posts(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    #posts = topic.posts.all()
    #print(dir(request))
    userGender = topic.starter.usergender.get(foruser_id=topic.starter_id)
    topic.views += 1
    topic.save()
    return render(request, 'topic_posts.html', {'topic': topic, 'userGender': userGender})



@login_required
def reply_topic(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()
            return redirect('topic_posts', pk=pk, topic_pk=topic_pk)
    else:
        form = PostForm()
    return render(request, 'reply_topic.html', {'topic': topic, 'form': form})


@method_decorator(login_required, name='dispatch')
class PostUpdateView(UpdateView):
    model = Post
    fields = ('message', )
    template_name = 'edit_post.html'
    pk_url_kwarg = 'post_pk'
    context_object_name = 'post'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_at = timezone.now()
        post.save()
        return redirect('topic_posts', pk=post.topic.board.pk, topic_pk=post.topic.pk)
