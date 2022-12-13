from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, Tag, ArticleTag


class RelationshipInlineFormset(BaseInlineFormSet):
    is_main_check = 0

    def clean(self):
        for form in self.forms:
            if form.cleaned_data:
                if form.cleaned_data['is_main']:
                    self.is_main_check += 1
        if self.is_main_check != 1:
            raise ValidationError('Основной раздел должен быть только один')
        return super().clean()


class RelationshipInline(admin.TabularInline):
    model = ArticleTag
    formset = RelationshipInlineFormset


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [RelationshipInline]


admin.site.register(Tag)
