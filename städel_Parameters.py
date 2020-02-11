Firefox_Driver_PATH = "C:\geckodriver.exe"
KEYWORD = "Anbetung"
Iconography = "Adoration"

Header = [  'Branch',
            'File Name',
            'Image ID',
            'Artist',
            'Title',
            'Iconography',
            'Part',
            'Earliest Date',
            'Latest Date',
            'Margin Years',
            'Genre',
            'Material',
            'Medium',
            'Height of Image Field',
            'Width of Image Field',
            'Type of Object',
            'Height of Object',
            'Width of Object',
            'Diameter of Object',
            'Position of Depiction on Object',
            'Current Location',
            'Repository Number',
            'Original Location',
            'Original Place',
            'Original Position',
            'Context',
            'Place of Discovery',
            'Place of Manufacture',
            'Associated Scenes',
            'Related Works of Art',
            'Type of Similarity',
            'Inscription',
            'Text Source',
            'Bibliography',
            'Photo Archive',
            'Image Credits',
            'Details URL',
            'Additional Information']

CSV_File_PATH = 'STÄDEL_Metadaten_' + KEYWORD + '.csv'
Images_PATH   = 'D:\_DATA\HiWiDateien\Crawler\Downloaded Images\_Anbetung, Adoration\Städel\ '

base_url      = 'https://sammlung.staedelmuseum.de'
search_URL    = 'https://sammlung.staedelmuseum.de/de/suche?q=' + KEYWORD + "&scope=all"

Images_are_already_downloaded = False