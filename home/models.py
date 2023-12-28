from django.db import models
from django.urls import reverse
from django_ckeditor_5.fields import CKEditor5Field

#Tag model
class Tag(models.Model):
    name                    = models.CharField(max_length=255, db_index=True)
    slug                    = models.SlugField(max_length=255, unique=True)  # http://127.0.0.1:8000/...(slug).../

    def get_absolute_url(self):
        return reverse('home:all_tags_list', args=[self.slug])
    
    def get_absolute_url_publications(self):
        return reverse('home:publications_tags_list', args=[self.slug])
    
    def get_absolute_url_projects(self):
        return reverse('home:projects_tags_list', args=[self.slug])

    def __str__(self):
        return self.name


#Post model
STATUS = (
    (0,"Draft"),
    (1,"Publish")
)

CATEGORIES = (
    (0,"Project"),
    (1,"Publication"),
    (2,"About-me")
)

class Post(models.Model):
    category                = models.IntegerField(choices=CATEGORIES)                       #If it's Project, Publication or About-me update
    title                   = models.CharField(max_length=200, unique=True)
    version                 = models.CharField(max_length=200, default='Version 1.0')
    slug                    = models.SlugField(max_length=200, unique=True)
    description             = models.TextField(max_length=400, blank=True)                  #An optional clarifier of the post’s content to help readers understand if they want to read it
    content                 = CKEditor5Field('Text', config_name='extends', blank=False)    #The post’s content
    meta_description        = models.CharField(max_length=150, blank=True)                  #An optional description to use for search engines like Google
    image                   = models.ImageField(upload_to='images/')
    updated_on              = models.DateTimeField(auto_now=True)
    created_on              = models.DateTimeField(auto_now_add=True)
    status                  = models.IntegerField(choices=STATUS, default=0)                #Published or Draft, default=Draft
    author                  = models.CharField(max_length=255, default='Marcel')
    tags                    = models.ManyToManyField(Tag, blank=True)

    class Meta:
        verbose_name_plural = 'Posts'   
        ordering = ['-created_on']

    def get_absolute_url(self):
        return reverse('home:post_detail', args=[self.slug])
        
    def __str__(self):
        return self.title
    
#Comment model
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField(blank=True)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)
    