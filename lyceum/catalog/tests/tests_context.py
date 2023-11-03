from django.db.models.query import QuerySet
import django.test
from django.urls import reverse

import catalog.models

__all__ = []


class ContextTests(django.test.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.published_category = catalog.models.Category.objects.create(
            is_published=True,
            name="Тестовая опубликованная категория",
            slug="test-cat-pub-slug",
            weight=100,
        )
        cls.unpublished_category = catalog.models.Category.objects.create(
            is_published=False,
            name="Тестовая неопубликованная категория",
            slug="test-cat-unpub-slug",
            weight=100,
        )
        cls.published_tag = catalog.models.Tag.objects.create(
            is_published=True,
            name="Тестовый опубликованный тэг",
            slug="test-tag-pub-slug",
        )
        cls.unpublished_tag = catalog.models.Tag.objects.create(
            is_published=False,
            name="Тестовый неопубликованный тэг",
            slug="test-tag-unpub-slug",
        )
        cls.published_item = catalog.models.Item(
            name="Опубликованный товар",
            category=cls.published_category,
            text="роскошно",
            is_published=True,
        )
        cls.unpublished_item = catalog.models.Item(
            name="Неопубликованный товар",
            category=cls.published_category,
            text="роскошно",
            is_published=False,
        )
        cls.published_category.save()
        cls.unpublished_category.save()

        cls.published_tag.save()
        cls.unpublished_tag.save()

        cls.published_item.full_clean()
        cls.published_item.save()
        cls.published_item.tags.add(cls.published_tag)

        cls.unpublished_item.full_clean()
        cls.unpublished_item.save()
        cls.unpublished_item.tags.add(cls.published_tag)

    def test_catalog_item_list_correct_context(self):
        response = django.test.Client().get(reverse("catalog:item_list"))
        self.assertIn(
            "items",
            response.context,
            msg="В контексте отсутсвует items",
        )
        self.assertIsInstance(response.context["items"], QuerySet)

    def test_correct_item_count_show(self):
        response = django.test.Client().get(reverse("catalog:item_list"))
        items = response.context["items"]
        self.assertEqual(
            len(items),
            1,
            msg="Товаров отображается больше чем нужно,"
            "возможно не работает логика is_published",
        )

    def test_correct_item_count_show_plus_one(self):
        self.assertFalse(
            self.unpublished_item.is_published,
            msg="У неопубликованного товара статус опубликованного",
        )

        self.unpublished_item.is_published = True
        self.unpublished_item.save()

        response = self.client.get(reverse("catalog:item_list"))
        items = response.context["items"]
        self.assertEqual(
            items.count(),
            2,
            msg="Товары отображаются неверно,"
            "возможно не работает логика is_published",
        )

        self.unpublished_item.is_published = False
        self.unpublished_item.save()

        self.assertFalse(
            self.unpublished_item.is_published,
            msg="У неопубликованного товара статус опубликованного после",
        )

    def test_correct_show_with_unpub_category(self):
        self.assertTrue(
            self.published_item.category.is_published,
            msg="У опубликованной категории статус неопубликованного",
        )

        self.published_item.category = self.unpublished_category
        self.published_item.save()

        response = self.client.get(reverse("catalog:item_list"))
        items = response.context["items"]
        self.assertEqual(
            items.count(),
            0,
            msg="Товары отображаются неверно,"
            "возможно не работает логика is_published категорий",
        )

        self.published_item.category = self.published_category
        self.published_item.save()

        self.assertTrue(
            self.published_item.category.is_published,
            msg="У опубликованной категории статус неопубликованного после",
        )
