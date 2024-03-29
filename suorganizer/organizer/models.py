from django.db import models
from django.shortcuts import reverse
from urllib.parse import urlparse


class Tag(models.Model):
    name = models.CharField(max_length=31, unique=True)
    slug = models.SlugField(max_length=31, unique=True, help_text='A label for URL config')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name.title()

    def get_absolute_url(self):
        return reverse('organizer_tag_detail', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('organizer_tag_update', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('organizer_tag_delete', kwargs={'slug': self.slug})


class Startup(models.Model):
    name = models.CharField(max_length=31, db_index=True)
    slug = models.SlugField(max_length=31, unique=True, help_text='A label for URL config')
    description = models.TextField()
    founded_date = models.DateField('date founded')
    contact = models.EmailField()
    website = models.URLField(max_length=255)
    tags = models.ManyToManyField(Tag, blank=True)

    class Meta:
        ordering = ['name']
        get_latest_by = 'founded_date'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('organizer_startup_detail', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('organizer_startup_update', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('organizer_startup_delete', kwargs={'slug': self.slug})

    def get_newslink_create_url(self):
        return reverse('organizer_newslink_create', kwargs={'startup_slug': self.slug})

    def get_feed_atom_url(self):
        return reverse('organizer_startup_atom_feed', kwargs={'startup_slug': self.slug})

    def get_feed_rss_url(self):
        return reverse('organizer_startup_rss_feed', kwargs={'startup_slug': self.slug})


class NewsLink(models.Model):
    title = models.CharField(max_length=63)
    slug = models.SlugField(max_length=63)
    link = models.URLField(max_length=255)
    pub_date = models.DateField('date published')
    startup = models.ForeignKey(Startup, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'news article'  # To display in the admin console instead of 'News links'
        ordering = ['-pub_date']
        get_latest_by = 'pub_date'
        unique_together = ('slug', 'startup')  # different startups can have the same slug field

    def __str__(self):
        return f'{self.startup}:{self.title}'

    def get_absolute_url(self):
        return self.startup.get_absolute_url()

    def get_update_url(self):
        return reverse('organizer_newslink_update',
                       kwargs={
                           'startup_slug': self.startup.slug,
                           'newslink_slug': self.slug
                       })

    def get_delete_url(self):
        return reverse('organizer_newslink_delete',
                       kwargs={
                           'startup_slug': self.startup.slug,
                           'newslink_slug': self.slug
                       })

    def description(self):
        return ('Written on {0:%A, %B} {0.day}, {0:%Y}; hosted at {1}'.format(self.pub_date,
                                                                              urlparse(self.link).netloc))
