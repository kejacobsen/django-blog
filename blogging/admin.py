from django.contrib import admin
from blogging.models import Post, Category


"""
InlineModelAdmin: represents Categories on the Post Admin Page

reference: https://docs.djangoproject.com/en/5.1/ref/contrib/admin/#working-with-a-model-with-two-or-more-foreign-keys-to-the-same-parent-model
The through attribute is a reference to the model that manages
the many-to-many relation. This model is automatically created
by Django when you define a many-to-many field.
"""


class CategoryInline(admin.TabularInline):
    model = Category.posts.through


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [CategoryInline]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    exclude = ["posts"]
