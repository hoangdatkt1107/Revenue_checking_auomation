import pandas as pd
from database import connect_to_postgres
from company_rename import rename_company

def read_data_ac() -> pd.DataFrame:
    ac1 = pd.read_excel("E:\\Documents\\NANO\\Revenue Automation\\paylater_t6\\06.2024. Paylater Revenue.xlsx", sheet_name='User', header=0)
    ac2 = pd.read_excel("E:\\Documents\\NANO\\Revenue Automation\\paylater_t6\\06.2024. Paylater Revenue.xlsx", sheet_name='DN hoàn ứng', header=0)
    ac = pd.concat([ac1, ac2], ignore_index=True)
    # ac['ac_company'] = ac['ac_company'].apply(rename_company)
    return ac

def read_data_user_profiles_view() -> pd.DataFrame:
    connection = connect_to_postgres()
    if connection is None:
        return None

    query = "select * from l1_tables.user_profiles_view"
    user_profiles_view = pd.read_sql(query, connection)
    print('Got data from user_profiles_view')
    return user_profiles_view

def read_data_user_payale() -> pd.DataFrame:
    connection = connect_to_postgres()
    if connection is None:
        return None

    query = "select * from paylater.user_payable"
    user_payable = pd.read_sql(query, connection)
    print('Got data from user_payable')
    return user_payable

def read_data_user_pay_report() -> pd.DataFrame:
    connection = connect_to_postgres()
    if connection is None:
        return None

    query = "select * from paylater.user_pay_report"
    user_pay_report = pd.read_sql(query, connection)
    print('Got data from user_pay_report')
    return user_pay_report

def read_data_user_pay_history() -> pd.DataFrame:
    connection = connect_to_postgres()
    if connection is None:
        return None

    query = "select * from paylater.user_pay_history"
    user_pay_history = pd.read_sql(query, connection)
    print('Got data from user_pay_history')
    return user_pay_history

def read_data_installment_loan() -> pd.DataFrame:
    connection = connect_to_postgres()
    if connection is None:
        return None

    query = "select * from paylater.installment_loan"
    installment_loan = pd.read_sql(query, connection)
    print('Got data from installment_loan')
    return installment_loan

def read_data_accountant_spending_transactions() -> pd.DataFrame:
    connection = connect_to_postgres()
    if connection is None:
        return None

    query = "select * from vui_app_report.accountant_spending_transactions where date_trunc('month',date) = '2024-06-01' and type = 'Paylater'"
    accountant_spending_transactions = pd.read_sql(query, connection)
    print('Got data from accountant_spending_transactions')
    return accountant_spending_transactions

def read_data_ar_tracking() -> pd.DataFrame:
    connection = connect_to_postgres()
    if connection is None:
        return None

    query = "select * from other_raw_data.ar_tracking where type = 'Paylater'"
    ar_tracking = pd.read_sql(query, connection)
    print('Got data from ar_tracking')
    connection.close()
    print('connection_closed')
    return ar_tracking





