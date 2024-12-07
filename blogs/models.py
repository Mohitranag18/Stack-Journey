from django.db import models
from django.contrib.auth.models import User

class Thanks(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog_post = models.ForeignKey('BlogPost', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'blog_post')  # Ensure a user can only give thanks once per post

    def __str__(self):
        return f"{self.user.username} thanks post '{self.blog_post.title}'"


class BlogPost(models.Model):
    CATEGORY_CHOICES = [
        ('experience', 'Experience'),
        ('guidance', 'Guidance'),
        ('roadmaps', 'Roadmaps'),
        ('tools_resources', 'Tools & Resources'),
        ('best_practices', 'Best Practices'),
        ('career_development', 'Career Development'),
        ('project_showcase', 'Project Showcase'),
        ('learning_challenges', 'Learning Challenges'),
        ('tech_news_trends', 'Tech News & Trends'),
        ('community_stories', 'Community Stories'),
    ]

    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='guidance')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def total_thanks(self):
        return Thanks.objects.filter(blog_post=self).count()

    def __str__(self):
        return self.title

