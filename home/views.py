from django.shortcuts import get_object_or_404, render, get_list_or_404
from .models import Post, Tag
from .forms import CommentForm
from django.db.models import Count, Q
from django.core.paginator import Paginator, EmptyPage

def get_tags_for_category(category):
    items = Post.objects.filter(category=category)
    return Tag.objects.filter(post__in=items).annotate(num_posts=Count('post')).filter(num_posts__gt=0)

#HOMEPAGE
def home(request):
    newest_project = newest_publication = newest_about_me = None
    #Project
    try:                       newest_project = Post.objects.filter(category=0, status=1).annotate(num_comments=Count('comments', filter=Q(comments__active=True))).latest('created_on')
    except Post.DoesNotExist:   pass
    #Publication
    try:                       newest_publication = Post.objects.filter(category=1, status=1).annotate(num_comments=Count('comments', filter=Q(comments__active=True))).latest('created_on')
    except Post.DoesNotExist:   pass 
    #About me 
    try:                        newest_about_me = Post.objects.filter(category=2, status=1).latest('created_on')
    except Post.DoesNotExist:   pass
    all_tags = Tag.objects.all()
    popular_posts = Post.objects.annotate(num_comments=Count('comments', filter=Q(comments__active=True))).order_by('-num_comments')[:5]

    return render(request, 'home/homepage.html', {
        'newest_project': newest_project,
        'newest_publication': newest_publication,
        'newest_about_me': newest_about_me,
        'all_tags': all_tags,
        'popular_posts': popular_posts})

def all_tags_list(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    posts_list = Post.objects.filter(tags=tag, status=1).annotate(num_comments=Count('comments', filter=Q(comments__active=True)))
    all_tags = Tag.objects.all()
    popular_posts = Post.objects.annotate(num_comments=Count('comments', filter=Q(comments__active=True))).order_by('-num_comments')[:5]
    
    paginator = Paginator(posts_list, 5) # Show 5 publications per page
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    
    return render(request, 'home/homepage_tag.html', {'tag': tag,
                                                      'posts': posts, 
                                                      'all_tags': all_tags,
                                                      'popular_posts': popular_posts})

#POSTS
def publications(request):
    publications_list = None
    try:   publications_list = Post.objects.filter(category=1, status=1).annotate(num_comments=Count('comments', filter=Q(comments__active=True)))
    except Post.DoesNotExist:   pass 
    tags_for_publications = get_tags_for_category(1)
    popular_posts = Post.objects.annotate(num_comments=Count('comments', filter=Q(comments__active=True))).order_by('-num_comments')[:5]
    paginator = Paginator(publications_list, 5) # Show 5 publications per page
    page = request.GET.get('page')
    publications = paginator.get_page(page)
    return render(request, 'home/posts/publications.html', {'publications': publications, 
                                                            'tags_for_publications': tags_for_publications,
                                                            'popular_posts': popular_posts})

def publications_tags_list(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    publications_list = Post.objects.filter(category=1, tags=tag, status=1).annotate(num_comments=Count('comments', filter=Q(comments__active=True)))
    tags_for_publications = get_tags_for_category(1)
    popular_posts = Post.objects.annotate(num_comments=Count('comments', filter=Q(comments__active=True))).order_by('-num_comments')[:5]
    paginator = Paginator(publications_list, 5) # Show 5 publications per page
    page = request.GET.get('page')
    publications = paginator.get_page(page)
    return render(request, 'home/posts/publications_tag.html', {'tag': tag, 
                                                                'publications': publications, 
                                                                'tags_for_publications': tags_for_publications,
                                                                'popular_posts' : popular_posts})

def projects(request):
    projects_list = None
    try:   projects_list = Post.objects.filter(category=0, status=1).annotate(num_comments=Count('comments', filter=Q(comments__active=True)))
    except Post.DoesNotExist:   pass
    tags_for_projects = get_tags_for_category(0)
    popular_posts = Post.objects.annotate(num_comments=Count('comments', filter=Q(comments__active=True))).order_by('-num_comments')[:5]
    paginator = Paginator(projects_list, 3) # Show 5 projects per page
    page = request.GET.get('page')
    projects = paginator.get_page(page)
    return render(request, 'home/posts/projects.html', {'projects': projects, 
                                                        'tags_for_projects': tags_for_projects,
                                                        'popular_posts': popular_posts})

def projects_tags_list(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    projects_list = Post.objects.filter(category=0, tags=tag, status=1).annotate(num_comments=Count('comments', filter=Q(comments__active=True)))
    tags_for_projects = get_tags_for_category(0)
    popular_posts = Post.objects.annotate(num_comments=Count('comments', filter=Q(comments__active=True))).order_by('-num_comments')[:5]
    paginator = Paginator(projects_list, 5) # Show 5 projects per page
    page = request.GET.get('page')
    projects = paginator.get_page(page)
    return render(request, 'home/posts/projects_tag.html', {'tag': tag, 
                                                            'projects': projects, 
                                                            'tags_for_projects': tags_for_projects,
                                                            'popular_posts': popular_posts})

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(active=True)
    new_comment = None    # Comment posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()
    return render(request, 'home/post_detail.html', {'post': post,
                                                    'comments': comments,
                                                    'new_comment': new_comment,
                                                    'comment_form': comment_form})


# ABOUT ME
def aboutMe(request):
    newest_about_me = None

    # Attempt to get the latest about me post
    try:
        newest_about_me = Post.objects.filter(category=2, status=1).latest('created_on')
    except Post.DoesNotExist:
        pass

    # Initialize a new_comment object
    new_comment = None

    # Check if the form is submitted
    if request.method == 'POST':
        # Create a CommentForm instance with the submitted data
        comment_form = CommentForm(data=request.POST)

        # Check if the form is valid
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            
            # Assign the current post to the comment
            new_comment.post = newest_about_me
            
            # Save the comment to the database
            new_comment.save()

    else:
        # If the request is not a POST request, initialize an empty CommentForm
        comment_form = CommentForm()

    # Render the template with the latest about me post and the comment form
    return render(request, 'home/about-me.html', {'newest_about_me': newest_about_me,
                                                  'comment_form': comment_form})