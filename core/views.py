from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.views.generic import DetailView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.http import Http404
from .models import Profile, Experience, Certification, Skill, UserSkill
from .forms import ProfileForm, ExperienceForm, CertificationForm

def home(request):
    """Vista principal del portafolio"""
    from portfolio_projects.models import Project, Category
    
    context = {
        'featured_projects': Project.objects.filter(is_featured=True)[:6],
        'categories': Category.objects.all(),
        'total_projects': Project.objects.count(),
    }
    return render(request, 'core/home.html', context)

def about(request):
    """Vista sobre mí"""
    try:
        # Obtener el primer perfil de superusuario
        profile = Profile.objects.filter(user__is_superuser=True).first()
    except Profile.DoesNotExist:
        profile = None
    
    context = {
        'profile': profile,
        'experiences': Experience.objects.filter(user__is_superuser=True),
        'certifications': Certification.objects.filter(user__is_superuser=True),
        'skills': Skill.objects.all(),
    }
    return render(request, 'core/about.html', context)

class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'core/profile_detail.html'
    context_object_name = 'profile'
    
    def get_object(self):
        # Obtener el primer perfil del superusuario
        profile = Profile.objects.filter(user__is_superuser=True).first()
        if not profile:
            raise Http404("No se encontró ningún perfil de superusuario")
        return profile
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['experiences'] = Experience.objects.filter(user__is_superuser=True)
        context['certifications'] = Certification.objects.filter(user__is_superuser=True)
        context['skills'] = Skill.objects.all()
        return context

class ProfileUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'core/profile_form.html'
    success_url = reverse_lazy('about')
    
    def test_func(self):
        return self.request.user.is_superuser
    
    def get_object(self):
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile
    
    def form_valid(self, form):
        messages.success(self.request, 'Perfil actualizado exitosamente.')
        return super().form_valid(form)

@login_required
def experience_create(request):
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para realizar esta acción.')
        return redirect('about')
    
    if request.method == 'POST':
        form = ExperienceForm(request.POST)
        if form.is_valid():
            experience = form.save(commit=False)
            experience.user = request.user
            experience.save()
            messages.success(request, 'Experiencia agregada exitosamente.')
            return redirect('about')
    else:
        form = ExperienceForm()
    
    return render(request, 'core/experience_form.html', {'form': form, 'experience': None})

@login_required
def experience_update(request, pk):
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para realizar esta acción.')
        return redirect('about')
    
    experience = get_object_or_404(Experience, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = ExperienceForm(request.POST, instance=experience)
        if form.is_valid():
            form.save()
            messages.success(request, 'Experiencia actualizada exitosamente.')
            return redirect('about')
    else:
        form = ExperienceForm(instance=experience)
    
    return render(request, 'core/experience_form.html', {'form': form, 'experience': experience})

@login_required
def experience_delete(request, pk):
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para realizar esta acción.')
        return redirect('about')
    
    experience = get_object_or_404(Experience, pk=pk, user=request.user)
    
    if request.method == 'POST':
        experience.delete()
        messages.success(request, 'Experiencia eliminada exitosamente.')
        return redirect('about')
    
    return render(request, 'core/experience_confirm_delete.html', {'experience': experience})

@login_required
def certification_create(request):
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para realizar esta acción.')
        return redirect('about')
    
    if request.method == 'POST':
        form = CertificationForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                certification = form.save(commit=False)
                certification.user = request.user
                certification.save()
                messages.success(request, 'Certificación agregada exitosamente.')
                return redirect('about')
            except Exception as e:
                messages.error(request, f'Error al guardar la certificación: {str(e)}')
                return render(request, 'core/certification_form.html', {'form': form, 'certification': None})
    else:
        form = CertificationForm()
    
    return render(request, 'core/certification_form.html', {'form': form, 'certification': None})

@login_required
def certification_update(request, pk):
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para realizar esta acción.')
        return redirect('about')
    
    certification = get_object_or_404(Certification, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = CertificationForm(request.POST, request.FILES, instance=certification)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Certificación actualizada exitosamente.')
                return redirect('about')
            except Exception as e:
                messages.error(request, f'Error al actualizar la certificación: {str(e)}')
                return render(request, 'core/certification_form.html', {'form': form, 'certification': certification})
    else:
        form = CertificationForm(instance=certification)
    
    return render(request, 'core/certification_form.html', {'form': form, 'certification': certification})

@login_required
def certification_delete(request, pk):
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para realizar esta acción.')
        return redirect('about')
    
    certification = get_object_or_404(Certification, pk=pk, user=request.user)
    
    if request.method == 'POST':
        certification.delete()
        messages.success(request, 'Certificación eliminada exitosamente.')
        return redirect('about')
    
    return render(request, 'core/certification_confirm_delete.html', {'certification': certification})
