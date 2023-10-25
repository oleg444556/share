import django.core.exceptions
import django.db
import django.test
from django.urls import reverse

import catalog.models

__all__ = ["ModelTests", "StaticUrlTests"]


class StaticUrlTests(django.test.TestCase):
    # test for catalog items
    def test_catalog_item_list_endpoint(self):
        response = django.test.Client().get(reverse("catalog:item_list"))
        self.assertEqual(response.status_code, 200)

    def test_catalog_item_detail_endpoint(self):
        # test for catalog item details
        response = django.test.Client().get(
            reverse("catalog:item_detail", args=["1"]),
        )
        self.assertEqual(response.status_code, 200)

    def test_re_exp_correct_status_catalog_endpoint(self):
        # test for correct re_path request
        response = django.test.Client().get(
            reverse("catalog:catalog_re", args=["100"]),
        )
        self.assertEqual(response.status_code, 200)

    def test_re_exp_correct_content_catalog_endpoint(self):
        # test for correct re_path request, for content of response
        response = django.test.Client().get(
            reverse("catalog:catalog_re", args=["100"]),
        )
        text = response.content.decode("utf-8")
        self.assertEqual(text, "<body>100</body>")

    def test_converter_status_catalog_endpoint(self):
        # test for correct request
        response = django.test.Client().get(
            reverse("catalog:catalog_converter", args=["100"]),
        )
        self.assertEqual(response.status_code, 200)

    def test_converter_content_catalog_endpoint(self):
        # test for correct converter request, for content of response
        response = django.test.Client().get(
            reverse("catalog:catalog_converter", args=["100"]),
        )
        text = response.content.decode("utf-8")
        self.assertEqual(text, "<body>100</body>")


class ModelTests(django.test.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.category = catalog.models.Category.objects.create(
            is_published=True,
            name="Тестовая категория",
            slug="test-cat-slug",
            weight=100,
        )
        cls.tag = catalog.models.Tag.objects.create(
            is_published=True,
            name="Тестовый тэг",
            slug="test-tag-slug",
        )

    def test_unable_to_create_must_contain(self):
        item_count = catalog.models.Item.objects.count()
        with self.assertRaises(django.core.exceptions.ValidationError):
            self.item = catalog.models.Item(
                name="Тестовый товар",
                category=self.category,
                text="qwertyроскошно",
            )
            self.item.full_clean()
            self.item.save()
            self.item.tags.add(ModelTests.tag)

        self.assertEqual(catalog.models.Item.objects.count(), item_count)

    def test_able_to_create_must_contain_roskoshno(self):
        item_count = catalog.models.Item.objects.count()
        self.item = catalog.models.Item(
            name="Тестовый товар",
            category=self.category,
            text="Нет слова роскошно",
        )
        self.item.full_clean()
        self.item.save()
        self.item.tags.add(ModelTests.tag)

        self.assertEqual(catalog.models.Item.objects.count(), item_count + 1)

    def test_able_to_create_must_contain_prevoshodno(self):
        item_count = catalog.models.Item.objects.count()
        self.item = catalog.models.Item(
            name="Тестовый товар",
            category=self.category,
            text="Нет слова превосходно",
        )
        self.item.full_clean()
        self.item.save()
        self.item.tags.add(ModelTests.tag)

        self.assertEqual(catalog.models.Item.objects.count(), item_count + 1)

    def test_unable_to_create_category_32768_weight(self):
        category_count = catalog.models.Category.objects.count()
        with self.assertRaises(django.core.exceptions.ValidationError):
            self.category_test = catalog.models.Category(
                name="Тестововая категория",
                slug="test_category_slug",
                weight=32768,
            )
            self.category_test.full_clean()
            self.category_test.save()

        self.assertEqual(
            catalog.models.Category.objects.count(),
            category_count,
        )

    def test_able_to_create_must_contain_monini(self):
        item_count = catalog.models.Item.objects.count()
        self.item = catalog.models.Item(
            name="Тестовый товар",
            category=self.category,
            text="Нет слова унинянимонини",
        )
        self.item.full_clean()
        self.item.save()
        self.item.tags.add(ModelTests.tag)

        self.assertEqual(catalog.models.Item.objects.count(), item_count + 1)

    # Тесты для всех схожих букв в алфавитах
    def test_unable_to_create_tags_similar_names_x(self):
        tags_count = catalog.models.Tag.objects.count()
        with self.assertRaises(django.core.exceptions.ValidationError):
            self.tag1 = catalog.models.Tag(name="х", slug="russkay")
            self.tag1.full_clean()
            self.tag1.save()
            self.tag2 = catalog.models.Tag(name="X", slug="english")
            self.tag2.full_clean()
            self.tag2.save()

        self.assertEqual(tags_count + 1, catalog.models.Tag.objects.count())

    def test_unable_to_create_tags_similar_names_p(self):
        tags_count = catalog.models.Tag.objects.count()
        with self.assertRaises(django.core.exceptions.ValidationError):
            self.tag1 = catalog.models.Tag(name="р", slug="russkay")
            self.tag1.full_clean()
            self.tag1.save()
            self.tag2 = catalog.models.Tag(name="p", slug="english")
            self.tag2.full_clean()
            self.tag2.save()

        self.assertEqual(tags_count + 1, catalog.models.Tag.objects.count())

    def test_unable_to_create_category_similar_name(self):
        cat_count = catalog.models.Category.objects.count()
        with self.assertRaises(django.core.exceptions.ValidationError):
            self.cat1 = catalog.models.Category(
                name="Кат Егория",
                slug="russkay",
            )
            self.cat1.full_clean()
            self.cat1.save()
            self.cat2 = catalog.models.Category(
                name="катего рия__",
                slug="english",
            )
            self.cat2.full_clean()
            self.cat2.save()

        self.assertEqual(
            cat_count + 1,
            catalog.models.Category.objects.count(),
        )
