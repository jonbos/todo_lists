from selenium import webdriver
from .base import FunctionalTest


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
        self.add_list_item('Miriam Makeba')

        #He notices a share this list option
        share_box = self.browser.find_element_by_css_selector('input[name="sharee"]')

        self.assertEqual(share_box.get_attribute('placeholder'), 'your-friend@example.com')