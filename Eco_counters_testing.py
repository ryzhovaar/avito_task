import os
import sys
import pytest
from playwright.sync_api import sync_playwright
import time

all_counters_selector = [
    "#app > div > div:nth-child(3) > div > div > div > div > div:nth-child(3) > div > div.desktop-impact-items-F7T6E > div:nth-child(2)",
    "#app > div > div:nth-child(3) > div > div > div > div > div:nth-child(3) > div > div.desktop-impact-items-F7T6E > div:nth-child(4)",
    "#app > div > div:nth-child(3) > div > div > div > div > div:nth-child(3) > div > div.desktop-impact-items-F7T6E > div:nth-child(6)"
]

@pytest.fixture(scope="module")
def take_screenshot(element, output_path):
    element.screenshot(path=output_path)

@pytest.mark.parametrize("resolution, window_size, browser_name, selectors", [
    ("1024x768", "800x600", "Chrome", all_counters_selector),
    ("1024x768", "1024x768", "Chrome", all_counters_selector),
    ("1920x1080", "800x600", "Chrome", all_counters_selector),
    ("1920x1080", "1024x768", "Chrome", all_counters_selector),
    ("1024x768", "800x600", "Firefox", all_counters_selector),
    ("1024x768", "1024x768", "Firefox", all_counters_selector),
    ("1920x1080", "800x600", "Firefox", all_counters_selector),
    ("1920x1080", "1024x768", "Firefox", all_counters_selector),
])

def testcase_2to9_counters_display(resolution, window_size, browser_name, selectors):
    with sync_playwright() as p:
        if browser_name == "Chrome":
            browser = p.chromium.launch()
        elif browser_name == "Firefox":
            browser = p.firefox.launch()
        context = browser.new_context(viewport={"width": int(resolution.split("x")[0]), "height": int(resolution.split("x")[1])})
        page = context.new_page()
        page.set_viewport_size({"width": int(window_size.split("x")[0]), "height": int(window_size.split("x")[1])})
        page.goto("https://www.avito.ru/avito-care/eco-impact")

        for i in range(2, 10):
            for j, single_selector in enumerate(selectors):
                path_to_save = os.path.join(os.path.dirname(__file__), 'output', f'testcase_№{i}_counter_{j + 1}.png')
                element_to_screenshot = page.wait_for_selector(single_selector, timeout=10000)
                element_to_screenshot.screenshot(path=path_to_save)
                time.sleep(10)

        browser.close()

def testcase_10_reopen_page():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        
        page.goto("https://www.avito.ru/avito-care/eco-impact")

        for i in range(1,4):

            path_to_save = os.path.join(os.path.dirname(__file__), 'output', f'testcase_№10_selector_{i}.png')
           
            element_to_screenshot = page.wait_for_selector(all_counters_selector[i], timeout=10000)
            
            element_to_screenshot.screenshot(path=path_to_save)

        page.reload()
        
        for i in range(1,4):

            path_to_save = os.path.join(os.path.dirname(__file__), 'output', f'testcase_№10_selector_reloaded_{i}.png')
       
            element_to_screenshot = page.wait_for_selector(all_counters_selector[i], timeout=10000)
        
            element_to_screenshot.screenshot(path=path_to_save)
        
        browser.close()

def testcase_1_display_counters():
    with sync_playwright() as p:
        
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto('https://www.avito.ru/avito-care/eco-impact')

        for i in range(1,4):
            path_to_save = os.path.join(os.path.dirname(__file__), 'output', f'testcase_№1_counter_{i}.png')
            element_to_screenshot = page.wait_for_selector(all_counters_selector[i], timeout=10000)
            element_to_screenshot.screenshot(path=path_to_save)
        browser.close()


sys.stderr = open("pytest_errors.txt", "w")
pytest.main(["-v"])

