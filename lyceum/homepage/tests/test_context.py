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
            is_on_main=True,
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

    def test_homepage_item_list_correct_context(self):
        response = django.test.Client().get(reverse("homepage:home"))
        self.assertIn(
            "items",
            response.context,
            msg="В контексте отсутсвует items",
        )
        self.assertIsInstance(response.context["items"], QuerySet)

    def test_correct_item_count_show(self):
        response = django.test.Client().get(reverse("homepage:home"))
        items = response.context["items"]
        self.assertEqual(len(items), 1)

    def test_correct_context_content(self):
        response = self.client.get(reverse("homepage:home"))
        items = response.context["items"]

        self.assertNotEqual(len(items), 0, msg="в контект не попадают данные")

        content = ("name", "text", "category_id", "_prefetched_objects_cache")
        item = items[0]
        for field in content:
            with self.subTest(field=field):
                self.assertIn(field, item.__dict__)

        bad_content = ("is_published", "is_on_main", "main_image_id")
        for field in bad_content:
            with self.subTest(field=field):
                self.assertNotIn(field, item.__dict__)

    def test_correct_context_content_in_prefetch(self):
        response = self.client.get(reverse("homepage:home"))
        items = response.context["items"]

        self.assertNotEqual(len(items), 0, msg="в контект не попадают данные")

        item = items[0]

        self.assertIn(
            "_prefetched_objects_cache",
            item.__dict__,
            msg="В товаре нет prefetched объектов",
        )

        self.assertIn("tags", item.__dict__["_prefetched_objects_cache"])
        self.assertNotIn("images", item.__dict__["_prefetched_objects_cache"])
