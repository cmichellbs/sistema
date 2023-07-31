import pandas as pd
from scipy.optimize import newton
import sgs
import json
from math import trunc
from datetime import datetime

def convert_date_format(input_date):
    # Parse the input date string to a datetime object
    date_object = datetime.strptime(input_date, '%Y-%m-%d')

    # Format the datetime object to the desired output format
    output_date = date_object.strftime('%d/%m/%Y')

    return output_date

def get_interest(P, C, n):
    # Define the function we're trying to solve
    func = lambda i: P - C * (((1 + i)**n)*i)/(((1 + i)**n)-1)

    # Initial guess
    i0 = 0.01  # Initial guess could be, say, 5% annual interest rate
    i = newton(func, i0)

    return i

def get_monthly_payment(C, n, i):
    func = lambda P: P - C * (((1 + i)**n)*i)/(((1 + i)**n)-1)
    P0 = 1
    P = newton(func, P0)
    return P

def get_loan_amount(P, n, i):
    func = lambda C: P - C * (((1 + i)**n)*i)/(((1 + i)**n)-1)
    C0 = 1
    C = newton(func, C0)

def get_number_of_months(P, C, i):
    func = lambda n: P - C * (((1 + i)**n)*i)/(((1 + i)**n)-1)
    n0 = 1
    n = newton(func, n0)

def bsb_sgs_interest( CODE,date):
        ts = sgs.time_serie(CODE,date,date)
        df = pd.DataFrame(ts)

        if df.empty:
            ts = sgs.time_serie(CODE,'01/01/1900','31/12/3000')
            df = pd.DataFrame(ts)
            average = df.tail(3)[CODE].sum()/3
            return average
        else:
            return df[CODE][0]

