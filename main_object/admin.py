from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Category, MainObject, Tag, AdditionalObjects, RankValue, Rank, Review
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget
# Register your models here.


class MainObjectAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = MainObject
        fields = '__all__'


class ReviewsCommentInline(admin.TabularInline):
    model = Review
    extra = 1
    list_display = (
        'author', 'parent', 'main_object', 'id'
    )
    readonly_fields = (
        'author',
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', "name", 'slug')
    list_display_links = ('name', 'id')


@admin.register(MainObject)
class MainObjectAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'date_published', 'category', 'about', 'author', 'draft'
    )
    list_display_links = ('id', 'name')
    list_filter = ('author',)
    search_fields = ('name', 'category__name')
    inlines = [
        ReviewsCommentInline,
    ]
    save_on_top = True
    save_as = True
    list_editable = ('draft',)
    actions = [
        'publish',
        'un_publish'
    ]
    form = MainObjectAdminForm

    def un_publish(self, request, queryset):
        row_update = queryset.update(draft=True)
        if row_update == 1:
            message_bit = 'object hac been updated'
        else:
            message_bit = f'{row_update} objects has been updated'
        self.message_user(request, f'{message_bit}')

    def publish(self, request, queryset):
        row_update = queryset.update(draft=False)
        if row_update == 1:
            message_bit = 'object hac been updated'
        else:
            message_bit = f'{row_update} objects has been updated'
        self.message_user(request, f'{message_bit}')

    publish.short_description = 'Publish'
    publish.allowed_permisions = ('change',)

    un_publish.short_description = 'UnPublish'
    un_publish.allowed_permisions = ('change',)


@admin.register(AdditionalObjects)
class AdditionalObjectsAdmin(admin.ModelAdmin):

    readonly_fields = ('get_image',)
    list_display = (
        'title', 'description', 'get_image',
    )

    def get_image(self, obj):
        return mark_safe(f'<img scr={obj.image.url} width="50" height="50"')

    get_image.short_description = 'Image'


@admin.register(Review)
class ReviewsCommentAdmin(admin.ModelAdmin):
    list_display = (
        'author', 'parent', 'main_object', 'id'
    )



admin.site.register(Tag)
admin.site.register(Rank)
admin.site.register(RankValue)