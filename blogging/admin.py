from django.contrib import admin
from blogging.models import Post, Category


# InlineModelAdmin: represents Categories on the Post Admin Page
class CategoryInline(admin.TabularInline):
    model = Category.posts.through

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [CategoryInline]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    exclude = ['posts']
