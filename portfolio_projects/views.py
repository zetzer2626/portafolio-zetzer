from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.http import JsonResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Project, Category, Comment, Vote, Technology, ProjectImage
from .forms import ProjectForm, CommentForm, ProjectImageForm

class ProjectListView(ListView):
    model = Project
    template_name = 'portfolio_projects/project_list.html'
    context_object_name = 'projects'
    paginate_by = 9
    
    def get_queryset(self):
        queryset = Project.objects.all()
        
        # Filtro por categoría
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(categories__slug=category_slug)
        
        # Filtro por tecnología
        technology = self.request.GET.get('technology')
        if technology:
            queryset = queryset.filter(technologies__name__icontains=technology)
        
        # Búsqueda por palabra clave
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(content__icontains=search_query) |
                Q(technologies__name__icontains=search_query)
            ).distinct()
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['technologies'] = Technology.objects.all()
        context['featured_projects'] = Project.objects.filter(is_featured=True)[:3]
        return context

class ProjectDetailView(DetailView):
    model = Project
    template_name = 'portfolio_projects/project_detail.html'
    context_object_name = 'project'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.get_object()
        
        # Incrementar vistas
        project.views += 1
        project.save()
        
        # Obtener comentarios aprobados
        context['comments'] = project.comments.filter(is_approved=True)
        context['comment_form'] = CommentForm()
        
        # Verificar si el usuario actual ha votado
        if self.request.user.is_authenticated:
            user_vote = project.votes.filter(user=self.request.user).first()
            context['user_vote'] = user_vote.vote_type if user_vote else None
        
        return context

class ProjectCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'portfolio_projects/project_form.html'
    success_url = reverse_lazy('project_list')
    
    def test_func(self):
        return self.request.user.is_superuser
    
    def form_valid(self, form):
        messages.success(self.request, 'Proyecto creado exitosamente.')
        return super().form_valid(form)

class ProjectUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'portfolio_projects/project_form.html'
    
    def test_func(self):
        return self.request.user.is_superuser
    
    def form_valid(self, form):
        messages.success(self.request, 'Proyecto actualizado exitosamente.')
        return super().form_valid(form)

class ProjectDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Project
    template_name = 'portfolio_projects/project_confirm_delete.html'
    success_url = reverse_lazy('project_list')
    
    def test_func(self):
        return self.request.user.is_superuser
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Proyecto eliminado exitosamente.')
        return super().delete(request, *args, **kwargs)

@login_required
def add_comment(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.project = project
            comment.user = request.user
            comment.save()
            messages.success(request, 'Comentario agregado exitosamente.')
        else:
            messages.error(request, 'Error al agregar el comentario.')
    
    return redirect('project_detail', slug=project.slug)

@login_required
def vote_project(request, project_id):
    if request.method == 'POST':
        project = get_object_or_404(Project, id=project_id)
        vote_type = request.POST.get('vote_type')
        
        if vote_type in ['like', 'dislike']:
            vote, created = Vote.objects.get_or_create(
                project=project,
                user=request.user,
                defaults={'vote_type': vote_type}
            )
            
            if not created:
                if vote.vote_type == vote_type:
                    # Si ya votó igual, eliminar el voto
                    vote.delete()
                    vote_type = None
                else:
                    # Cambiar el tipo de voto
                    vote.vote_type = vote_type
                    vote.save()
            
            return JsonResponse({
                'likes': project.get_likes_count(),
                'dislikes': project.get_dislikes_count(),
                'user_vote': vote_type
            })
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

def category_projects(request, slug):
    category = get_object_or_404(Category, slug=slug)
    projects = Project.objects.filter(categories=category)
    
    paginator = Paginator(projects, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'projects': page_obj,
        'categories': Category.objects.all(),
    }
    return render(request, 'portfolio_projects/category_projects.html', context)

# Vistas para gestionar imágenes del proyecto
@login_required
def project_images(request, slug):
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para realizar esta acción.')
        return redirect('project_list')
    
    project = get_object_or_404(Project, slug=slug)
    
    if request.method == 'POST':
        form = ProjectImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.project = project
            image.save()
            messages.success(request, 'Imagen agregada exitosamente.')
            return redirect('project_images', slug=slug)
    else:
        form = ProjectImageForm()
    
    context = {
        'project': project,
        'form': form,
    }
    return render(request, 'portfolio_projects/project_images.html', context)

@login_required
def project_image_update(request, slug, image_id):
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para realizar esta acción.')
        return redirect('project_list')
    
    project = get_object_or_404(Project, slug=slug)
    image = get_object_or_404(ProjectImage, id=image_id, project=project)
    
    if request.method == 'POST':
        form = ProjectImageForm(request.POST, request.FILES, instance=image)
        if form.is_valid():
            form.save()
            messages.success(request, 'Imagen actualizada exitosamente.')
            return redirect('project_images', slug=slug)
    else:
        form = ProjectImageForm(instance=image)
    
    context = {
        'project': project,
        'form': form,
        'image': image,
    }
    return render(request, 'portfolio_projects/project_image_form.html', context)

@login_required
def project_image_delete(request, slug, image_id):
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para realizar esta acción.')
        return redirect('project_list')
    
    project = get_object_or_404(Project, slug=slug)
    image = get_object_or_404(ProjectImage, id=image_id, project=project)
    
    if request.method == 'POST':
        image.delete()
        messages.success(request, 'Imagen eliminada exitosamente.')
        return redirect('project_images', slug=slug)
    
    context = {
        'project': project,
        'image': image,
    }
    return render(request, 'portfolio_projects/project_image_confirm_delete.html', context)
