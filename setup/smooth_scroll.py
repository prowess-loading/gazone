import random
import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


class SmoothScroll:
    def __init__(self, driver, speed=20.0):
        self.driver = driver
        self.speed = speed

    def _smooth_scroll(self, current_position, next_position, scroll_step):

        for position in range(current_position, next_position, scroll_step):
            self.driver.execute_script(
                f"window.scrollTo(0, {max(0, position)});")
            time.sleep(random.uniform(0.02, 0.05))

    def _scroll_to_position(self, target_position, current_position, scrolling_up=False, toggle_up_once=False):

        while current_position != target_position:
            # Determine scroll direction and calculate scroll amount
            scroll_amount = (-random.randint(80, 200)
                             if scrolling_up else random.randint(200, 500))
            next_position = current_position + scroll_amount

            # Adjust scroll direction once reaching the target position
            if (scrolling_up and next_position <= target_position) or (not scrolling_up and next_position >= target_position):
                break  # Stop scrolling once the target position is reached

            scroll_step = int(scroll_amount / abs(scroll_amount) * self.speed)

            # Smooth scrolling with random pauses
            self._smooth_scroll(current_position, next_position, scroll_step)
            current_position = next_position

            # Pause randomly to mimic human-like behavior
            if random.random() < 0.02:
                time.sleep(random.uniform(1, 3))
            else:
                time.sleep(random.uniform(0.3, 0.6))

            # Occasionally toggle scroll direction
            if not scrolling_up and random.random() < 0.1 and not toggle_up_once:
                scrolling_up = True
                toggle_up_once = True
            elif scrolling_up and random.random() < 0.1:
                scrolling_up = False

            yield current_position

    def scroll(self, target_selector=None, scroll_to_end=False, by=By.CSS_SELECTOR):
        print("Scrolling scenario...")

        total_scroll_height = self.driver.execute_script(
            "return document.body.scrollHeight")
        current_position = self.driver.execute_script(
            "return window.pageYOffset;")
        scrolling_up = False
        toggle_up_once = False

        while True:
            if target_selector:
                try:
                    target_element = self.driver.find_element(
                        by, target_selector)
                    target_in_view = self.driver.execute_script(
                        "var rect = arguments[0].getBoundingClientRect();"
                        "return (rect.top >= 0 && rect.bottom <= window.innerHeight);",
                        target_element,
                    )
                    if target_in_view:
                        print("Target element is in view, Clicking...")
                        time.sleep(2)  # Simulate human-like delay
                        target_element.click()
                        break
                except NoSuchElementException:
                    pass

            # Perform scrolling with toggling logic
            for current_position in self._scroll_to_position(
                total_scroll_height if scroll_to_end else current_position,
                current_position,
                scrolling_up,
                toggle_up_once,
            ):
                # Break when reaching the final position
                if scroll_to_end and current_position >= total_scroll_height:
                    return

    def scroll_to_end_and_close(self):
        print("Scrolling to end and close scenario...")
        self.scroll(scroll_to_end=True)
        time.sleep(2)
        self.driver.quit()

    def scroll_down_then_up_and_click(self, target_selector, by=By.CSS_SELECTOR):
        print("Scrolling down, up and click scenario...")

        # Get total scroll height and current scroll position
        total_scroll_height = self.driver.execute_script(
            "return document.body.scrollHeight")
        current_position = self.driver.execute_script(
            "return window.pageYOffset;")

        # Phase 1: Scroll Down
        print("Phase 1: Scrolling down...")
        scrolling_up = False
        toggle_up_once = False

        for current_position in self._scroll_to_position(total_scroll_height, current_position, scrolling_up, toggle_up_once):

            if not scrolling_up and random.random() < 0.1:  # 10% chance to scroll up occasionally
                scrolling_up = True
                toggle_up_once = True

        # Hold for a random time at the bottom
        time.sleep(random.uniform(1, 3))

        # Phase 2: Scroll Up
        print("Phase 2: Scrolling up...")
        scrolling_up = True
        toggle_up_once = False

        for current_position in self._scroll_to_position(0, current_position, scrolling_up, toggle_up_once):

            if scrolling_up and random.random() < 0.1:
                scrolling_up = False

        time.sleep(random.uniform(2, 3))

        # Phase 3: Look for the target and scroll to it
        print("Phase 3: Scrolling to target element...")
        try:
            target_element = self.driver.find_element(by, target_selector)
            while True:
                target_in_view = self.driver.execute_script(
                    "var rect = arguments[0].getBoundingClientRect();"
                    "return (rect.top >= 0 && rect.bottom <= window.innerHeight);",
                    target_element,
                )
                if target_in_view:
                    print("Target element is in view, Clicking...")
                    # Simulate human-like delay
                    time.sleep(random.uniform(1, 2))
                    target_element.click()
                    break

                # Determine the target's position and adjust scrolling
                target_position = self.driver.execute_script(
                    "var rect = arguments[0].getBoundingClientRect();"
                    "return rect.top + window.pageYOffset;",
                    target_element,
                )
                current_position = self.driver.execute_script(
                    "return window.pageYOffset;")

                # Adjust scroll direction based on the target's position
                innerHeight = self.driver.execute_script(
                    "return window.innerHeight;")

                if target_position > current_position:
                    next_position = min(
                        target_position, current_position + innerHeight / 2)
                else:
                    next_position = max(
                        target_position, current_position - innerHeight / 2)

                self.driver.execute_script(
                    f"window.scrollTo(0, {next_position});")
                time.sleep(random.uniform(0.5, 1))  # Smooth scrolling delay

        except NoSuchElementException:
            print("Target element not found.")

    def random_scroll_for_duration(self, duration_range=(10, 40)):

        total_duration = random.randint(*duration_range)
        start_time = time.time()
        print(f"Random scrolling for {total_duration} seconds...")

        # Get the initial scroll position
        current_position = self.driver.execute_script(
            "return window.pageYOffset;")
        total_scroll_height = self.driver.execute_script(
            "return document.body.scrollHeight")

        while time.time() - start_time < total_duration:
            # Randomly choose whether to scroll up or down
            scroll_direction = random.choice(
                [True, False])  # True for up, False for down

            # Generate a random scroll distance within bounds
            scroll_amount = random.randint(
                50, 300) * (-1 if scroll_direction else 1)
            target_position = max(
                0, min(total_scroll_height, current_position + scroll_amount))

            # Perform the scrolling
            self._smooth_scroll(
                current_position, target_position, scroll_step=12)
            current_position = target_position

            # Introduce random pauses
            if random.random() < 0.2:  # 20% chance for a longer hold
                hold_duration = random.uniform(2, 4)
                print(f"Holding for {hold_duration:.2f} seconds...")
                time.sleep(hold_duration)
            else:
                # Short pause between scrolls
                time.sleep(random.uniform(0.3, 0.8))

            # Occasionally change the direction randomly
            if random.random() < 0.3:  # 30% chance to switch direction
                scroll_direction = not scroll_direction

            # Handle reaching the bounds (top or bottom)
            if current_position <= 0 or current_position >= total_scroll_height:
                scroll_direction = not scroll_direction

        print("Random scrolling completed.")
