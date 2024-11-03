from read_data import *
from datetime import datetime
from dateutil.relativedelta import relativedelta
from datetime import datetime
import numpy as np
import pandas as pd
from functions import *

def main_task():
  user_profiles_view = read_data_user_profiles_view()
  user_payable = read_data_user_payale()
  user_pay_report = read_data_user_pay_report()
  user_pay_history = read_data_user_pay_history()
  installment_loan = read_data_installment_loan()
  accountant_spending_transactions = read_data_accountant_spending_transactions() 
  ar_tracking = read_data_ar_tracking()
  ar_tracking1 = read_data_ar_tracking()
  ac = read_data_ac()

  accountant_spending_transactions = accountant_spending_transactions.groupby('employee_id').agg({'net_revenue':'sum','employment_id':'first','company':'first','date':'first'}).reset_index()
  ac = ac.groupby('ac_employee_id').agg({'ac_company':'first','ac_amount':'sum'}).reset_index()
  # accountant_spending_transactions['employee_id'] = accountant_spending_transactions['employee_id'].astype(str)
  # ac['ac_employee_id'] = ac['ac_employee_id'].astype(str)

  amount_checking = ac.merge(accountant_spending_transactions, left_on='ac_employee_id',right_on='employee_id',how='inner')
  amount_checking = amount_checking[['company','employee_id','net_revenue','ac_amount']]
  amount_checking['ac_amount'] = amount_checking['ac_amount'].replace('-', '0')
  amount_checking['net_revenue'] = amount_checking['net_revenue'].astype('int64')
  # amount_checking['ac_amount'] = amount_checking['ac_amount'].astype(float)

  amount_checking['diff'] = amount_checking['net_revenue'] - amount_checking['ac_amount']
  export_amount_checking_to_excel(amount_checking)

  employee_checking = ac.merge(accountant_spending_transactions, left_on='ac_employee_id',right_on='employee_id',how='outer')

  system_exclude = employee_checking[employee_checking['employee_id'].isnull()]['ac_employee_id']
  export_system_exclude_to_excel(system_exclude)

  employee_checking = ac.merge(accountant_spending_transactions, left_on='ac_employee_id',right_on='employee_id',how='right')
  ## filter not in system
  system_exclude = employee_checking[employee_checking['employee_id'].isnull()]['ac_employee_id']
  export_system_exclude_to_excel(system_exclude)

  employee_checking = employee_checking[employee_checking['employee_id'].notnull()]

  employee_checking = employee_checking[employee_checking['ac_employee_id'].isnull()]
  employee_checking= employee_checking[['employee_id', 'employment_id', 'company', 'date', 'net_revenue']]
  employee_checking= employee_checking.groupby(['company', 'employee_id','employment_id', 'date']).sum('net_revenue').reset_index()

  ar_tracking['late_payment_penalty_date'] = pd.to_datetime(ar_tracking['late_payment_penalty_date'], format='%d/%m/%Y')
  ar_tracking['late_payment_penalty_date'] = ar_tracking['late_payment_penalty_date'].apply(lambda x: x.replace(day=1))

  date = get_date_input('Enter date (yyyy/mm/dd): ')
  print("Ngày bạn đã nhập:", date)
  revenue_date = date + relativedelta(months=1)

  ar_tracking = ar_tracking[ar_tracking['late_payment_penalty_date'] == revenue_date]
  ar_tracking = ar_tracking.drop_duplicates(subset=['employee_id'], keep='first')
  employee_checking = employee_checking.merge(ar_tracking, on='employee_id', how='left')

  # apply_cs_check
  employee_checking['cs_status'] = employee_checking.apply(check_cs_status, axis=1)

  # status_cs_check
  employee_checking = employee_checking[['company','employee_id','employment_id','date','net_revenue','cs_status']]
  completed_merge =  user_payable.merge( user_pay_report, left_on='id', right_on='user_payable_id',how='inner')
  completed_merge = completed_merge.drop_duplicates()

  completed_merge = completed_merge[['installment_loan_id','status','amount_x','payable_date','type','created_date_y']]

  completed_merge = completed_merge.merge(installment_loan, left_on='installment_loan_id', right_on='id',how='inner')
  completed_merge = completed_merge[['employment_id','status_x','amount_x','payable_date','type','created_date_y']]
  completed_merge = completed_merge[completed_merge['type']=='Fee']
  completed_merge['created_date_y'] = completed_merge['created_date_y'].dt.date

  #apply_system_status
  completed_merge['system_status'] = completed_merge.apply(check_system_status, axis=1)

  completed_merge['start_month'] = completed_merge['payable_date'].apply(lambda x: x.replace(day=1))
  revenue_date_date = revenue_date.date()

  completed_merge = completed_merge[completed_merge['start_month']== revenue_date_date]
  completed_merge = completed_merge.drop_duplicates(subset=['employment_id'], keep='first')

  # status_system_check
  employee_checking = employee_checking.merge(completed_merge, left_on='employment_id', right_on='employment_id', how='left')
  employee_checking['date'] = employee_checking['date'].dt.date

  employee_checking = employee_checking[['company','employee_id','employment_id','date','net_revenue','cs_status','system_status']]
  ar_tracking1['late_payment_penalty_date'] = pd.to_datetime(ar_tracking1['late_payment_penalty_date'], format='%d/%m/%Y')
  ar_tracking1['late_payment_penalty_date'] = ar_tracking1['late_payment_penalty_date'].apply(lambda x: x.replace(day=1))

  ar_merge = ar_tracking1.groupby('employee_id').agg({'late_payment_penalty_date': 'max'})
  ar_tracking1 = ar_tracking1.merge(ar_merge, on=['employee_id', 'late_payment_penalty_date'], how='inner')

  # status_daily_writeoff_check
  ar_tracking1['daily_writeoff_status'] = ar_tracking1.apply(check_daily_writeoff_status, axis=1)

  ar_tracking1 = ar_tracking1[['employee_id', 'daily_writeoff_status']]
  ar_tracking1 = ar_tracking1.drop_duplicates(subset=['employee_id'], keep='first')
  employee_checking = employee_checking.merge(ar_tracking1, on='employee_id', how='left')
  employee_checking['result'] = employee_checking['cs_status'].fillna(employee_checking['system_status']).fillna(employee_checking['daily_writeoff_status'])
  final = employee_checking[['company','employee_id','employment_id','date','net_revenue','result']]
  export_to_excel(final)
  happy = 'Hoàn thành!!! Chúc bạn một ngày tốt lành 사랑해요!!!'
  return print(happy)

