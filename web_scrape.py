from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
import datetime

def songList():
    options = Options()
    options.headless = True
    options.add_argument = ('--window-size=1920,1080')

    DRIVER_PATH = 'chromedriver.exe'

    driver = webdriver.Chrome(options = options, executable_path=DRIVER_PATH)
    driver.get('https://radiokampus.fm/playlista/')

    cookies_button = driver.find_elements_by_css_selector('.cookieConsent button')
    cookies_button[0].click()

    # Find calendar button
    change_date = driver.find_elements_by_class_name('react-datepicker__input-container')

    # Get current date for playlist name
    current_date = change_date[0].find_elements_by_tag_name('input[value]')

    # Save current date
    playlist_date = current_date[0].get_attribute('value')

    if playlist_date[-2:] == '01':
            
        # Check which day is last 30 or 31
        last_month_date = datetime.datetime.today() - datetime.timedelta(days=1)
        last_month_date = str(last_month_date)
        
        # Change playlist_date var for Spotify Playlist name reference
        playlist_date = last_month_date[:10]

        # Create last day var for web calendar
        last_month_day = last_month_date[-2:]

        # Show calendar window
        current_date[0].click()

        # Change month
        previous_month = driver.find_elements_by_class_name('react-datepicker__navigation--previous')
        previous_month[0].click()    

        # Click last day of the month
        calendar = driver.find_elements_by_class_name('react-datepicker__month')
        previous_day = calendar[0].find_elements_by_css_selector('div[aria-label=day-' + last_month_day + ']:not(.react-datepicker__day--outside-month)')
        previous_day[0].click()

    else:            
        # Calculate date of the previous day
        change_date = str(int(playlist_date[-2:]) - 1)

        # Change date var to a previous day
        playlist_date = playlist_date[:-2] + change_date

        # Show calendar window
        current_date[0].click()

        # Find the previous day and click it
        calendar = driver.find_elements_by_class_name('react-datepicker__month')
        previous_day = calendar[0].find_elements_by_tag_name('div[aria-label=day-' + change_date + ']')

        previous_day[0].click()

    print('Sleeping start')
    sleep(3)
    print('Sleeping end')

    song_container = driver.find_elements_by_class_name('song_container')
    song_list = []

    for song in song_container:
        song = song.find_elements_by_tag_name('span')
        song_list.append((song[0].text + ' ' + song[1].text).replace('(', '').replace(')', '').replace('feat. ', ''))

    driver.quit()

    return [song_list, playlist_date]
