# AI Prompts

У цьому файлі зібрані промпти, які використовувалися під час виконання завдання з AI-assisted development для проєкту "Книжковий магазин".

---

## 1. Code Review — BookListView

### Prompt

```text
Review this Django BookListView.

Check:
- code quality;
- database query efficiency;
- readability;
- filtering and search implementation;
- pagination stability;
- possible improvements.

Do not change the existing functionality.

Provide:
1. Problems or possible improvements.
2. Explanation for each recommendation.
3. Improved final version of the code.
```

---

## 2. Code Review — order_create

### Prompt

```text
Review this Django order_create view.

The view:
- creates an Order;
- creates OrderItem objects;
- uses transaction.atomic;
- sends confirmation email;
- creates a Stripe Checkout Session;
- clears the shopping cart.

Check:
- database transaction usage;
- performance;
- Stripe integration structure;
- email handling;
- database query efficiency;
- maintainability.

Do not change the expected user flow.

Provide recommendations and an improved version of the code.
```

---

## 3. Code Review — AsyncBookDetailView

### Prompt

```text
Review this asynchronous Django view that retrieves a Book using Django async ORM.

Check:
- async ORM usage;
- error handling;
- 404 handling;
- query efficiency;
- readability.

Suggest improvements without changing the purpose of the view.
```

---

## 4. Генерація тестів для моделей

### Prompt

```text
Generate pytest-django tests for the Django bookstore project.

Create additional tests for these models:
- Book;
- Order;
- OrderItem.

Use factory-boy factories where appropriate.

Test:
- object creation;
- __str__ methods;
- default values;
- relationships;
- OrderItem.get_cost();
- Order.get_total_cost().

Each AI-generated test must contain this comment:

# Generated with AI, reviewed and modified

The tests must be compatible with pytest-django.
```

---

## 5. Генерація docstrings

### Prompt

```text
Generate clear and concise Python docstrings for all Django views in the project.

The project contains:
- class-based views;
- function-based views;
- asynchronous views;
- authentication views;
- cart views;
- order and payment views.

Do not modify the application logic.
Only add docstrings that explain the purpose and behavior of each view.
```

---

## 6. README

### Prompt

```text
Create a README for a Django bookstore project.

The README should include:
- project description;
- main features;
- technologies;
- installation instructions;
- running the project;
- running tests;
- coverage;
- project structure;
- AI Usage section.

In the AI Usage section explain that ChatGPT was used for:
- code review;
- test generation;
- docstrings;
- documentation.

Mention that all AI-generated recommendations were manually reviewed before being applied.
```

---

# AI Tool

Для виконання завдання використовувався:

```text
ChatGPT
```

AI використовувався як допоміжний інструмент для аналізу та покращення коду.

Усі запропоновані зміни були перевірені вручну перед додаванням до проєкту.