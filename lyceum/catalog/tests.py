import django.core.exceptions
import django.test
from django.urls import reverse

from catalog import views
import catalog.models


class StaticUrlTests(django.test.TestCase):
    # test for catalog items
    def test_catalog_item_list_endpoint(self):
        response = django.test.Client().get(reverse(views.item_list))
        self.assertEqual(response.status_code, 200)

    def test_catalog_item_detail_endpoint(self):
        # test for catalog item details
        response = django.test.Client().get(
            reverse(views.item_detail, args=["1"])
        )
        self.assertEqual(response.status_code, 200)

    def test_re_exp_correct_status_catalog_endpoint(self):
        # test for correct re_path request
        response = django.test.Client().get(
            reverse(views.catalog_int_pos_num, args=["100"])
        )
        self.assertEqual(response.status_code, 200)

    def test_re_exp_correct_content_catalog_endpoint(self):
        # test for correct re_path request, for content of response
        response = django.test.Client().get(
            reverse(views.catalog_int_pos_num, args=["100"])
        )
        text = response.content.decode("utf-8")
        self.assertEqual(text, "<body>100</body>")

    def test_converter_status_catalog_endpoint(self):
        # test for correct request
        response = django.test.Client().get(
            reverse(views.catalog_converter_int_pos, args=["100"])
        )
        self.assertEqual(response.status_code, 200)

    def test_converter_content_catalog_endpoint(self):
        # test for correct converter request, for content of response
        response = django.test.Client().get(
            reverse(views.catalog_converter_int_pos, args=["100"])
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
            catalog.models.Category.objects.count(), category_count
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
