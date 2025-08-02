from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class FooterPage(BasePage):
    FOOTER_LINKS = (By.XPATH, "//div[@class='footer']//ul//li/a")

    def get_footer_links(self):
        return self.get_elements(self.FOOTER_LINKS)

    def click_and_validate_links(self):
        links = self.get_footer_links()
        results = []
        for i in range(len(links)):
            links = self.get_footer_links()
            link = links[i]
            text = link.text
            href = link.get_attribute("href")
            self.scroll_to_element(link)
            link.click()

            current_url = self.driver.current_url
            success = href in current_url or text.lower().replace(" ", "-") in current_url
            results.append((text, href, current_url, success))

            self.driver.back()
        return results
