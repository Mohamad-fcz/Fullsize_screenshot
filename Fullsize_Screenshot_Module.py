import os
import time
from datetime import datetime
import schedule
import ipywidgets as widgets
from IPython.display import IFrame
from IPython.display import display
from IPython.display import Image
from IPython.display import HTML
from tqdm.notebook import tqdm
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException


def full_page_screenshot(url2, duration2, interval2, output_directory2, size_screenshot2):
    while True:
        try:
            uploaded_file = uploader.value[0]
            name = uploaded_file["name"]
            with open(name, "wb") as fp:
                fp.write(uploaded_file.content)
            url2 = os.path.join(os.getcwd(), name)
            break
        except NameError:
            break

    # To tell apart the HTML document from the web address
    if os.path.isfile(url2):
        # screenshots are taken in sequence a number of times (counter)
        counter = 0
        # sleep time steps between screenshots
        interval2 = 0
    else:
        counter = (duration2 * 60) / interval2

    pbar = tqdm(range(int(counter) + 1))
    for i in pbar:
        pbar.set_description(f"screen shot number {i} of {int(counter)} has been stored")
        # options = Options()
        options = Options()
        if size_screenshot2 == "Full Page Screenshot":
            options.add_argument("--headless=new")
        elif size_screenshot2 == "Area Screenshot":
            options.add_argument("--start-maximized")
            options.add_argument("--window-size=1920,1080")
            options.add_experimental_option("detach", False)
        # the driver is defined for Google Chrome
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.implicitly_wait(10)
        # pass the URL of desired website
        driver.get(url2)
        # wait until the page has fully loaded and the screenshot is of the entire page
        driver.implicitly_wait(10)
        # naming the final output based on the input file
        if url2.endswith(".html"):
            name = os.path.basename(url2)[:-5]
        
        """" Full-Page OR Area Screenshot """
        driver.get_window_size()
        # obtain browser height and width
        w = driver.execute_script('return document.body.parentNode.scrollWidth')
        h = driver.execute_script('return document.body.parentNode.scrollHeight')
        # setting window size to take a full size page screenshot
        driver.set_window_size(w, h)
        # obtain screenshot of page within body tag
        time.sleep(2)
        driver.save_screenshot(
            os.path.join(os.path.abspath(output_directory2), f"{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}.png"))
        
        #######################################################################################################################
        
        # get window size
        s = driver.get_window_size()
        driver.set_window_size(s['width'], s['height'])
        # Alternatively using body in the page
        # websites use a body name for header and this line implements that to take the screenshot
        driver.find_element(by=By.TAG_NAME, value='body').screenshot(os.path.join(os.path.abspath(output_directory2), f"{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}_Body.png"))
        # closing the window after each screenshot
        driver.quit()
        # sleep steps between screenshots
        time.sleep(interval2 * 60)
        if os.path.isfile(url2):
            uploader.close()
            os.remove(url2)
    return



def fields():
    # HTML and java friendly interface
    output = widgets.Output()
    size_screenshot = widgets.RadioButtons(
        options=['Full Page Screenshot', 'Area Screenshot'],
        value='Full Page Screenshot',  # Defaults to 'pineapple'
        # layout=widgets.Layout(flex='3 1 auto', width='auto'),  # If the items' names are long
        description='Size:',
        disabled=False
    )
    # Ipywidgets GUI text box for user-entered url input
    url = widgets.Textarea(
        value=r'https://www.cnn.com/',
        placeholder='Type your URL',
        description='URL:',
        layout=widgets.Layout(height="auto", width="auto"),
        disabled=False
    )
    # Ipywidgets GUI dropdown for taking user desired duration for taking the screenshots
    duration = widgets.Dropdown(
        options=[('1 minute', 0.017), ('30 minutes', 0.5), ('1 Hour', 1), ('1.5 Hour', 1.5),
                 ('2 Hour', 2), ('4 Hour', 4), ('5 Hour', 5), ('6 Hour', 6), ('7 Hour', 7),
                 ('8 Hour', 8), ('9 Hour', 9), ('10 Hour', 10), ('11 Hour', 11), ('12 Hour', 12),
                 ('13 Hour', 13), ('14 Hour', 14), ('15 Hour', 15), ('16 Hour', 16), ('17 Hour', 17),
                 ('18 Hour', 18), ('19 Hour', 19), ('20 Hour', 20), ('21 Hour', 21), ('22 Hour', 22),
                 ('23 Hour', 23), ('24 Hour', 24), ('48 Hour', 48)],
        value=1,
        description='Duration:'
    )
    # Ipywidgets GUI slider for taking the desired user duration
    interval = widgets.FloatSlider(
        value=15,
        min=0,
        max=60.0,
        step=0.5,
        description='Interval (Minutes)',
        disabled=False,
        continuous_update=False,
        orientation='horizontal',
        readout=True,
        readout_format='.1f',
        style={'description_width': 'initial'},
        layout=widgets.Layout(flex='3 1 00%', width='auto')
    )
    # Ipywidgets GUI text box for user-entered output directory
    output_directory = widgets.Textarea(
        value=f"{os.getcwd()}",
        placeholder='Type folder path',
        layout=widgets.Layout(height="auto", width="auto"),
        description='Out folder:',
        disabled=False
    )
    # Ipywidgets GUI button
    executer = widgets.Button(
        description='Capture Screenshot',
        layout=widgets.Layout(flex='3 1 00%', height='auto', width='auto'),
        disabled=False,
        button_style='success',
        tooltip='Click me',
        icon='check'
    )
    uploader = widgets.FileUpload(
        accept='.html',
        multiple=False
    )
    loading = Image(url="https://github.com/conda/conda/assets/99288525/81dcbb68-219b-498b-aaea-c583b512a352",
                    width=200, height=100, alt=" Your screenshots are being captured")
    loading_text = HTML(data="<b style='color:#FF5050;''font-size: 40'>Your screenshots are being captured</b>")
    # function for saving the
    def on_button_clicked(b):
        with output:
            display(loading_text)
            display(loading)
            full_page_screenshot(url.value, duration.value, interval.value, output_directory.value, size_screenshot.value)

    executer.on_click(on_button_clicked)
    items = [url, duration, output_directory, interval, size_screenshot, executer]
    left_box = widgets.VBox([items[4], items[0], items[2]],
                            display='flex',
                            flex_flow='column',
                            align_items='stretch',
                            border='solid',
                            width='50%')
    right_box = widgets.VBox([items[1], items[3], items[5]],
                             display='flex',
                             flex_flow='column',
                             align_items='stretch',
                             border='solid',
                             width='50%')

    tab_nest = widgets.Tab()
    # tab_nest.children = [widgets.HBox([left_box, right_box]), widgets.VBox([items[5], uploader])]
    tab_nest.children = [widgets.GridBox([left_box, right_box], layout=widgets.Layout(grid_template_columns="repeat(2, 540px)")), widgets.VBox([uploader, items[5]])]
    tab_nest.titles = ('Web Page URL', 'HTML File')

    display(tab_nest, output)
