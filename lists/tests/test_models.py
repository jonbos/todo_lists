from django.test import TestCase
from django.core.exceptions import ValidationError
from lists.models import Item, List
from django.contrib.auth import get_user_model
User = get_user_model()


class ListModelTest(TestCase):
    def test_get_absolute_URL(self):
        list_ = List.objects.create()
        self.assertEqual(list_.get_absolute_url(), f'/lists/{list_.id}/')

    def test_create_new_creates_list_and_first_item(self):
        List.create_new(first_item_text='new item text')
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'new item text')
        new_list = List.objects.first()
        self.assertEqual(new_item.list, new_list)

    def test_creates_new_optionally_saves_owner(self):
        user = User.objects.create()
        List.create_new(first_item_text='new item text', owner=user)
        new_list = List.objects.first()
        self.assertEqual(new_list.owner, user)

    def test_lists_can_have_owners(self):
        List(owner=User())  # should not raise

    def test_list_owner_is_optional(self):
        List().full_clean()  # should not raise

    def test_create_new_returns_new_list_object(self):
        returned = List.create_new(first_item_text='new item text')
        new_list = List.objects.first()
        self.assertEqual(returned, new_list)

    def test_list_name_is_first_item_on_list(self):
        list_ = List.objects.create()
        Item.objects.create(text='first item', list=list_)
        Item.objects.create(text='second item', list=list_)
        self.assertEqual(list_.name, 'first item')

    def test_adding_user_to_shared_with_saves_user_to_list(self):
        list_ = List.objects.create()
        correct_user = User.objects.create(email='a@b.com')
        incorrect_user = User.objects.create(email='bad@wrong.com')

        list_.shared_with.add(correct_user)
        print(list_.shared_with.all())
        self.assertIn(correct_user, list_.shared_with.all())
        self.assertNotIn(incorrect_user, list_.shared_with.all())



class ItemModelTest(TestCase):

    def test_default_text(self):
        item = Item()
        self.assertEqual(item.text, "")

    def test_item_is_related_to_list(self):
        list_ = List.objects.create()
        item = Item()
        item.list = list_
        item.save()
        self.assertIn(item, list_.item_set.all())

    def test_cannot_save_empty_list_items(self):
        list_ = List.objects.create()
        empty_item = Item(list=list_, text='')
        with self.assertRaises(ValidationError):
            empty_item.full_clean()
            empty_item.save()

    def test_duplicate_items_are_invalid(self):

        list_ = List.objects.create()
        Item.objects.create(list=list_, text='dup')

        with self.assertRaises(ValidationError):
            item = Item(list=list_, text='dup')
            item.full_clean()
            item.save()

    def test_CAN_save_identical_items_to_diffrent_list(self):
        first_list = List.objects.create()
        second_list = List.objects.create()

        Item.objects.create(list=first_list, text='dup')
        item = Item(list=second_list, text='dup')

        # should not raise
        item.full_clean()

    def test_list_ordering(self):
        list1 = List.objects.create()
        item1 = Item.objects.create(list=list1, text='i1')
        item2 = Item.objects.create(list=list1, text='item 2')
        item3 = Item.objects.create(list=list1, text='3')
        self.assertEqual(
            list(Item.objects.all()),
            [item1, item2, item3]
        )

    def test_item_string_representation(self):
        item = Item(text='Some text')
        self.assertEqual(str(item), 'Some text')
