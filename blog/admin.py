from django.contrib import admin

from .models import Post, Author, Tag

# Register your models here.


class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('author', 'tag', 'date')
    list_display = ('title', 'date', 'author',)
    readonly_fields = ('date',)


admin.site.register(Post, PostAdmin)
admin.site.register(Author)
admin.site.register(Tag)
