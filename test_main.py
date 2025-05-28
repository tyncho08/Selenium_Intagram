import unittest
from unittest.mock import MagicMock, patch
from io import StringIO
import sys

# Import Keys from selenium.webdriver.common.keys
from selenium.webdriver.common.keys import Keys

from main import InstagramBot, print_same_line

class TestInstagramBot(unittest.TestCase):

    @patch('main.webdriver.Firefox')
    @patch('main.time.sleep')
    @patch('main.random.randint')
    @patch('sys.stdout', new_callable=StringIO)
    def setUp(self, mock_stdout, mock_randint, mock_sleep, mock_firefox):
        self.mock_driver = MagicMock()
        mock_firefox.return_value = self.mock_driver
        self.bot = InstagramBot("test_user", "test_password")
        # Ensure the bot uses the mock_driver instance
        self.bot.driver = self.mock_driver  

    def test_login(self):
        # Mock elements
        mock_login_button_element = MagicMock()
        mock_username_element = MagicMock()
        mock_password_element = MagicMock()

        # Configure find_element_by_xpath to return mock elements based on XPath
        def find_element_side_effect(xpath):
            if xpath == "//a[@href='/accounts/login/?source=auth_switcher']":
                return mock_login_button_element
            elif xpath == "//input[@name='username']":
                return mock_username_element
            elif xpath == "//input[@name='password']":
                return mock_password_element
            return MagicMock() # Default mock for other calls

        self.mock_driver.find_element_by_xpath.side_effect = find_element_side_effect
        
        self.bot.login()

        # Test driver.get call for login page
        self.mock_driver.get.assert_any_call("https://www.instagram.com/")

        # Test find_element_by_xpath calls
        self.mock_driver.find_element_by_xpath.assert_any_call("//a[@href='/accounts/login/?source=auth_switcher']")
        self.mock_driver.find_element_by_xpath.assert_any_call("//input[@name='username']")
        self.mock_driver.find_element_by_xpath.assert_any_call("//input[@name='password']")

        # Test send_keys calls
        mock_username_element.send_keys.assert_any_call("test_user")
        mock_password_element.send_keys.assert_any_call("test_password")

        # Test click call on login button
        mock_login_button_element.click.assert_called_once()
        
        # Test that Keys.RETURN is sent to the password field
        # Use the imported Keys
        mock_password_element.send_keys.assert_any_call(Keys.RETURN)


    def test_like_photo(self):
        hashtag = "test_hashtag"

        # Mock find_elements_by_tag_name to return mock anchor elements
        mock_anchor_element = MagicMock()
        mock_anchor_element.get_attribute.return_value = "https://www.instagram.com/p/test_photo_id"
        self.mock_driver.find_elements_by_tag_name.return_value = [mock_anchor_element]

        # Mock find_element_by_xpath for the like button
        mock_like_button_element = MagicMock()
        # Ensure this mock is returned only for the like button XPath
        self.mock_driver.find_element_by_xpath = MagicMock(side_effect=lambda x: mock_like_button_element if x == '//span[@aria-label="Like"]' else MagicMock())

        self.bot.like_photo(hashtag)

        # Test driver.get call for hashtag page
        self.mock_driver.get.assert_any_call("https://www.instagram.com/explore/tags/" + hashtag + "/")

        # Test execute_script call
        self.mock_driver.execute_script.assert_any_call("window.scrollTo(0, document.body.scrollHeight);")

        # Test find_elements_by_tag_name call
        self.mock_driver.find_elements_by_tag_name.assert_any_call('a')
        
        # Test driver.get call for photo page
        self.mock_driver.get.assert_any_call("https://www.instagram.com/p/test_photo_id")

        # Test find_element_by_xpath call for like button
        self.mock_driver.find_element_by_xpath.assert_any_call('//span[@aria-label="Like"]')

        # Test click call on like button
        mock_like_button_element.click.assert_called_once()

    def test_closeBrowser(self):
        self.bot.closeBrowser()
        self.mock_driver.close.assert_called_once()

if __name__ == '__main__':
    unittest.main()
