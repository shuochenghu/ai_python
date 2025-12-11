from google import genai
from google.colab import userdata
from IPython.display import HTML, display
from google.colab import files
from dotenv import load_dotenv
import ipywidgets as widgets
import os
import csv
import base64


# Get API key from Colab secrets
GOOGLE_API_KEY = userdata.get('GOOGLE_API_KEY')
client = genai.Client(api_key=GOOGLE_API_KEY)

def print_llm_response(prompt, model="gemini-2.5-flash"):
    # Prepend the system instruction to ensure Traditional Chinese responses
    full_prompt = f"一律以繁體中文回覆。{prompt}"
    response = client.models.generate_content(
        model=model,
        contents=full_prompt
    )
    print(response.text)

def get_llm_response(prompt, model="gemini-2.5-flash"):
    # Prepend the system instruction to ensure Traditional Chinese responses
    full_prompt = f"一律以繁體中文回覆。{prompt}"
    response = client.models.generate_content(
        model=model,
        contents=full_prompt
    )
    return response.text

# 測試
#print_llm_response("請用繁體中文撰寫一篇關於人工智慧倫理的小短文，字數約150字。")

def read_journal(filename):
    """
    讀取 Google Drive 中指定檔案的內容。

    Args:
        filename (str): 要讀取的檔案名稱。

    Returns:
        str: 檔案的內容，如果檔案不存在則返回錯誤訊息。
    """
    #drive_path = '/content/drive/MyDrive/'
    drive_path = '/content/'
    full_path = os.path.join(drive_path, filename)

    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except FileNotFoundError:
        return f"錯誤：檔案 '{filename}' 不存在於 Google Drive 中。"
    except Exception as e:
        return f"讀取檔案 '{filename}' 時發生錯誤：{e}"


def display_html(html_response):
    """
    將 HTML 字串作為輸出顯示在 Colab 筆記本中。

    Args:
        html_response (str): 包含 HTML 內容的字串。
    """
    display(HTML(html_response))

def upload_txt_file():
    uploaded = files.upload()
    for fn in uploaded.keys():
        print(f'使用者上傳了檔案 "{fn}" (大小: {uploaded[fn]} bytes)')

def list_files_in_directory(directory='.'):
    """
    Lists all non-hidden files in the specified directory.
    
    Args:
        directory (str): The directory to list files from. Defaults to the current working directory.
    """
    try:
        files = [f for f in os.listdir(directory) if (not f.startswith('.') and not f.startswith('_'))]
        for file in files:
            print(file)
    except Exception as e:
        print(f"An error occurred: {e}")

def read_csv_dict(csv_file_path):
    """This function takes a csv file and loads it as a dict."""

    # Initialize an empty list to store the data
    data_list = []

    # Open the CSV file
    with open(csv_file_path, mode='r') as file:
        # Create a CSV reader object
        csv_reader = csv.DictReader(file)
    
        # Iterate over each row in the CSV file
        for row in csv_reader:
            # Append the row to the data list
            data_list.append(row)

    # Convert the list to a dictionary
    data_dict = {i: data_list[i] for i in range(len(data_list))}
    return data_dict

def download_file():
    """
    Creates a widget to download a file from the working directory.
    """
    # Text input to specify the file name
    file_name_input = widgets.Text(
        value='',
        placeholder='Enter file name',
        description='File:',
        disabled=False
    )
    
    # Button to initiate the download
    download_button = widgets.Button(
        description='Download',
        disabled=False,
        button_style='', # 'success', 'info', 'warning', 'danger' or ''
        tooltip='Download the specified file',
        icon='download' # (FontAwesome names without the `fa-` prefix)
    )
    
    # Output widget to display the download link
    output = widgets.Output()

    def on_button_click(b):
        with output:
            output.clear_output()
            file_name = file_name_input.value
            if (not file_name.startswith('.') and not file_name.startswith('_')):
                try:
                    download_link = create_download_link(file_name, 'Click here to download your file')
                    display(download_link)
                except Exception as e:
                    print(f"Error: {e}")
            else:
                print("Please enter a valid file name.")
    
    # Attach the button click event to the handler
    download_button.on_click(on_button_click)
    
    # Display the widgets
    display(widgets.HBox([file_name_input, download_button]), output)

def create_download_link(file_path, description):
    with open(file_path, 'rb') as file:
        file_data = file.read()
        encoded_data = base64.b64encode(file_data).decode()
        href = f'<a href="data:text/html;base64,{encoded_data}" download="{file_path}">{description}</a>'
        return HTML(href)