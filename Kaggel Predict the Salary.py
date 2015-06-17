import numpy as np
import scipy as sp
import pandas as pd
import csv
from matplotlib import pyplot as plt

def remove_nan(criteria):
    result = []
    for e in criteria:
        if e == e:
            result.append(e)
        else:
            break
    return result

def change_nan(data):
    result = []
    for e in data:
        if e == e and e != None:
            result.append(e)
        else:
            result.append('others')
    return result

def change_extra(test, train):
    result = []
    for e in test:
        if e in train:
            result.append(e)
        else:
            result.append('others')
    return result
    

def job_level(title):
    result = []
    for a in title:
        if a == a:
            if a.find('apprentice') or a.find('intern'):
                result.append('level 0')
            elif a.find('assist') or a.find('worker') or \
            a.find('technician') or a.find('support'):
                result.append('level 1')   
            elif a.find('senior') and a.find('manage'):
                result.append('level 4')
            elif a.find('senior') or a.find('midlevel') or\
            a.find('level2') or a.find('level 2') or\
            a.find('level3') or a.find('level 3') or\
            a.find('mid level') or a.find('lead'):
                result.append('level 3')
            elif a.find('director'):
                result.append('level 5')
            elif a.find('vice president'):
                result.append('level 6')
            elif a.find('ceo') or a.find('chief') or a.find('cfo') or\
            a.find('cto'):
                result.append('level 7')
            else:
                result.append('level 2')
        else:
            result.append('level 2')
    return result         

def factor_salary(factor_t, salary_t, factor, factors):
    count = [0] * len(factor)
    money = [0] * len(factor)
    added = 0
    
    for e in range(len(factor_t)):
        added = 0
        for f in range(len(factor)):
            if factor_t[e] == factor[f]:
                money[f] += salary_t[e]
                count[f] += 1
                added = 1
                break
        if added == 0:
            money[0] += salary_t[e]
            count[0] += 1

    for e in range(len(money)):
        if count[e] == 0:
            count[e] = 1
            
        factors[factor[e]] = money[e] / count[e]

    return factors

def function_salary(title_t, salary_t, title, factors):
    count = [0] * 8
    money = [0] * 8
    added = 0
    for e in range(len(title_t)):
        added = 0
        a = title_t[e].lower()
        if a.find('apprentice') or a.find('intern'):
            money[0] += salary_t[e]
            count[0] += 1
            added = 1
            title_t[e] = title[0]
            break
        elif a.find('assist') or a.find('worker') or \
        a.find('technician') or a.find('support'):
            money[1] += salary_t[e]
            count[1] += 1
            added = 1
            title_t[e] = title[1]
            break
        elif a.find('senior') and a.find('manage'):
            money[4] += salary_t[e]
            count[4] += 1
            added = 1
            title_t[e] = title[4]
            break
        elif a.find('senior') or a.find('midlevel') or\
        a.find('level2') or a.find('level 2') or\
        a.find('level3') or a.find('level 3') or\
        a.find('mid level') or a.find('lead'):
            money[3] += salary_t[e]
            count[3] += 1
            title_t[e] = title[3]
            added = 1
            break
        elif a.find('director'):
            money[5] += salary_t[e]
            count[5] += 1
            added = 1
            title_t[e] = title[5]
            break
        elif a.find('vice president'):
            money[6] += salary_t[e]
            count[6] += 1
            added = 1
            title_t[e] = title[6]
            break
        elif a.find('ceo') or a.find('chief') or a.find('cfo') or\
        a.find('cto'):
            moeny[7] += salary_t[e]
            count[7] += 1
            added = 1
            title_t[e] = title[7]
            break

        if added == 0:
            money[2] += salary_t[e]
            count[2] += 1
            title_t[e] = title[2]

    for e in range(len(money)):
        if count[e] == 0:
            count[e] = 1

        factors[title[e]] = money[e] / count[e]

    return factors
                       

def model():
    factors = {}
    
    data = pd.read_csv("train.csv")

    criteria = pd.read_csv("criteria.csv")

    title = remove_nan(criteria['Title'])
    c_type = remove_nan(criteria['ContractType'])
    c_time = remove_nan(criteria['ContractTime'])
    category = remove_nan(criteria['Category'])
    location = remove_nan(criteria['LocationNormalized'])
                          
    title_t = job_level(data['Title'])
    c_type_t = change_nan(data['ContractType'])
    c_time_t = change_nan(data['ContractTime'])
    category_t = change_nan(data['Category'])
    location_t = change_nan(data['LocationNormalized'])
    salary_t = change_nan(data['SalaryNormalized'])

    factors = factor_salary(c_type_t, salary_t, c_type, factors)
    factors = factor_salary(c_time_t, salary_t, c_time, factors)
    factors = factor_salary(category_t, salary_t, category, factors)
    factors = factor_salary(location_t, salary_t, location, factors)
    factors = function_salary(title_t, salary_t, title, factors)

    y = salary_t
    x = []
    for e in range(len(salary_t)):
        wrap = []
        wrap.append(factors[title_t[e]])
        wrap.append(factors[location_t[e]])
        wrap.append(factors[c_type_t[e]])
        wrap.append(factors[c_time_t[e]])
        wrap.append(factors[category_t[e]])
        x.append(wrap)

    X = np.vstack(x)
    coeffs = np.linalg.lstsq(X,y)[0]

    data = pd.read_csv("test.csv")

    title_t = job_level(data['Title'])
    c_type_t = change_nan(data['ContractType'])
    c_time_t = change_nan(data['ContractTime'])
    category_t = change_nan(data['Category'])
    location_t = change_nan(data['LocationNormalized'])

    c_type_t = change_extra(c_type_t, c_type)
    c_time_t = change_extra(c_time_t, c_time)
    category_t = change_extra(category_t, category)
    location_t = change_extra(location_t, location)

    x = []
    for e in range(len(title_t)):
        wrap = []
        wrap.append(factors[title_t[e]])
        wrap.append(factors[location_t[e]])
        wrap.append(factors[c_type_t[e]])
        wrap.append(factors[c_time_t[e]])
        wrap.append(factors[category_t[e]])
        x.append(wrap)

    X = np.vstack(x)

    pred = np.dot(X, coeffs)
    ID = change_nan(data['Id'])

    data = {}

    data = {'Id' : ID, 'PredictedSalary' : pred}

    df = pd.DataFrame(data)

    df.to_csv('Jaycy.G result.csv', delimiter = ',')
     


    
        
    

    
