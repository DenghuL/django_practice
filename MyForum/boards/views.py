from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from django.utils import timezone
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Board, User, Topic, Post
from .forms import NewTopicForm, PostForm
from django.views.generic import UpdateView, ListView


# Create your views here.
class BoardListView(ListView):
    """
    首页 Boards
    """
    model = Board
    context_object_name = 'boards'
    template_name = 'home.html'

    # def home(request):
    #     """
    #     首页
    #     """
    #     boards = Board.objects.all()  # 获取所有的board
    #     """
    #     下面的逻辑交给前端处理
    #     # boards_names = [f"{board.name}<br>{board.description}<br>" for board in boards]#讲boards放入列表中
    #     # respone_html = '<br>'.join(boards_names)#换行符号
    #     """
    #
    #     return render(request, "home.html", {"boards": boards})


class TopicListView(ListView):
    """
    主题页 Topics ，展示的是帖子
    """
    model = Topic
    context_object_name = 'topics'
    template_name = 'topics.html'
    paginate_by = 8

    def get_context_data(self, **kwargs):
        kwargs['board'] = self.board
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.board = get_object_or_404(Board, pk = self.kwargs.get('pk'))
        queryset = self.board.topics.order_by('-last_update').annotate(replies=Count('posts')-1)
        return queryset

    # def board_topics(request, pk):
    #     """
    #     使用到了动态的 url
    #     :param request:
    #     :return:
    #     """
    #     # try:
    #     #     board = Board.objects.get(pk=pk)
    #     # except Board.DoesNotExist:
    #     #     raise Http404
    #     # return render(request, 'topics.html', {"board": board})
    #
    #     # 使用django的快速返回404对象：
    #     board = get_object_or_404(Board, pk=pk)
    #     querryset = board.topics.order_by('-last_update').annotate(replies=Count('posts') - 1)
    #     page = request.GET.get('page',1)
    #
    #     paginator = Paginator(querryset, 8)  # 对获得的 topic 进行分页
    #     try:
    #         topics=paginator.page(page)
    #     except PageNotAnInteger:
    #         #fallback to first page
    #         topics = paginator.page(1)
    #     except EmptyPage:
    #         # probably the user tried to add a page number
    #         # in the url ,so we fallback to the last page
    #         topics = paginator.page(paginator.num_pages)
    #
    #     return render(request, 'topics.html', {'board': board, 'topics': topics})


@login_required
def new_topic(request, pk):
    """
    创建一个 topic
    :param request:
    :param pk:
    :return:
    """
    board = get_object_or_404(Board, pk=pk)
    # user = User.objects.first()  # TODO: get the currently logged in user

    if request.method == 'POST':
        form = NewTopicForm(request.POST)  # 实例化一个提交的新建 topic 表单
        if form.is_valid():  # 验证数据，检查 form 是否有效
            topic = form.save(commit=False)  # 返回一个存入数据库的 Model 实例
            topic.board = board
            topic.starter = request.user
            topic.save()
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=request.user
            )

            return redirect('topic_posts', pk=pk, topic_pk=topic.pk)  # TODO: redirect to the created topic page
    else:
        form = NewTopicForm()
    return render(request, 'new_topic.html', {'board': board, 'form': form})


class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'topic_posts.html'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        session_key = 'viewed_topic_{}'.format(self.topic.pk)
        if not self.request.session.get(session_key, False):
            self.topic.views += 1
            self.topic.save()
            self.request.session[session_key] = True
        kwargs['topic'] = self.topic
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.topic = get_object_or_404(Topic, board__pk=self.kwargs.get('pk'), pk=self.kwargs.get('topic_pk'))
        queryset = self.topic.posts.order_by('created_by').annotate()
        return queryset

    # def topic_posts(request, pk, topic_pk):
    #     # topic 的 post 展示
    #     topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    #     topic.views += 1
    #     topic.save()
    #     return render(request, 'topic_posts.html', {'topic': topic})


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

            topic.last_update = timezone.now()  # <- 这里
            topic.save()

            return redirect('topic_posts', pk=pk, topic_pk=topic_pk)
    else:
        form = PostForm()
    return render(request, 'reply_topic.html', {'topic': topic, 'form': form})


@method_decorator(login_required, name='dispatch')
class PostUpDataView(UpdateView):
    model = Post
    fields = ('message',)
    template_name = 'edit_post.html'
    pk_url_kwarg = 'post_pk'
    context_object_name = 'post'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)

    def form_valid(self,form):
        # form = PostForm(self.request.POST)
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_at = timezone.now()
        post.save()
        return redirect('topic_posts', pk=post.topic.board.pk, topic_pk=post.topic.pk)

