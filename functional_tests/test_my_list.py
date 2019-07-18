from django.conf import settings
from .base import FunctionalTest
from .server_tools import create_session_on_server
from .management.commands.create_session import create_pre_authenticated_session

import time


class MyListsTest(FunctionalTest):

    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        # Edith is a logged-in user
        self.create_pre_authenticated_session('edith@example.com')

        # She goes to the homepage and starts a list
        self.browser.get(self.live_server_url)
        self.add_list_item('Buy a motorcycle')
        self.add_list_item('Do a wheelie')
        first_list_url = self.browser.current_url

        # She notices a 'My lists' link for the first time
        self.browser.find_element_by_link_text('My Lists').click()

        # She sees that her list is in there,
        #named according to it's first list item
        self.wait_for(lambda: self.browser.find_element_by_link_text('Buy a motorcycle'))
        self.browser.find_element_by_link_text('Buy a motorcycle').click()
        self.wait_for(lambda: self.assertEqual(self.browser.current_url, first_list_url))

        #She starts another list
        self.browser.get(self.live_server_url)
        self.add_list_item('Buy a helmet')
        second_list_url = self.browser.current_url

        #Under my lists, her new list appears
        self.browser.find_element_by_link_text('My Lists').click()
        self.wait_for(lambda: self.browser.find_element_by_link_text('Buy a helmet'))
        self.browser.find_element_by_link_text('Buy a helmet').click()
        self.wait_for(lambda: self.assertEqual(self.browser.current_url, second_list_url))

        #She logs out. The 'my lists' option disappears
        self.browser.find_element_by_link_text('Log out').click()
        self.wait_for(lambda: self.assertEqual(self.browser.find_elements_by_link_text('My Lists'), []))

