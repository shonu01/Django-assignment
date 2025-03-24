from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Post, Comment, Category, UserProfile, User
from .forms import PostForm, CommentForm, UserRegistrationForm, UserProfileForm, SearchForm
from django.http import Http404

def home(request):
    posts = Post.objects.filter(status='published')
    categories = Category.objects.all()
    recent_posts = Post.objects.filter(status='published').order_by('-created_at')[:5]
    
    # Search functionality
    search_form = SearchForm(request.GET)
    if search_form.is_valid():
        query = search_form.cleaned_data.get('query')
        category = search_form.cleaned_data.get('category')
        
        if query:
            posts = posts.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query)
            )
        if category:
            posts = posts.filter(category=category)
    
    # Pagination
    paginator = Paginator(posts, 5)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    
    context = {
        'posts': posts,
        'categories': categories,
        'recent_posts': recent_posts,
        'search_form': search_form
    }
    return render(request, 'blog/home.html', context)

def post_detail(request, slug):
    """View for displaying a single post with its comments."""
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.all().order_by('-created_at')  # Show all comments, newest first
    
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()  # Remove auto-approval since we're not using it anymore
            messages.success(request, 'Your comment has been posted successfully!')
            return redirect('post_detail', slug=post.slug)
    else:
        comment_form = CommentForm()
    
    # Increment view count
    post.views += 1
    post.save()
    
    # Get related posts
    related_posts = Post.objects.filter(category=post.category).exclude(id=post.id)[:3]
    
    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'related_posts': related_posts,
        'categories': Category.objects.all(),
    }
    return render(request, 'blog/post_detail.html', context)

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Post created successfully!')
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm()
    
    context = {
        'form': form,
        'title': 'Create Post',
        'categories': Category.objects.all()
    }
    return render(request, 'blog/post_form.html', context)

@login_required
def edit_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    
    if request.user != post.author:
        messages.error(request, 'You are not authorized to edit this post.')
        return redirect('post_detail', slug=post.slug)
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully!')
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm(instance=post)
    
    context = {
        'form': form,
        'title': 'Edit Post',
        'categories': Category.objects.all()
    }
    return render(request, 'blog/post_form.html', context)

@login_required
def delete_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    
    if request.user != post.author:
        messages.error(request, 'You are not authorized to delete this post.')
        return redirect('post_detail', slug=post.slug)
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted successfully!')
        return redirect('home')
    
    context = {
        'post': post,
        'categories': Category.objects.all()
    }
    return render(request, 'blog/post_confirm_delete.html', context)

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'blog/register.html', {'form': form})

@login_required
def profile(request, username=None):
    if username is None:
        username = request.user.username
    
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(UserProfile, user=user)
    
    # Get user's posts
    posts = Post.objects.filter(author=user, status='published').order_by('-created_at')
    
    # If viewing own profile, allow editing
    is_own_profile = request.user == user
    if is_own_profile and request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile', username=username)
    else:
        form = UserProfileForm(instance=profile)
    
    context = {
        'profile': profile,
        'form': form,
        'posts': posts,
        'is_own_profile': is_own_profile,
    }
    return render(request, 'blog/profile.html', context)

@login_required
def profile_edit(request, username):
    """View for editing user profile."""
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(UserProfile, user=user)
    
    # Only allow users to edit their own profile
    if request.user != user:
        messages.error(request, 'You are not authorized to edit this profile.')
        return redirect('profile', username=username)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile', username=username)
    else:
        form = UserProfileForm(instance=profile)
    
    context = {
        'form': form,
        'profile': profile,
        'categories': Category.objects.all()
    }
    return render(request, 'blog/profile.html', context)

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(category=category, status='published')
    
    paginator = Paginator(posts, 5)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    
    context = {
        'category': category,
        'posts': posts,
        'categories': Category.objects.all()
    }
    return render(request, 'blog/category_detail.html', context)

def tag_detail(request, slug):
    raise Http404("Tags are no longer supported")

def search(request):
    """View for searching posts."""
    query = request.GET.get('q', '')
    category = request.GET.get('category')
    
    posts = Post.objects.filter(status='published')
    
    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
        )
    
    if category:
        posts = posts.filter(category__slug=category)
    
    # Pagination
    paginator = Paginator(posts, 5)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    
    context = {
        'posts': posts,
        'query': query,
        'categories': Category.objects.all(),
        'selected_category': category,
    }
    return render(request, 'blog/search_results.html', context)

@login_required
def like_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect('post_detail', slug=slug)

def catalog(request):
    """View for displaying a catalog of all posts organized by category."""
    categories = Category.objects.all()
    posts = Post.objects.filter(status='published').order_by('-created_at')
    
    # Create a dictionary of posts by category
    posts_by_category = {}
    for category in categories:
        posts_by_category[category] = posts.filter(category=category)
    
    context = {
        'categories': categories,
        'posts_by_category': posts_by_category,
    }
    return render(request, 'blog/catalog.html', context)

@login_required
def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    
    # Only allow comment author or post author to edit
    if request.user != comment.author and request.user != comment.post.author:
        messages.error(request, 'You are not authorized to edit this comment.')
        return redirect('post_detail', slug=comment.post.slug)
    
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Comment updated successfully!')
            return redirect('post_detail', slug=comment.post.slug)
    else:
        form = CommentForm(instance=comment)
    
    context = {
        'form': form,
        'comment': comment,
        'post': comment.post
    }
    return render(request, 'blog/edit_comment.html', context)

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    
    # Only allow comment author or post author to delete
    if request.user != comment.author and request.user != comment.post.author:
        messages.error(request, 'You are not authorized to delete this comment.')
        return redirect('post_detail', slug=comment.post.slug)
    
    if request.method == 'POST':
        comment.delete()
        messages.success(request, 'Comment deleted successfully!')
        return redirect('post_detail', slug=comment.post.slug)
    
    context = {
        'comment': comment,
        'post': comment.post
    }
    return render(request, 'blog/delete_comment.html', context)
