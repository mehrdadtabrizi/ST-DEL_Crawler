import städel as st
import städel_Parameters as Parameters

def main():
    browser = st.browser_open()
    browser = st.browser_open_url(browser,Parameters.search_URL)
    browser = st.search_for_the_keyword(browser)
    current_page = 1
    PAGE_EXISTS = True
    st.create_csv_file(Parameters.CSV_File_PATH)
    item_dic = {

    }
    #while(PAGE_EXISTS):
    print('Working on page ' + str(current_page) )
    page_dic = st.extract_page_metadata(browser)
    st.append_metadata_to_CSV(page_dic)
        #PAGE_EXISTS = st.go_to_next_page(browser)

    st.browser_quit(browser)

main()