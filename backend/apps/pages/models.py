from django.db import models
from wagtail.contrib.routable_page.models import RoutablePage, path
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import RichTextField
from apps.blog.models import BlogPostPage
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


class HomePage(RoutablePage):
    subpage_types = [
        "pages.AboutPage",
        "pages.ContactPage",
        "pages.InnerPage",
        "blog.BlogIndexPage",
        "portfolio.PortfolioIndexPage",
    ]

    hero_title = models.CharField(blank=True)
    hero_subtitle = models.CharField(blank=True)
    hero_description = RichTextField(blank=True)
    hero_button = models.CharField(blank=True)

    content_panels = RoutablePage.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("hero_title"),
                FieldPanel("hero_subtitle"),
                FieldPanel("hero_description"),
                FieldPanel("hero_button"),
            ],
            "Hero Section",
        )
    ]

    @path("")
    def home_page(self, request):
        posts_queryset = BlogPostPage.objects.live().specific().select_related("cover", "category")
        paginator = Paginator(posts_queryset, 4)
        posts = paginator.page(1)

        return self.render(request, context_overrides={"posts": posts})


class AboutPage(RoutablePage):
    subpage_types = []
    content_panels = RoutablePage.content_panels


class ContactPage(RoutablePage):
    subpage_types = []
    content_panels = RoutablePage.content_panels


class InnerPage(RoutablePage):
    subpage_types = ["pages.InnerPage"]
    parent_page_types = ["pages.InnerPage"]

    content_panels = RoutablePage.content_panels
