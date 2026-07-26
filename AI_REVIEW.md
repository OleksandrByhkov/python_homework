# AI Code Review

Цей документ містить AI-assisted code review трьох views з Django-проєкту "Книжковий магазин".

Code review було виконано за допомогою ChatGPT.
Усі рекомендації AI були перевірені вручну перед застосуванням.

---

# 1. BookListView

## Оригінальний код

```python
class BookListView(ListView):
    model = Book
    template_name = "catalog/book_list.html"
    context_object_name = "books"
    paginate_by = 5

    def get_queryset(self):
        queryset = Book.objects.select_related("category").all()

        search = self.request.GET.get("search")
        category = self.request.GET.get("category")
        available = self.request.GET.get("available")

        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(author__icontains=search) |
                Q(description__icontains=search)
            )

        if category:
            queryset = queryset.filter(category_id=category)

        if available == "on":
            queryset = queryset.filter(stock__gt=0)

        return queryset.order_by("title")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["categories"] = Category.objects.all()
        context["search"] = self.request.GET.get("search", "")
        context["selected_category"] = self.request.GET.get("category", "")
        context["available"] = self.request.GET.get("available", "")

        return context
```

## Рекомендації AI

Під час перевірки коду ChatGPT запропонував:

- прибрати зайвий виклик `.all()` після `select_related()`;
- використовувати `.strip()` для пошукового запиту, щоб ігнорувати зайві пробіли;
- залишити `select_related("category")` для оптимізації SQL-запитів;
- залишити сортування `order_by("title")` для стабільної пагінації;
- додати docstring з описом призначення view.

## Застосовані зміни

Рекомендації були перевірені вручну та визнані доцільними.

Було прибрано зайвий `.all()`, додано `.strip()` для пошукового запиту та docstring.

## Фінальний код

```python
class BookListView(ListView):
    """
    Display a paginated list of books.

    Supports searching by title, author and description,
    filtering by category and showing only available books.
    """

    model = Book
    template_name = "catalog/book_list.html"
    context_object_name = "books"
    paginate_by = 5

    def get_queryset(self):
        queryset = Book.objects.select_related("category")

        search = self.request.GET.get("search", "").strip()
        category = self.request.GET.get("category")
        available = self.request.GET.get("available")

        if search:
            queryset = queryset.filter(
                Q(title__icontains=search)
                | Q(author__icontains=search)
                | Q(description__icontains=search)
            )

        if category:
            queryset = queryset.filter(category_id=category)

        if available == "on":
            queryset = queryset.filter(stock__gt=0)

        return queryset.order_by("title")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["categories"] = Category.objects.all()
        context["search"] = self.request.GET.get("search", "")
        context["selected_category"] = self.request.GET.get("category", "")
        context["available"] = self.request.GET.get("available", "")

        return context
```

---

# 2. order_create

## Оригінальний код

```python
def order_create(request):
    cart = Cart(request)

    if len(cart) == 0:
        return redirect("catalog:book_list")

    if request.method == "POST":
        form = OrderCreateForm(request.POST)

        if form.is_valid():
            with transaction.atomic():
                order = form.save(commit=False)

                if request.user.is_authenticated:
                    order.user = request.user

                order.save()

                for item in cart:
                    OrderItem.objects.create(
                        order=order,
                        book=item["book"],
                        price=item["price"],
                        quantity=item["quantity"],
                    )

                send_mail(
                    subject=f"Замовлення #{order.id} створено",
                    message=f"Ваше замовлення #{order.id} успішно створено.",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[order.email],
                    fail_silently=True,
                )

                stripe.api_key = settings.STRIPE_SECRET_KEY

                checkout_session = stripe.checkout.Session.create(
                    payment_method_types=["card"],
                    mode="payment",
                    customer_email=order.email,
                    line_items=[
                        {
                            "price_data": {
                                "currency": "uah",
                                "product_data": {
                                    "name": item["book"].title,
                                },
                                "unit_amount": int(item["price"] * 100),
                            },
                            "quantity": item["quantity"],
                        }
                        for item in cart
                    ],
                    success_url=request.build_absolute_uri(
                        reverse("catalog:payment_success")
                    ),
                    cancel_url=request.build_absolute_uri(
                        reverse("catalog:payment_cancel")
                    ),
                    metadata={
                        "order_id": order.id,
                    },
                )

                order.stripe_session_id = checkout_session.id
                order.save()

                cart.clear()

                return redirect(checkout_session.url)

    else:
        form = OrderCreateForm()

    return render(request, "catalog/order_create.html", {
        "cart": cart,
        "form": form,
    })
```

## Рекомендації AI

Під час перевірки коду ChatGPT запропонував:

