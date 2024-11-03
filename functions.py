from read_data import *
from datetime import datetime
from dateutil.relativedelta import relativedelta
from datetime import datetime
import numpy as np

def get_date_input(prompt):
    while True:
        date_str = input(prompt)
        try:
            # Kiểm tra và phân tích chuỗi đầu vào theo định dạng yyyy/mm/dd
            date_obj = datetime.strptime(date_str, '%Y/%m/%d')
            return date_obj
        except ValueError:
            print("Định dạng không hợp lệ. Vui lòng nhập theo định dạng yyyy/mm/dd.")

def check_cs_status(row):
    if row['loan_status'] == 'Đã hoàn thành':
        return 'cs_done'
    elif row['loan_status'] == 'Đang xử lý':
        return 'cs_processing'
    elif row['loan_status'] == 'Ngừng xử lý':
        return 'cs_write_off'
    else:
        return np.nan

def check_system_status(row):
    if row['created_date_y'] > row['payable_date']:
        return 'system_late'
    elif row['created_date_y'] <= row['payable_date']:
        return 'system_done'
    else:
        return np.nan

def check_daily_writeoff_status(row):
    if row['loan_status'] == 'Đã hoàn thành':
        return 'note'
    elif row['loan_status'] == 'Đang xử lý':
        return 'daily_interest'
    elif row['loan_status'] == 'Ngừng xử lý':
        return 'cs_write_off'
    else:
        return np.nan
    
def export_to_excel(df):
    # Đường dẫn thư mục lưu trữ tệp Excel
    folder_path = "E:\\Documents\\NANO\\Revenue Automation\\export_file"

    # Tên của tệp Excel
    excel_file_name = 'output_data.xlsx'

    # Kết hợp đường dẫn và tên tệp
    full_path = folder_path + excel_file_name

    # Lưu DataFrame vào tệp Excel
    df.to_excel(full_path, index=False)

    print(f'Tệp Excel đã được lưu tại: {full_path}')

def export_system_exclude_to_excel(system_exclude):
    # Đường dẫn thư mục lưu trữ tệp Excel
    folder_path = "E:\\Documents\\NANO\\Revenue Automation\\export_file"

    # Tên của tệp Excel
    excel_file_name = 'system_exclude.xlsx'

    # Kết hợp đường dẫn và tên tệp
    full_path = folder_path + excel_file_name

    # Lưu DataFrame vào tệp Excel
    system_exclude.to_excel(full_path, index=False)

    print(f'Tệp Excel đã được lưu tại: {full_path}')

def export_amount_checking_to_excel(amount_checking):
    # Đường dẫn thư mục lưu trữ tệp Excel
    folder_path = "E:\\Documents\\NANO\\Revenue Automation\\export_file"

    # Tên của tệp Excel
    excel_file_name = 'amount_checking.xlsx'

    # Kết hợp đường dẫn và tên tệp
    full_path = folder_path + excel_file_name

    # Lưu DataFrame vào tệp Excel
    amount_checking.to_excel(full_path, index=False)

    print(f'Tệp Excel đã được lưu tại: {full_path}')
