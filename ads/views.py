from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.db.models.functions import Lower
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from ads.forms import AdFilterForm, AdForm, SignUpForm
from ads.models import Ad


class AdListView(ListView):
    model = Ad
    template_name = 'ads/ads_list.html'
    context_object_name = 'ads'
    paginate_by = 5
    page_title = 'Все объявления'

    def get_base_queryset(self):
        return Ad.objects.select_related('category', 'author')

    def get_queryset(self):
        qs = self.get_base_queryset()
        self.filter_form = AdFilterForm(self.request.GET or None)
        if self.filter_form.is_valid():
            q = self.filter_form.cleaned_data['q']
            category = self.filter_form.cleaned_data['category']
            if q:
                q = q.strip().lower()
                qs = qs.annotate(
                    title_lower=Lower('title'),
                    description_lower=Lower('description'),
                ).filter(Q(title_lower__contains=q) | Q(description_lower__contains=q))
            if category:
                qs = qs.filter(category=category)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.filter_form
        context['page_title'] = self.page_title
        context['is_filtered'] = bool(
            self.request.GET.get('q') or self.request.GET.get('category')
        )
        return context


class MyAdListView(LoginRequiredMixin, AdListView):
    page_title = 'Мои объявления'

    def get_base_queryset(self):
        return super().get_base_queryset().filter(author=self.request.user)


class AdDetailView(DetailView):
    model = Ad
    template_name = 'ads/ad_detail.html'
    context_object_name = 'ad'

    def get_queryset(self):
        return Ad.objects.select_related('category', 'author')


class AdCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Ad
    form_class = AdForm
    template_name = 'ads/ad_form.html'
    success_message = 'Объявление опубликовано.'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class AuthorRequiredMixin(LoginRequiredMixin):
    def get_queryset(self):
        return Ad.objects.filter(author=self.request.user)


class AdUpdateView(AuthorRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Ad
    form_class = AdForm
    template_name = 'ads/ad_form.html'
    success_message = 'Изменения сохранены.'


class AdDeleteView(AuthorRequiredMixin, DeleteView):
    model = Ad
    template_name = 'ads/ad_confirm_delete.html'
    context_object_name = 'ad'
    success_url = reverse_lazy('my_ads')

    def form_valid(self, form):
        messages.success(self.request, f'Объявление «{self.object.title}» удалено.')
        return super().form_valid(form)


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('ad_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, 'Добро пожаловать! Аккаунт создан.')
        return response
