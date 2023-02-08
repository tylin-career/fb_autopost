import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from logger import Logger
import os
import json
import random
import line_notify


logger = Logger(__name__).get_logger()
GROUP_LISTS = "data/groups/group_list_DEV.txt"
ARTICLE_PATH = "data/resource/article.txt"
PHOTO_PATH = "data/resource/pic_folder/pic.png"


def load_passage_txt(ARTICLE_PATH) -> str:
    with open(ARTICLE_PATH, 'r', encoding='utf-8') as file:
        content = file.readlines()
    return content


def get_photo_path():
    abs_path = os.path.dirname(os.path.abspath("__file__"))
    photo_path = os.path.join(abs_path, PHOTO_PATH)
    return photo_path


def write_passage(browser, content):
    logger.info("Start writing articles")
    # Leave a message
    msg_box_xpath = "//div[@class = 'x1i10hfl x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x16tdsg8 x1hl2dhg xggy1nq x87ps6o x1lku1pv x1a2a7pz x6s0dn4 xmjcpbm x107yiy2 xv8uw2v x1tfwpuw x2g32xy x78zum5 x1q0g3np x1iyjqo2 x1nhvcw1 x1n2onr6 xt7dq6l x1ba4aug x1y1aw1k xn6708d xwib8y2 x1ye3gou']"
    # msg_box_xpath = "//div[@role = 'button']"
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH, msg_box_xpath))
    ).click()
    # browser.find_element(By.XPATH, msg_box_xpath).click()

    photo_video_path = "//div[@aria-label = '相片／影片']"
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH, photo_video_path))
    ).click()
    logger.info("Posting box opened successfully")

    # # Post
    text_box = "/html/body/div[1]/div/div[1]/div/div[6]/div/div/div[1]/div/div[2]/div/div/div/div/div[1]/form/div/div[1]/div/div/div[1]/div/div[2]/div[1]/div[1]/div[1]/div[1]/div/div/div/div/div[2]/div"
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH, text_box))
    ).send_keys(content)
    time.sleep(1)

    # Attach picture
    pic_path = "/html/body/div[1]/div/div[1]/div/div[6]/div/div/div[1]/div/div[2]/div/div/div/div/div[1]/form/div/div[1]/div/div/div[1]/div/div[2]/div[1]/div[1]/div[2]/div/div[1]/div/div[1]/input"
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH, pic_path))
    ).send_keys(get_photo_path())
    time.sleep(2)

    # Submit the post
    path2 = "/html/body/div[1]/div/div[1]/div/div[6]/div/div/div[1]/div/div[2]/div/div/div/div/div[1]/form/div/div[1]/div/div/div[1]/div/div[3]/div[2]/div[1]/div"
    browser.find_element(By.XPATH, path2).click()

    logger.info(
        'Article has been posted. Please verify your post in the group page later.'
    )
    rand_time = random.randint(30, 120)

    
    logger.info(f'Directing to next group in {rand_time} seconds.')
    time.sleep(rand_time)


def browse_webpage(browser, group):
    logger.info(f"Loading group page: {group}...")
    browser.get(group)

    time.sleep(random.randint(2, 7))
    ActionChains(browser).send_keys(Keys.ESCAPE).perform()
    logger.info("Group page is loaded successfully")


def credential_loads_using_json():
    try:
        with open("data/credentials/credentials_load.json") as filePointer:
            contents = filePointer.read()
        contents = json.loads(contents)
        logger.info(f"Credentials loaded.")
        return contents
    except:
        logger.info(
            "Failed to retrieve your credentials. Please prepare your credential file."
        )
        input("Press ENTER to exit...")


def login_facebook(options):
    logger.info('Login automation started...')
    try:
        browser = webdriver.Chrome('chromedrivier/chromedriver', options=options)
    except:
        browser = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    browser.get('https://www.facebook.com/')
    assert 'Facebook' in browser.title
    time.sleep(1)

    # Find elements
    usr_box = browser.find_element('id', 'email')
    pwd_box = browser.find_element('id', 'pass')

    # Operate
    contents = credential_loads_using_json()
    usr_box.send_keys(contents["user_email"])
    pwd_box.send_keys(contents["password"])
    browser.find_element(
        By.XPATH, "//button[@class = '_42ft _4jy0 _6lth _4jy6 _4jy1 selected _51sy']"
    ).click()

    logger.info('Credentials entered. Facebook logging in progress')
    time.sleep(5)
    return browser


def get_group_list(file_name: str):
    with open(file_name, "r", encoding="utf-8") as f:
        urls = f.readlines()
        groups = [url.rstrip() for url in urls]
    return groups


def setup():
    options = Options()
    prefs = {'profile.default_content_setting_values': {'notifications': 2}}
    options.add_experimental_option('prefs', prefs)  # Prevent pop-up (notification)
    options.add_experimental_option(
        'excludeSwitches', ['enable-logging']
    )  # remove devtool message log
    options.add_argument(
        '--disable-gpu'
    )  # Google document says to add this to avoid bug
    options.add_argument(
        'user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"'
    )  # add user-agent
    # options.add_argument('--headless')  # 背景執行
    options.add_argument("window-size=1920,1080")  # to support background process
    return options


def main():
    options = setup()
    logger.info("Timer started")
    start_time = time.time()

    browser = login_facebook(options)
    groups = get_group_list(GROUP_LISTS)
    content = load_passage_txt(ARTICLE_PATH)
    token = "gz9wkJZEn5PzCpVrBunGDVp5WvrGhGtRwdbibB1gnKl"
    fail_url = list()
    for group in groups:
        try:
            browse_webpage(browser, group)
            write_passage(browser, content)
        except Exception as e:
            logger.info(
                f'''
                ********** Group <{group}> has been skipped due to 
                {e}
                **********
                '''
            )
            fail_url.append(group)
            continue
        finally:
            print("-----------------------------------------------------------")
    end_time = time.time()
    line_notify.lineNotify(
        token,
        f'''
        Failed urls are: {fail_url}.
        '''
    )
    logger.info(
        "Timer stopped. Total execution time is: {:.2f} minute(s)".format(
            ((end_time - start_time) / 60)
        )
    )
    logger.info('Posting automation finished.')
    browser.quit()
    input("Press ENTER to shut down...")

