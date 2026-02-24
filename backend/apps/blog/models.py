from wagtail.contrib.routable_page.models import RoutablePage, path
from wagtail.images.models import Image as WagtailImage
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from django.db import models
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.conf import settings
from django.contrib.auth import get_user_model


class BlogIndexPage(RoutablePage):
    parent_page_types = ["pages.HomePage"]
    subpage_types = ["blog.BlogPostPage", "blog.BlogCategoryPage"]

    excerpt = models.TextField(blank=True)

    content_panels = RoutablePage.content_panels + [
        FieldPanel("excerpt"),
    ]

    @path("")
    def blog_index(self, request):
        posts_queryset = BlogPostPage.objects.child_of(self).live().specific().select_related("cover", "category")
        paginator = Paginator(posts_queryset, 10)
        page_number = request.GET.get("page")

        try:
            posts = paginator.page(page_number)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        return self.render(request, context_overrides={"posts": posts})


class BlogPostPage(RoutablePage):
    subpage_types = []
    parent_page_types = ["blog.BlogIndexPage"]

    cover = models.ForeignKey(
        WagtailImage,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="+",
    )
    excerpt = models.TextField(null=True, blank=True)
    body = RichTextField(blank=True)
    category = models.ForeignKey(
        "blog.BlogCategoryPage",
        related_name="posts",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )

    content_panels = RoutablePage.content_panels + [
        FieldPanel("category"),
        FieldPanel("excerpt"),
        FieldPanel("cover"),
        FieldPanel("body"),
    ]


class BlogCategoryPage(RoutablePage):
    subpage_types = []
    parent_page_types = ["blog.BlogIndexPage"]

    content_panels = RoutablePage.content_panels + []
