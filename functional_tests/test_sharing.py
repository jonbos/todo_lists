from selenium import webdriver
from .base import FunctionalTest
from .list_page import ListPage
from .my_lists_page import MyListsPage


def quit_if_possible(browser):
    try:
        browser.quit()
    except:
        pass


class SharingTest(FunctionalTest):

    def test_can_share_list_with_another_user(self):
        # Juan is a logged-in user
        self.create_pre_authenticated_session(email='juan@example.com')
        juan_browser = self.browser
        self.addCleanup(lambda: quit_if_possible(juan_browser))

        # His friend Matt is also hanging out on the lists site
        matt_browser = webdriver.Firefox()
        self.addCleanup(lambda: quit_if_possible(matt_browser))
        self.browser = matt_browser
        self.create_pre_authenticated_session(email='matt@matt.com')

        # Juan goes to the site and starts a list
        self.browser = juan_browser
        self.browser.get(self.live_server_url)
        list_page = ListPage(self).add_list_item('Miriam Makebe')

        # He notices a share this list option
        share_box = list_page.get_share_box()

        self.assertEqual(share_box.get_attribute(
            'placeholder'), 'your-friend@example.com')

        # She shares her list, the page updates to say it's shared with Matt
        list_page.share_list_with('matt@matt.com')

        # Matt goes to the home page with his browser
        self.browser = matt_browser
        MyListsPage(self).go_to_my_lists_page()

        # He sees Juan's list is in there
        self.browser.find_element_by_link_text('Miriam Makebe').click()

        # On the list page, Matt can see says that it's Jon's list
        self.wait_for(lambda: self.assertEqual(
            list_page.get_list_owner(), 'juan@example.com'))

        # He adds an item to the list
        list_page.add_list_item('Hola, Juan!')

        #When Juan visits the list, he sees the list item added by Matt
        self.browser=juan_browser
        self.browser.refresh()
        list_page.wait_for_row_in_list_table('Hola, Juan!', 2)