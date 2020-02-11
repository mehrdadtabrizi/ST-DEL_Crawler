import  csv
import  requests
from    bs4         import BeautifulSoup
from    urllib      import request
from    collections import OrderedDict
from    selenium    import webdriver
import  städel_Parameters as Parameters
import  re

def browser_open():
    driver = webdriver.Firefox(executable_path=Parameters.Firefox_Driver_PATH)
    return driver

def browser_open_url(browser, url):
    browser.get(url)
    return browser

def get_soup_page(browser):
    res = browser.execute_script("return document.documentElement.outerHTML")
    soup = BeautifulSoup(res, 'lxml')
    return soup

def search_for_the_keyword(browser):
    print('Searching for the Keyword "' + Parameters.KEYWORD + '"...')
    browser_open_url(browser,Parameters.search_URL)
    return browser

def get_soup_from_url(url):
    r = requests.get(url)
    html = r.text
    soup = BeautifulSoup(html, 'html.parser')
    return soup

def extract_links_page(browser):
    links_in_page = []
    url = ' '
    soup = get_soup_page(browser)

    link_tags = soup.find_all('li', {'class': 'dsSearchResultItem'})
    for link in link_tags:
        if link.find('a') is not None:
            url = Parameters.base_url + link.find('a').get('href')
            links_in_page.append(url)

    return links_in_page

def refine_date(raw_date):
    earliest_date = ''
    latest_date = ''
    refined_date = []
    dates_array = re.findall(r"\d+", raw_date)
    try:
        earliest_date = dates_array[0]
    except:
        pass
    try:
        latest_date = dates_array[1]
    except:
        pass
    refined_date.append(earliest_date)
    refined_date.append(latest_date)
    return refined_date

def extract_page_metadata(browser):

    page_dic = []
    current_item = 1
    page_links = extract_links_page(browser)
    temp_browser = browser_open()

    for item_link in page_links:
        artist = ''
        date = ''
        earliest_date = ''
        latest_date = ''
        title = ''
        location = ''
        material = ''
        genre = ''
        temp_browser = browser_open_url(temp_browser,item_link)
        page_soup = get_soup_page(temp_browser)
        item_URL = item_link
        print('Item ' + str(current_item))
        info_box = page_soup.find('div' , {'class' : 'dsGroup__content'})
        try:
            date = temp_browser.find_element_by_xpath('//*/h1[@class="dsArtwork__titleHeadline"]/span[@class="dsArtwork__titleYear"]').text[2:]
        except:
            pass

        value_tags = info_box.find_all('dt',{'class' : 'dsProperty__caption'} )
        for tag in value_tags:
            if "Titel" in tag.text:
                title = re.sub(' +',' ' , tag.find_next_sibling('dd').text.replace('\n' , ' '))

            if "Material und Technik" in tag.text:
                material = re.sub(' +',' ' , tag.find_next_sibling('dd').text.replace('\n' , ' '))

            if "Maler" in tag.text or "Zeichner" in tag.text or "Künstler" in tag.text:
                artist = re.sub(' +',' ' , tag.find_next_sibling('dd').text.replace('\n' , ' '))

            if "Entstehungszeit" in tag.text and not date:
                date = re.sub(' +',' ' , tag.find_next_sibling('dd').text.replace('\n' , ' '))

            if "Objektart" in tag.text:
                genre = re.sub(' +',' ' , tag.find_next_sibling('dd').text.replace('\n' , ' '))
        file_name = str(current_item) + "_" + item_URL.split('/')[-1] + ".jpg"
        print(file_name)
        print(date)
        try:
            earliest_date = refine_date(date)[0]
            latest_date = refine_date(date)[-1]
        except:
            pass

        item_dic = {
            'Photo Archive'     : Parameters.base_url,
            'File Name'         : file_name,
            'Title'             : title,
            'Iconography'       : Parameters.Iconography,
            'Branch'            : 'ArtHist',
            'Artist'            : artist,
            'Current Location'  : 'Städel Museum',
            'Earliest Date'     : earliest_date,
            'Latest Date'       : latest_date,
            'Genre'             : genre,
            'Material'          : material,
            'Details URL'       : item_URL,
            'Image Credits'     : ''
        }
        keyorder = Parameters.Header
        item_dic = OrderedDict(sorted(item_dic.items(), key=lambda i: keyorder.index(i[0])))
        page_dic.append(item_dic)
        current_item += 1

    temp_browser.quit()
    return page_dic

def go_to_next_page(browser):
    try:
        buttons = browser.find_elements_by_xpath("//*/td[@width='80']/a")
        for button in buttons:
            if "next" in button.text:
                button.click()
                browser.implicitly_wait(30)
                return True
    except:
        pass
    return  False


def download_image(url,file_name):
    path = Parameters.Images_PATH + file_name
    request.urlretrieve(url, path)

def create_csv_file(file_path):
    keyorder = Parameters.Header
    with open(file_path, "w", newline='') as f:
        wr = csv.DictWriter(f, dialect="excel", fieldnames=keyorder)
        wr.writeheader()

def append_metadata_to_CSV(page_dic):
    keyorder = Parameters.Header
    with open(Parameters.CSV_File_PATH, "a", newline='') as fp:
        wr = csv.DictWriter(fp,dialect="excel",fieldnames=keyorder)
        for row in page_dic:
            wr.writerow(row)

def browser_quit(browser):
    browser.quit()