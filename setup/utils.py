from datetime import datetime, timedelta
import json
import random
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from setup.smooth_scroll import SmoothScroll
from selenium.common.exceptions import ElementNotInteractableException
from data.agents_data import desk_agents
from data.utms import main_page, utms
from data.agents_data import ios_versions, apple_crios_versions, apple_fxios_versions, apple_edgios_versions


def target_url(add_utm):
    if add_utm:
        base_url = random.choice(main_page)
        utm_param = random.choice(utms)

        return f"{base_url}{utm_param}"
    else:
        return random.choice(main_page)


def get_mobile_user_agent(device, browser_name):

    if device["deviceMetrics"]["isiOS"]:
        if browser_name == "chrome":
            browser_ios_name = "CriOS"
            browser_version = random.choice(apple_crios_versions)
        elif browser_name == "firefox":
            browser_ios_name = "Fxios"
            browser_version = random.choice(apple_fxios_versions)
        elif browser_name == "edge":
            browser_ios_name = "Edgios"
            browser_version = random.choice(apple_edgios_versions)

        ios_version = random.choice(ios_versions)
        user_agent = f"Mozilla/5.0 (iPhone; CPU iPhone OS {ios_version} like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) {browser_ios_name}/{browser_version} Mobile/15E148 Safari/604.1"

    else:
        android_version = random.choice(range(9, 15))
        chrome_version = random.choice(apple_crios_versions)
        model = device["deviceMetrics"]["model"]
        user_agent = f"Mozilla/5.0 (Linux; Android {android_version}; {model}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_version} Mobile Safari/537.36"

    return user_agent


def get_desk_user_agent():
    return random.choice(desk_agents)


def adjust_dimensions(device, browser_deltas, browser_name):
    delta = browser_deltas.get(browser_name, {"width": 0, "height": 0})
    width = round((device["deviceMetrics"]["width"] +
                  delta["width"]) / device["deviceMetrics"]["pixelRatio"])
    height = round((device["deviceMetrics"]["height"] +
                   delta["height"]) / device["deviceMetrics"]["pixelRatio"])
    return width, height


def set_window_size(driver, device, browser_deltas, browser_name):
    width, height = adjust_dimensions(device, browser_deltas, browser_name)
    driver.set_window_size(width, height)


def scroll_to_single(driver, target_selector):
    navigator = SmoothScroll(driver)
    navigator.scroll_to_single_element(target_selector)


def scroll_to_multi_or_end(driver, speed, target_selector=None):
    navigator = SmoothScroll(driver, speed=speed)
    navigator.navigate_and_scroll(target_selector)


def random_wait():
    sec = random.randint(1, 3)
    sleep(sec)


def load_locators(calculator_name):
    with open("data/calculator_locators.json", "r") as f:
        all_locators = json.load(f)
    calculator_locators = all_locators.get(calculator_name, {}).copy()

    # Merge shared locators if defined
    if "Shared" in calculator_locators:
        shared_key = calculator_locators["Shared"]
        shared_locators = all_locators["SharedLocators"].get(shared_key, {})
        calculator_locators = {
            **shared_locators,
            **calculator_locators.get("NewField", {}),
            **calculator_locators
        }

    # Add CurrencyIcons from Common section
    common_currency_icons = all_locators["Common"].get("CurrencyIcons", [])
    calculator_locators.update({
        "CurrencyIcons": common_currency_icons,
    })
    return calculator_locators


def select_random_currency(driver, locators):
    currency_icons = locators.get("CurrencyIcons", [])
    random_currency = random.choice(currency_icons)
    currency_locator = (By.CSS_SELECTOR, random_currency["locator"])

    currency_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(currency_locator)
    )
    sleep(1)
    if currency_button.is_displayed():
        currency_button.click()
        currency_button.click()


def scroll_to_calculate_button(driver, locator):
    element = driver.find_element(
        By.CSS_SELECTOR, locator)
    driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", element)


def fill_input(driver, locator, value, retry_count=3):
    for attempt in range(retry_count):
        try:
            element = driver.find_element(By.CSS_SELECTOR, locator)
            driver.execute_script(
                "arguments[0].setAttribute('type', 'text');", element)

            if element.is_displayed() and element.is_enabled():
                element.clear()
                element.send_keys(str(value))
                sleep(0.5)
                return
            else:
                raise ElementNotInteractableException(
                    "Element not interactable.")
        except ElementNotInteractableException as e:
            print(f"Attempt {attempt + 1} failed")
            if attempt < retry_count - 1:
                driver.refresh()
                sleep(3)
                select_random_currency(driver, "label[for='btnradio4']")
            else:
                print("Max retries reached. Failing the test.")
                raise
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise


def select_dropdown(driver, locator, value, by=By.CSS_SELECTOR):
    dropdown = Select(driver.find_element(by, locator))

    try:
        dropdown.select_by_visible_text(value)
    except Exception:
        try:
            dropdown.select_by_value(value)
        except Exception as e:
            print(f"Failed to select '{value}' from dropdown: {e}")


def calculate_button(driver, locator):
    button = driver.find_element(By.CSS_SELECTOR, locator)

    if button.is_displayed() and button.is_enabled():
        button.click()
    else:
        driver.execute_script("arguments[0].click();", button)


def click_element(driver, locator, by=By.XPATH):
    element = driver.find_element(by, locator)
    if element.is_displayed():
        element.click()


def get_random_number(min_value, max_value):
    if min_value > max_value:
        raise ValueError("min_value should not be greater than max_value.")

    return random.randint(min_value, max_value)


def get_random_date():
    today = datetime.now()
    earliest_date = today - timedelta(days=15 * 365)

    random_days = random.randint(0, (today - earliest_date).days)
    random_date = earliest_date + timedelta(days=random_days)

    return random_date.strftime("%Y-%m-%d")


def fill_date_input(driver, locator, date):
    element = driver.find_element(By.CSS_SELECTOR, locator)

    driver.execute_script(
        "arguments[0].setAttribute('type', 'text');", element)

    if element.is_displayed() and element.is_enabled():
        element.clear()
        element.send_keys(date)
    else:
        ActionChains(driver).move_to_element(element).click().perform()
        element.clear()
        element.send_keys(date)
    sleep(1)


def select_result(driver, locator):
    element = driver.find_element(By.CSS_SELECTOR, locator)
    driver.execute_script(
        "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
    sleep(1)

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(element))
    action = ActionChains(driver)
    action.move_to_element(element).pause(1).click().perform()
    random_wait()


def single_element_normal_scroll(driver, locator):
    element = driver.find_element(By.CSS_SELECTOR, locator)
    driver.execute_script(
        "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
    random_wait()


def link_clicks(driver):
    topic_element = 'ul.content-paragraph'
    single_element_normal_scroll(driver, topic_element)

    ul_element = driver.find_element(By.CSS_SELECTOR, topic_element)
    li_elements = ul_element.find_elements(By.TAG_NAME, 'li')
    index = get_random_number(0, len(li_elements) - 1)

    random_li = li_elements[index]
    print(f"Clicking on: {random_li.text}")
    random_li.find_element(By.TAG_NAME, 'a').click()
    random_wait()
