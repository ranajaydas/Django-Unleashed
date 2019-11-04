from django.db import models
from django.shortcuts import reverse
from organizer.models import Startup, Tag


class Post(models.Model):
    title = models.CharField(max_length=63)
    slug = models.SlugField(
        max_length=63,
        help_text='A label for URL config',
        unique_for_month='pub_date')
    text = models.TextField()
    pub_date = models.DateField('date published', auto_now_add=True)
    startups = models.ManyToManyField(Startup, related_name='blog_posts')   # related_name used instead of 'post_set'
    tags = models.ManyToManyField(Tag, related_name='blog_posts')   # related_name used instead of 'post_set'

    class Meta:
        verbose_name = 'blog post'
        ordering = ['-pub_date', 'title']
        get_latest_by = 'pub_date'

    def __str__(self):
        return '{} on {}'.format(
            self.title,
            self.pub_date.strftime('%Y-%m-%d')
        )

    def get_absolute_url(self):
        return reverse('blog_post_detail',
                       kwargs={'slug': self.slug,
                               'year': self.pub_date.year,
                               'month': self.pub_date.month})

    def get_update_url(self):
        return reverse('blog_post_update',
                       kwargs={'slug': self.slug,
                               'year': self.pub_date.year,
                               'month': self.pub_date.month})

    def get_delete_url(self):
        return reverse('blog_post_delete',
                       kwargs={'slug': self.slug,
                               'year': self.pub_date.year,
                               'month': self.pub_date.month})
