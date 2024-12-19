from typing import Any

from django.contrib.auth.models import User
from django.db.models import Q
from django.db.models.query import QuerySet
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.views.generic import DetailView, ListView

from blog.models import Page, Post

PER_PAGE = 9


# Create your views here.
class PostListView(ListView):
    queryset = Post.objects.get_published()  # type: ignore
    template_name = "blog/pages/index.html"
    context_object_name = "posts"
    paginate_by = PER_PAGE

    # Adicionando mais informações ao contexto
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context.update({"page_title": "Home"})
        return context


class PageDetailView(DetailView):
    model = Page
    template_name = "blog/pages/page.html"
    slug_field = "slug"
    context_object_name = "page"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        page = self.get_object()
        page_title = f"{page.title} - Página"  # type: ignore
        context.update({"page_title": page_title})
        return context

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(is_published=True)


# def page(request: HttpRequest, slug: str):
#     page_obj = Page.objects.filter(is_published=True).filter(slug=slug).first()
#     if page_obj is None:
#         raise Http404()

#     page_title = f"{page_obj.title} - Página"  # type: ignore

#     return render(
#         request,
#         "blog/pages/page.html",
#         {
#             "page": page_obj,
#             "page_title": page_title,
#         },
#     )


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/pages/post.html"
    slug_field = "slug"
    context_object_name = "post"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        page_title = f"{post.title} - Página"  # type: ignore
        context.update({"page_title": page_title})
        return context

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(is_published=True)


# def post(request: HttpRequest, slug: str):
#     post_object = Post.objects.get_published().filter(slug=slug).first()  # type: ignore

#     if post_object is None:
#         raise Http404()

#     page_title = f"{post_object.title} - Post"  # type: ignore

#     return render(
#         request,
#         "blog/pages/post.html",
#         {"post": post_object, "page_title": page_title},
#     )


class CreatedByListView(PostListView):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._temp_context: dict[str, Any] = {}

    def get(
        self, request: HttpRequest, *args: Any, **kwargs: int
    ) -> HttpResponse:
        author_pk: int = self.kwargs.get("author_pk")
        user = User.objects.filter(pk=author_pk).first()

        if user is None:
            raise Http404()

        self._temp_context.update({"author_pk": author_pk, "user": user})

        return super().get(request, *args, **kwargs)

    def get_queryset(self) -> QuerySet[Any]:
        qs = super().get_queryset()
        # OBS: O __ do filter indica que está procurando dentro da foreign key
        qs = qs.filter(created_by__pk=self._temp_context["user"].pk)

        return qs

    def get_context_data(self, **kwargs: int) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        user: User = self._temp_context["user"]
        user_full_name = user.username

        if user.first_name:
            user_full_name = f"{user.first_name} {user.last_name}"

        page_title = f"Página de {user_full_name}"
        context.update({"page_title": page_title})
        return context


# def created_by(request: HttpRequest, author_pk: int):
#     user = User.objects.filter(pk=author_pk).first()

#     if user is None:
#         raise Http404()

#     # OBS: O __ do filter indica que está procurando dentro da foreign key
#     posts = Post.objects.get_published().filter(created_by__pk=author_pk)  # type: ignore
#     paginator = Paginator(posts, PER_PAGE)  # type: ignore
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)

#     user_full_name = user.username  # type: ignore
#     if user.first_name:  # type: ignore
#         user_full_name = f"{user.first_name} {user.last_name}"  # type: ignore
#     page_title = f"Página de {user_full_name}"

#     return render(
#         request,
#         "blog/pages/index.html",
#         {"page_obj": page_obj, "page_title": page_title},  # type: ignore
#     )


class CategoryListView(PostListView):
    allow_empty = False

    def get_queryset(self) -> QuerySet[Any]:
        slug: str = self.kwargs.get("slug")
        # OBS: O __ do filter indica que está procurando dentro da foreign key
        return super().get_queryset().filter(category__slug=slug)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        page_title = f"{self.object_list[0].tags.first().name} - categoria"  # type: ignore
        context.update({"page_title": page_title})
        return context


# def category(request: HttpRequest, slug: str):
#     # OBS: O __ do filter indica que está procurando dentro da foreign key
#     posts = Post.objects.get_published().filter(category__slug=slug)  # type: ignore
#     paginator = Paginator(posts, PER_PAGE)  # type: ignore
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)

#     if len(page_obj) == 0:  # type: ignore
#         raise Http404()

#     page_title = f"{page_obj[0].tags.first().name} - categoria"  # type: ignore

#     return render(
#         request,
#         "blog/pages/index.html",
#         {"page_obj": page_obj, "page_title": page_title},
#     )


class TagListView(PostListView):
    allow_empty = False

    def get_queryset(self) -> QuerySet[Any]:
        slug: str = self.kwargs.get("slug")
        # OBS: O __ do filter indica que está procurando dentro da foreign key
        return super().get_queryset().filter(tags__slug=slug)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        page_title = f"{self.object_list[0].tags.first().name} - tags"  # type: ignore
        context.update({"page_title": page_title})
        return context


# def tag(request: HttpRequest, slug: str):
#     # OBS: O __ do filter indica que está procurando dentro da foreign key
#     posts = Post.objects.get_published().filter(tags__slug=slug)  # type: ignore
#     paginator = Paginator(posts, PER_PAGE)  # type: ignore
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)

#     if len(page_obj) == 0:  # type: ignore
#         raise Http404()

#     page_title = f"{page_obj[0].tags.first().name} - tags"  # type: ignore

#     return render(
#         request,
#         "blog/pages/index.html",
#         {"page_obj": page_obj, "page_title": page_title},
#     )


class SearchListView(PostListView):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        # Não é possível usar self.request.GET.get() aqui pois o request ainda não foi criado. Por isso é necessário usar o metodo setup
        self._search_value: str = ""

    # setup tem um comportamento parecido com o hook useEffect do React para pegar contexts de html
    def setup(self, request: HttpRequest, *args: Any, **kwargs: Any) -> None:
        # query params = ?search=valor
        self._search_value = request.GET.get("search", "").strip()
        return super().setup(request, *args, **kwargs)

    def get_queryset(self) -> QuerySet[Any]:
        # icontains = contém
        return (
            super()
            .get_queryset()
            .filter(
                Q(title__icontains=self._search_value)
                | Q(excerpt__icontains=self._search_value)
                | Q(content__icontains=self._search_value)
            )[:PER_PAGE]
        )

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        search_title = f"Busca por '{self._search_value[:20]}'"
        context.update(
            {
                "search_value": self._search_value,
                "page_title": search_title,
            }
        )
        return context

    def get(
        self, request: HttpRequest, *args: Any, **kwargs: Any
    ) -> HttpResponse:
        if self._search_value == "":
            return redirect("blog:index")
        return super().get(request, *args, **kwargs)


# def search(request: HttpRequest):
#     # query params = ?search=valor
#     search_value = request.GET.get("search", "").strip()
#     # icontains = contém
#     posts = Post.objects.get_published().filter(  # type: ignore
#         Q(title__icontains=search_value)
#         | Q(excerpt__icontains=search_value)
#         | Q(content__icontains=search_value)
#     )[:PER_PAGE]

#     search_title = f"Busca por '{search_value[:20]}'"

#     return render(
#         request,
#         "blog/pages/index.html",
#         {
#             "page_obj": posts,
#             "search_value": search_value,
#             "page_title": search_title,
#         },
#     )
