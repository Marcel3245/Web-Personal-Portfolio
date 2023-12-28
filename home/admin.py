from django.contrib import admin
from .models import  Post, Tag, Comment

@admin.register(Post)
class ProductAdmin(admin.ModelAdmin):
    list_display =          ['title',           #Filtering a products by
                            'category', 
                            'slug',
                            'status', 
                            'created_on', 
                            'updated_on']    
    
    list_filter =           ['status',
                            'category',
                            'tags', 
                            'created_on']
    
    list_editable =         ['status',          #Data posible to edit
                            'category']
    
    search_fields =         ["title",
                            "status",
                            'tags',
                            "category"]
    
    prepopulated_fields =   {'slug':('title',)} 
    date_hierarchy = "created_on"
    save_on_top = True


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    model = Tag
    prepopulated_fields =   {'slug':('name',)} 


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'post', 'created_on', 'active')
    list_filter = ('active', 'created_on')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comments']
    list_editable = ['active']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)