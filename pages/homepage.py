import json
import random
import time
from setup.smooth_scroll import SmoothScroll


class HomePage:
    def __init__(self, driver):
        self.driver = driver

        with open('data/page_locators.json', 'r') as f:
            self.locators = json.load(f)

    def run_main_page(self):
        scroller = SmoothScroll(self.driver)

        # Locate buttons and games
        button_locator = self.locators["mainButtons"]
        game_locator = self.locators["games"]

        select_game_type = random.choice(list(button_locator.values()))
        select_game = random.choice(list(game_locator.values()))

        # Helper methods
        def hold_and_click_back(self):
            hold_time = random.randint(10, 40)
            print(f"Holding for {hold_time} seconds...")
            time.sleep(hold_time)
            self.driver.back()
            print("Navigating back...")

        # Scenarios
        def scenario_scroll_down_then_up_click_main():
            scroller.scroll_down_then_up_and_click(select_game_type)

            # Second-level logic after navigating to a new page
            if random.random() <= 0.7:
                scroller.random_scroll_for_duration()
            else:
                scroller.scroll_down_then_up_and_click(select_game)
                hold_and_click_back(self)

        def scenario_select_game_directly():
            scroller.scroll_down_then_up_and_click(select_game)
            hold_and_click_back(self)

        def scenario_random_scrolling():
            scroller.random_scroll_for_duration()

        # Main distribution logic
        scenarios = []
        probabilities = []

        # 60% scene 1
        scenarios.append(scenario_scroll_down_then_up_click_main)
        probabilities.append(0.6)

        # 30% scene 2
        scenarios.append(scenario_select_game_directly)
        probabilities.append(0.3)

        # 10% scene 3
        scenarios.append(scenario_random_scrolling)
        probabilities.append(0.1)

        # Execute based on probabilities
        selected_scenario = random.choices(scenarios, probabilities)[0]
        print(f"Selected scenario: {selected_scenario.__name__}")
        selected_scenario()

        # Optionally incorporate additional scenarios like scroll to end
        if random.random() < 0.15:  # 15% chance to add extra random behavior
            scroller.scroll_to_end_and_close()