- не виконувати Stripe-запити та відправлення email всередині `transaction.atomic()`;
- залишити всередині транзакції тільки операції з базою даних;
- використовувати `bulk_create()` для створення декількох `OrderItem`;
- використовувати `update_fields` при оновленні тільки `stripe_session_id`;
- додати docstring з описом функції;
- продовжити використовувати mock для Stripe та email у тестах.

## Застосовані зміни

Рекомендації були перевірені вручну та застосовані.

Створення `Order` та `OrderItem` залишено всередині транзакції бази даних.

Виклики Stripe та відправлення email винесено за межі `transaction.atomic()`.

Для створення позицій замовлення використано `bulk_create()`.

При оновленні `stripe_session_id` використовується `update_fields=["stripe_session_id"]`.

## Фінальний код

```python
def order_create(request):
    """
    Create an order from the current shopping cart.

    Validates customer data, creates the order and its items,
    sends a confirmation email, creates a Stripe Checkout Session
    and clears the shopping cart.
    """

    cart = Cart(request)

    if len(cart) == 0:
        return redirect("catalog:book_list")

    if request.method == "POST":
        form = OrderCreateForm(request.POST)

        if form.is_valid():
            with transaction.atomic():
                order = form.save(commit=False)

                if request.user.is_authenticated:
                    order.user = request.user

                order.save()

                order_items = []

                for item in cart:
                    order_items.append(
                        OrderItem(
                            order=order,
                            book=item["book"],
                            price=item["price"],
                            quantity=item["quantity"],
                        )
                    )

                OrderItem.objects.bulk_create(order_items)

            send_mail(
                subject=f"Замовлення #{order.id} створено",
                message=f"Ваше замовлення #{order.id} успішно створено.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[order.email],
                fail_silently=True,
            )

            stripe.api_key = settings.STRIPE_SECRET_KEY

            checkout_session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                mode="payment",
                customer_email=order.email,
                line_items=[
                    {
                        "price_data": {
                            "currency": "uah",
                            "product_data": {
                                "name": item["book"].title,
                            },
                            "unit_amount": int(item["price"] * 100),
                        },
                        "quantity": item["quantity"],
                    }
                    for item in cart
                ],
                success_url=request.build_absolute_uri(
                    reverse("catalog:payment_success")
                ),
                cancel_url=request.build_absolute_uri(
                    reverse("catalog:payment_cancel")
                ),
                metadata={
                    "order_id": order.id,
                },
            )

            order.stripe_session_id = checkout_session.id
            order.save(update_fields=["stripe_session_id"])

            cart.clear()

            return redirect(checkout_session.url)

    else:
        form = OrderCreateForm()

    return render(
        request,
        "catalog/order_create.html",
        {
            "cart": cart,
            "form": form,
        },
    )
```

---

# 3. AsyncBookDetailView

## Оригінальний код

```python
class AsyncBookDetailView(View):
    async def get(self, request, pk):
        book = await Book.objects.select_related("category").aget(pk=pk)

        return render(
            request,
            "catalog/async_book_detail.html",
            {"book": book},
        )
```

## Рекомендації AI

Під час перевірки коду ChatGPT запропонував:

- обробити ситуацію, коли книги з переданим `pk` не існує;
- перехоплювати виняток `Book.DoesNotExist`;
- повертати стандартну HTTP-помилку 404 замість необробленого винятку;
- залишити `select_related("category")` для оптимізації запиту;
- додати docstring.

## Застосовані зміни

Рекомендації були перевірені вручну та застосовані.

Тепер, якщо книга не існує, `Book.DoesNotExist` перетворюється на стандартну HTTP-помилку 404.

Для цього до імпортів у `catalog/views.py` було додано `Http404`.

## Фінальний код

```python
class AsyncBookDetailView(View):
    """
    Display detailed information about a book asynchronously.

    Returns HTTP 404 when the requested book does not exist.
    """

    async def get(self, request, pk):
        try:
            book = await Book.objects.select_related("category").aget(pk=pk)
        except Book.DoesNotExist as exc:
            raise Http404("Book not found") from exc

        return render(
            request,
            "catalog/async_book_detail.html",
            {"book": book},
        )
```

---

# Результати тестування

Після застосування AI-рекомендацій було запущено всі автоматичні тести.

Результат:

```text
43 passed
```

Coverage моделей:

```text
Name                Stmts   Miss   Cover
----------------------------------------
catalog\models.py      48      0    100%
----------------------------------------
TOTAL                  48      0    100%
```

Coverage всього проєкту:

```text
TOTAL    735    61    92%
```

Вимога завдання щодо coverage не менше 60% виконана.

Coverage моделей становить **100%**, а загальний coverage проєкту — **92%**.