class ContractAlternatives(object):
    
    def __init__(self, months, interest_rate, loan_amount, monthly_payment, CODE, date):
        self.months = months
        self.interest_rate = interest_rate/100
        self.loan_amount = loan_amount
        self.monthly_payment = monthly_payment
        self.effective_interest_rate = get_interest(self.monthly_payment, self.loan_amount, self.months)
        self.effective_monthly_payment = get_monthly_payment(self.loan_amount, self.months, self.interest_rate)
        self.effective_loan_amount = get_loan_amount(self.monthly_payment, self.months, self.interest_rate)
        self.effective_number_of_months = get_number_of_months(self.monthly_payment, self.loan_amount, self.interest_rate)
        self.CODE = CODE
        self.bcb_interest = bsb_sgs_interest(self.CODE,convert_date_format(date))/100





    def price_table(self,variant=None):
        
        if variant == 'bcb':
            A = self.monthly_payment
            C = self.loan_amount
            i = self.bcb_interest
            n = self.months

            P = C * (((1 + i)**n)*i)/(((1 + i)**n)-1)
            
            df = pd.DataFrame(columns=['Parcela','Valor','Juros','Amortização','Saldo Devedor'])
            for  item in range(1,n+1):
                if item == 1:
                    saldo_devedor = C
                juros = saldo_devedor * i
                amortizacao = P - juros
                saldo_devedor = saldo_devedor - amortizacao
                df = pd.concat([df,pd.DataFrame([[item,P,juros,amortizacao,saldo_devedor]],columns=['Parcela','Valor','Juros','Amortização','Saldo Devedor'])],ignore_index=True)  
                df = df.round({'Valor': 2, 'Juros': 2, 'Amortização': 2, 'Saldo Devedor': 2})
            
            return df
        
        elif variant == 'effective':
            A = self.monthly_payment
            C = self.loan_amount
            i = self.effective_interest_rate
            n = self.months

            P = C * (((1 + i)**n)*i)/(((1 + i)**n)-1)
            
            df = pd.DataFrame(columns=['Parcela','Valor','Juros','Amortização','Saldo Devedor'])
            for  item in range(1,n+1):
                if item == 1:
                    saldo_devedor = C
                juros = saldo_devedor * i
                amortizacao = P - juros
                saldo_devedor = saldo_devedor - amortizacao
                df = pd.concat([df,pd.DataFrame([[item,P,juros,amortizacao,saldo_devedor]],columns=['Parcela','Valor','Juros','Amortização','Saldo Devedor'])],ignore_index=True)  
                df = df.round({'Valor': 2, 'Juros': 2, 'Amortização': 2, 'Saldo Devedor': 2})
            
            return df
        
        else:

            A = self.monthly_payment
            C = self.loan_amount
            i = self.interest_rate
            n = self.months

            P = C * (((1 + i)**n)*i)/(((1 + i)**n)-1)
            
            df = pd.DataFrame(columns=['Parcela','Valor','Juros','Amortização','Saldo Devedor'])
            for  item in range(1,n+1):
                if item == 1:
                    saldo_devedor = C
                juros = saldo_devedor * i
                amortizacao = P - juros
                saldo_devedor = saldo_devedor - amortizacao
                df = pd.concat([df,pd.DataFrame([[item,P,juros,amortizacao,saldo_devedor]],columns=['Parcela','Valor','Juros','Amortização','Saldo Devedor'])],ignore_index=True)  
                df = df.round({'Valor': 2, 'Juros': 2, 'Amortização': 2, 'Saldo Devedor': 2})
            
            return df
    
    def sac_table(self,variant = None):
        
        if variant == 'bcb':
            C = self.loan_amount
            i = self.bcb_interest
            n = self.months
            A = self.monthly_payment
            
            
            df = pd.DataFrame(columns=['Parcela','Taxa','Valor','Juros','Juros Acum.','Amortização','Saldo Devedor'])
            for  item in range(1,n+1):
                amortizacao = C/n
                if item == 1:
                    saldo_devedor = C
                    juros = saldo_devedor * i
                    P = amortizacao + juros
                    sum_juros = juros
                else:
                    saldo_devedor = C - (amortizacao * (item-1))
                    juros = saldo_devedor * i
                    P = amortizacao + juros
                    sum_juros += juros
                
                df = pd.concat([df,pd.DataFrame([[item,i * 100,P,juros,sum_juros,amortizacao,saldo_devedor]],columns=['Parcela','Taxa','Valor','Juros','Juros Acum.','Amortização','Saldo Devedor'])],ignore_index=True)
                df = df.round({'Valor': 2, 'Juros': 2, 'Juros Acum.':2 , 'Amortização': 2, 'Saldo Devedor': 2})
            return df
        
        
        elif variant == 'effective':
            C = self.loan_amount
            i = self.effective_interest_rate
            n = self.months
            A = self.monthly_payment
            
            
            
            df = pd.DataFrame(columns=['Parcela','Taxa','Valor','Juros','Juros Acum.','Amortização','Saldo Devedor'])
            for  item in range(1,n+1):
                amortizacao = C/n
                if item == 1:
                    saldo_devedor = C
                    juros = saldo_devedor * i
                    P = amortizacao + juros
                    sum_juros = juros
                else:
                    saldo_devedor = C - (amortizacao * (item-1))
                    juros = saldo_devedor * i
                    P = amortizacao + juros
                    sum_juros += juros
                
                df = pd.concat([df,pd.DataFrame([[item,i * 100,P,juros,sum_juros,amortizacao,saldo_devedor]],columns=['Parcela','Taxa','Valor','Juros','Juros Acum.','Amortização','Saldo Devedor'])],ignore_index=True)
                df = df.round({'Valor': 2, 'Juros': 2, 'Juros Acum.':2 , 'Amortização': 2, 'Saldo Devedor': 2})
            return df
        
        
        else:
            C = self.loan_amount
            i = self.interest_rate
            n = self.months
            A = self.monthly_payment
            
            
            
            df = pd.DataFrame(columns=['Parcela','Taxa','Valor','Juros','Juros Acum.','Amortização','Saldo Devedor'])
            for  item in range(1,n+1):
                amortizacao = C/n
                if item == 1:
                    saldo_devedor = C
                    juros = saldo_devedor * i
                    P = amortizacao + juros
                    sum_juros = juros
                else:
                    saldo_devedor = C - (amortizacao * (item-1))
                    juros = saldo_devedor * i
                    P = amortizacao + juros
                    sum_juros += juros
                
                df = pd.concat([df,pd.DataFrame([[item,i * 100,P,juros,sum_juros,amortizacao,saldo_devedor]],columns=['Parcela','Taxa','Valor','Juros','Juros Acum.','Amortização','Saldo Devedor'])],ignore_index=True)
                df = df.round({'Valor': 2, 'Juros': 2, 'Juros Acum.':2 , 'Amortização': 2, 'Saldo Devedor': 2})
            return df
        
        
    
    def mejs_table(self, variant = None):
        
        if variant == 'bcb':
            C = self.loan_amount
            i = self.bcb_interest
            n = self.months
            A = self.monthly_payment

            sfva = 0
            for  item in range(1,n+1):
                sfva += (1/(1+(i*item)))
            P = C/sfva
            df = pd.DataFrame(columns=['Parcela','Valor','Juros','Amortização','Saldo Devedor'])

            for  item in range(1,n+1):
                if item == 1:
                    saldo_devedor = C
                    fva = 1/(1+(i*item))
                    juros = saldo_devedor * i
                    amortizacao = saldo_devedor * fva
                else:
                    fva = 1/(1+(i*item))
                    amortizacao = P * fva
                    saldo_devedor = saldo_devedor -(amortizacao)
                    juros = P - amortizacao
                df = pd.concat([df,pd.DataFrame([[item,P,juros,amortizacao,saldo_devedor]],columns=['Parcela','Valor','Juros','Amortização','Saldo Devedor'])],ignore_index=True)
                df = df.round({'Valor': 2, 'Juros': 2, 'Amortização': 2, 'Saldo Devedor': 2})
            return df
        
        elif variant == 'effective':
            C = self.loan_amount
            i = self.effective_interest_rate
            n = self.months
            A = self.monthly_payment

            sfva = 0
            for  item in range(1,n+1):
                sfva += (1/(1+(i*item)))
            P = C/sfva
            df = pd.DataFrame(columns=['Parcela','Valor','Juros','Amortização','Saldo Devedor'])

            for  item in range(1,n+1):
                if item == 1:
                    saldo_devedor = C
                    fva = 1/(1+(i*item))
                    juros = saldo_devedor * i
                    amortizacao = saldo_devedor * fva
                else:
                    fva = 1/(1+(i*item))
                    amortizacao = P * fva
                    saldo_devedor = saldo_devedor -(amortizacao)
                    juros = P - amortizacao
                df = pd.concat([df,pd.DataFrame([[item,P,juros,amortizacao,saldo_devedor]],columns=['Parcela','Valor','Juros','Amortização','Saldo Devedor'])],ignore_index=True)
                df = df.round({'Valor': 2, 'Juros': 2, 'Amortização': 2, 'Saldo Devedor': 2})
            return df
            
        else:
            C = self.loan_amount
            i = self.interest_rate
            n = self.months
            A = self.monthly_payment

            sfva = 0
            for  item in range(1,n+1):
                sfva += (1/(1+(i*item)))
            P = C/sfva
            df = pd.DataFrame(columns=['Parcela','Valor','Juros','Amortização','Saldo Devedor'])

            for  item in range(1,n+1):
                if item == 1:
                    saldo_devedor = C
                    fva = 1/(1+(i*item))
                    juros = saldo_devedor * i
                    amortizacao = saldo_devedor * fva
                else:
                    fva = 1/(1+(i*item))
                    amortizacao = P * fva
                    saldo_devedor = saldo_devedor -(amortizacao)
                    juros = P - amortizacao
                df = pd.concat([df,pd.DataFrame([[item,P,juros,amortizacao,saldo_devedor]],columns=['Parcela','Valor','Juros','Amortização','Saldo Devedor'])],ignore_index=True)
                df = df.round({'Valor': 2, 'Juros': 2, 'Amortização': 2, 'Saldo Devedor': 2})
            return df

    def resume_table(self):

        A = self.monthly_payment
        n = self.months
        efetivo_abusivo = None
        efetivo_superAbusivo = None
        nominal_abusivo = None
        nominal_superAbusivo = None



        juro_bcb = round(self.bcb_interest,7)*100
        juro_bcb = "{:7f}".format(juro_bcb)
        juro_nominal= round(self.interest_rate,7)*100
        
        if juro_nominal > float(1.5)*float(juro_bcb):
            nominal_superAbusivo = 'Sim'
            nominal_abusivo = 'Sim'

        elif juro_nominal > float(1.1)*float(juro_bcb):
            nominal_abusivo = 'Sim'
            nominal_superAbusivo = 'Não'

        else:
            nominal_abusivo = 'Não'
            nominal_superAbusivo = 'Não'

        juro_nominal = "{:7f}".format(juro_nominal)

        juro_efetivo = round(self.effective_interest_rate,7)*100
        if juro_efetivo > float(1.5)*float(juro_bcb):
            efetivo_superAbusivo = 'Sim'
            efetivo_abusivo = 'Sim'
        elif juro_efetivo > float(1.1)*float(juro_bcb):
            efetivo_abusivo = 'Sim'
            efetivo_superAbusivo = 'Não'

        else:
            efetivo_abusivo = 'Não'
            efetivo_superAbusivo = 'Não'


        juro_efetivo = "{:7f}".format(juro_efetivo)

        df_price_bcb = self.price_table(variant='bcb')
        df_price_bcb_parcela = self.price_table(variant='bcb').head(1)

        if round((A * n) - df_price_bcb['Valor'].sum(),2) <= 0:
            df_price_bcb_beneficio = 0
        else:
            df_price_bcb_beneficio = round((A * n) - df_price_bcb['Valor'].sum(),2)

        df_price_effective = self.price_table(variant='effective')
        df_price_effective_parcela = self.price_table(variant='effective').head(1)

        if round((A * n) - df_price_effective['Valor'].sum(),2) <= 0:
             df_price_effective_beneficio = 0
        else:
            df_price_effective_beneficio = round((A * n) - df_price_effective['Valor'].sum(),2)

        df_price_nominal = self.price_table()
        df_price_nominal_parcela = self.price_table().head(1)

        if round((A * n) - df_price_nominal['Valor'].sum(),2) <= 0:
            df_price_nominal_beneficio = 0
        else:
            df_price_nominal_beneficio = round((A * n) - df_price_nominal['Valor'].sum(),2)

        df_mejs_bcb = self.mejs_table(variant='bcb')
        df_mejs_bcb_parcela = self.mejs_table(variant='bcb').head(1)

        if round((A * n) - df_mejs_bcb['Valor'].sum(),2) <= 0:
            df_mejs_bcb_beneficio = 0
        else:
            df_mejs_bcb_beneficio = round((A * n) - df_mejs_bcb['Valor'].sum(),2)

        
        df_mejs_effective = self.mejs_table(variant='effective')
        df_mejs_effective_parcela = self.mejs_table(variant='effective').head(1)

        if round((A * n) - df_mejs_effective['Valor'].sum(),2) <= 0:
            df_mejs_effective_beneficio = 0
        else:
            df_mejs_effective_beneficio = round((A * n) - df_mejs_effective['Valor'].sum(),2)

        
        df_mejs_nominal = self.mejs_table()
        df_mejs_nominal_parcela = self.mejs_table().head(1)
        
        if round((A * n) - df_mejs_nominal['Valor'].sum(),2) <= 0:
            df_mejs_nominal_beneficio = 0
        else:
            df_mejs_nominal_beneficio = round((A * n) - df_mejs_nominal['Valor'].sum(),2)

        df_sac_bcb = self.sac_table(variant='bcb')
        df_sac_bcb_parcela = self.sac_table(variant='bcb').head(1)

        if round((A * n) - df_sac_bcb['Valor'].sum(),2) <= 0:
            df_sac_bcb_beneficio = 0
        else:
            df_sac_bcb_beneficio = round((A * n) - df_sac_bcb['Valor'].sum(),2)

        df_sac_effective = self.sac_table(variant='effective')
        df_sac_effective_parcela = self.sac_table(variant='effective').head(1)

        if round((A * n) - df_sac_effective['Valor'].sum(),2) <= 0:
            df_sac_effective_beneficio = 0
        else:
            df_sac_effective_beneficio = round((A * n) - df_sac_effective['Valor'].sum(),2)


        df_sac_nominal = self.sac_table()
        df_sac_nominal_parcela = self.sac_table().head(1)

        if round((A * n) - df_sac_nominal['Valor'].sum(),2) <= 0:
            df_sac_nominal_beneficio = 0
        else:
            df_sac_nominal_beneficio = round((A * n) - df_sac_nominal['Valor'].sum(),2)

        df = pd.DataFrame(columns=['Juros Remuneratórios (%)','Juro Abusivo(+10%)?','Juro Super Abusivo(+50%) ?','Valor Parcela Price', 'Benefício Sistema Price','Valor Parcela MEJS','Benefício Sistema MEJS','Valor Parcela SAC', 'Beneficio Sistema SAC'])  
        df = pd.concat([df,pd.DataFrame([[f'Taxa Efetiva - {juro_efetivo}',efetivo_abusivo,efetivo_superAbusivo,df_price_effective_parcela['Valor'][0],df_price_effective_beneficio,df_mejs_effective_parcela['Valor'][0],df_mejs_effective_beneficio,df_sac_effective_parcela['Valor'][0],df_sac_effective_beneficio]],columns=['Juros Remuneratórios (%)','Juro Abusivo(+10%)?','Juro Super Abusivo(+50%) ?','Valor Parcela Price', 'Benefício Sistema Price','Valor Parcela MEJS','Benefício Sistema MEJS','Valor Parcela SAC', 'Beneficio Sistema SAC'])],ignore_index=True)
        df = pd.concat([df,pd.DataFrame([[f'Taxa Nominal - {juro_nominal}',nominal_abusivo,nominal_superAbusivo,df_price_nominal_parcela['Valor'][0],df_price_nominal_beneficio,df_mejs_nominal_parcela['Valor'][0],df_mejs_nominal_beneficio,df_sac_nominal_parcela['Valor'][0],df_sac_nominal_beneficio]],columns=['Juros Remuneratórios (%)','Juro Abusivo(+10%)?','Juro Super Abusivo(+50%) ?','Valor Parcela Price', 'Benefício Sistema Price','Valor Parcela MEJS','Benefício Sistema MEJS','Valor Parcela SAC', 'Beneficio Sistema SAC'])],ignore_index=True)
        df = pd.concat([df,pd.DataFrame([[f'Taxa BACEN - {juro_bcb}','-','-',df_price_bcb_parcela['Valor'][0],df_price_bcb_beneficio,df_mejs_bcb_parcela['Valor'][0],df_mejs_bcb_beneficio,df_sac_bcb_parcela['Valor'][0],df_sac_bcb_beneficio]],columns=['Juros Remuneratórios (%)','Juro Abusivo(+10%)?','Juro Super Abusivo(+50%) ?','Valor Parcela Price', 'Benefício Sistema Price','Valor Parcela MEJS','Benefício Sistema MEJS','Valor Parcela SAC', 'Beneficio Sistema SAC'])],ignore_index=True)
        df = df.round({'parcela price': 2, 'beneficio price': 2, 'parcela mejs': 2, 'beneficio mejs': 2, 'parcela sac': 2, 'beneficio sac': 2})
        
        return df

        

        




    
        
    

        
