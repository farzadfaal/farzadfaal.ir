from wagtail.contrib.routable_page.models import path, RoutablePage
from django.db import models
from wagtail.images.models import Image as WagtailImage
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class PortfolioIndexPage(RoutablePage):
    subpage_types = ["portfolio.PortfolioItemPage"]
    parent_page_types = ["pages.HomePage"]

    content_panels = RoutablePage.content_panels + []

    @path("")
    def portfolio_index(self, request):
        items_queryset = PortfolioItemPage.objects.child_of(self).live().specific().select_related("cover", "category")
        paginator = Paginator(items_queryset, 10)
        page_number = request.GET.get("page")

        try:
            items = paginator.page(page_number)
        except PageNotAnInteger:
            items = paginator.page(1)
        except EmptyPage:
            items = paginator.page(paginator.num_pages)

        return self.render(request, context_overrides={"items": items})


class PortfolioItemPage(RoutablePage):
    subpage_types = []
    parent_page_types = ["portfolio.PortfolioIndexPage"]

    category = models.ForeignKey(
        "portfolio.PortfolioCategoryPage",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="+",
    )
    cover = models.ForeignKey(
        WagtailImage,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
    )
    excerpt = RichTextField(blank=True)
    body = RichTextField(blank=True)

    content_panels = RoutablePage.content_panels + [
        FieldPanel("cover"),
        FieldPanel("excerpt"),
        FieldPanel("body"),
    ]


class PortfolioCategoryPage(RoutablePage):
    subpage_types = []
    parent_page_types = ["portfolio.PortfolioIndexPage"]

    content_panels = RoutablePage.content_panels + []
