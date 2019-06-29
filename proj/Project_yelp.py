# !/usr/bin/python

import pymysql
import matplotlib.pyplot as plt
from itertools import groupby
import numpy as np
import scipy.stats as stats
from sklearn.cluster import KMeans

def open_conn():
    """open the connection before each test case"""
    conn = pymysql.connect(user='root', password='202020',
                                   host='localhost',
                                   database='yelp_db')

    return conn

def close_conn(conn):
    """close the connection after each test case"""
    conn.close()
    
def executeQuery(conn, query, commit=False):
    """ fetch result after query"""
    cursor = conn.cursor()
    query_num = query.count(";")
    if query_num > 1:
        for result in cursor.execute(query, params=None, multi=True):
            if result.with_rows:
                result = result.fetchall()
    else:
        cursor.execute(query)
        result = cursor.fetchall()
    # we commit the results only if we want the updates to the database
    # to persist.
    if commit:
        conn.commit()
    else:
        conn.rollback()
    # close the cursor used to execute the query
    cursor.close()
    return result

# ======================================Question 1==============================================
def rating_in_time_series():
    #fetch results from the database
    sql = "select date, stars from review where business_id='4JNXUYY8wbaaDmk3BPzlWw' order by date;"
    result = executeQuery(conn, sql)
    #retreive results as a list from the list of tuples, list(group)
    result_list = [list(group) for key, group in groupby(result, key=lambda x:x[0])]

    date_list = [key for key, group in groupby(result, key=lambda x:x[0])]
    rating_list = []

    for group in result_list:
        total = []
        for ele in group:
            total.append(ele[1])
        rating_list.append(total)
    avg_rating, cnt = [0], 0

    num_review_to_now = []
    for ratings in rating_list:
        sum_uptonow = cnt*avg_rating[-1] 
        cnt += len(ratings)
        num_review_to_now.append(len(ratings))
        sum_after = sum(ratings) + sum_uptonow
        avg_now = float(sum_after/cnt)
        avg_rating.append(avg_now)
    avg_rating = avg_rating[1:]
    #plot results

    x = date_list
    y = avg_rating
    plt.figure(figsize=(10,6))
    l1, = plt.plot(x, y, color='red')

    plt.xlabel('Day after the first review')
    plt.ylabel('Average Rating Up to Now')
    plt.legend(handles = [l1,], labels = ['ID: 4JNXUYY8wbaaDmk3BPzlWw'], loc = 'best')
    plt.ylim(0, 5) 
    plt.show()
    
    plt.figure(figsize=(10,6))
    plt.bar(x, num_review_to_now, width=10, color='royalblue')  

    plt.xlabel('Day after the first review')
    plt.ylabel('Total number of reviews')
    plt.show()
    return 


# =====================================Question 2===============================================

def get_correlation_rate(x, y, response, compare='Text'):
    '''Return the correlation of two variables'''
    print('The correlation between %s and %s Length is %f, and the confidence level is %f' %(response, compare, stats.pearsonr(x, y)[0], stats.pearsonr(x, y)[1]))
    return

def Get_closest(num, ever):
    index, difference = 0, 5
    for i in range(len(ever)):
        dif = abs(float(num)-float(ever[i]))
        if dif <= difference:
            difference = dif
            index = i
    return ever[index]

def Rating_Based_Past():
    '''Predict based on past at certain confidence level'''
    confidence = 0.4
    
    sql = "select ROUND(convert(F1.stars,decimal),1), ROUND(F2.Avg,1) from (select business_id, stars from review where user_id='CxDOIDnH8gp9KXzpBHJYXw') as F1 natural join (select business_id, avg(stars) as Avg from review where business_id in (select distinct business_id from review where user_id = 'CxDOIDnH8gp9KXzpBHJYXw') group by business_id) as F2;"
    result = executeQuery(conn, sql)
    points = np.array(result)
    #print(points)
    #get_correlation_rate(points[:,0], points[:,1], 'Average_Rating', 'User_Rating')
    #count the frequency of every tuple (user, average) and total number of average in the form
    #{4.5:{3: 1, 4: 2, 5: 1, subtotal:4}} means 1 (4.5, 3) 2(4.5, 4) 1(4.5, 5) 4 in total
    dic_avg = dict()
    cnt = 0
    for user, average in points:
        sub = dic_avg.setdefault(str(average), dict())
        sub[user] = sub.setdefault(user, [0])
        sub[user][-1] += 1
        dic_avg[str(average)][user] = sub[user]
        dic_avg[str(average)]['sub_total'] = dic_avg[str(average)].setdefault('sub_total',0 ) + 1 
        cnt += 1
    avg_ever_been_to = list(dic_avg.keys())
    
    # find out tuples whose confidence level is higher than pre-set confidence, thus udner this confidence level we have
    # average -> user rating  
    for avg_rat in dic_avg:
        for user_rating in dic_avg[avg_rat]:
            if user_rating != 'sub_total':
                confidence_level = float(dic_avg[avg_rat][user_rating][-1])/float(dic_avg[avg_rat]['sub_total'])
                dic_avg[avg_rat][user_rating].append(confidence_level)
                print('Average Rating: %s    User Rating: %s   Frequency: %3d   Confidence Level: %f'%(avg_rat, str(user_rating), dic_avg[avg_rat][user_rating][0], dic_avg[avg_rat][user_rating][1]))
    while True:
        average_rating = str(input('Given the average rating of this restaurant:'))
        average_rating = Get_closest(average_rating, avg_ever_been_to)
        print('According to the record of the user')
        find = False
        for user_rating in dic_avg[average_rating]:
            if user_rating != 'sub_total':
                confidence_level = dic_avg[average_rating][user_rating][-1]
                if confidence_level >= confidence:
                    find = True
                    print('The user might rate the business as: %d with the probability of %d %%'%(user_rating, confidence_level*100))
        if not find:
            print('No prediction could be made under this confidence level: %d'%(confidence))
    return

# =================================Question 3===================================================
def get_percentage(x_labels, ufc_labels):
    '''Computes the percentage of getting at least one response of the length range'''
    percentage = dict()
    for index in range(len(x_labels)):
        percentage[x_labels[index]] = percentage.setdefault(x_labels[index], [0, 0])
        percentage[x_labels[index]][0] += 1
        if ufc_labels[index] > 0:
            percentage[x_labels[index]][1] += 1
    x, y= [], []
    for key in percentage:
        x.append(key)
        y.append(float(percentage[key][1])/float(percentage[key][0]))
    return percentage, x, y


def length_and_useful():
    '''relation between length and useful'''
    #fetch results from the database
    sql = "select text, useful, funny, cool from review;"
    result = executeQuery(conn, sql)
    #every length_range as a group
    length_range = 40
    
    #retreive results as a list from the list of tuples, list(group) get [(date1, rating1), (date1, rating2)]
    x_labels = np.array([len(sub[0].split())/length_range for sub in result])
    #get text_lengtj and every 50 as a group 0-50 50-100 100-150
    useful_labels = np.array([sub[1] for sub in result])
    funny_labels = np.array([sub[2] for sub in result])
    cool_labels = np.array([sub[3] for sub in result])
    #get possibility to get at least one response
    per_get_useful, x1, y1 = get_percentage(x_labels, useful_labels)
    per_get_funny , x2, y2 = get_percentage(x_labels,  funny_labels)
    per_get_cool  , x3, y3 = get_percentage(x_labels,   cool_labels)
    
    get_correlation_rate(x1, y1, 'Useful')
    get_correlation_rate(x2, y2, 'Funny')
    get_correlation_rate(x3, y3, 'Cool')

    plt.figure(figsize=(20,10))
    l1, = plt.plot(x1, y1, color='yellowgreen')
    l2, = plt.plot(x2, y2, color='tomato')
    l3, = plt.plot(x3, y3, color='cornflowerblue')

    plt.xlabel('Text length range')
    plt.ylabel('Possibility to get related feedback')

    plt.legend(handles = [l1, l2, l3,], labels = ['Useful', 'Funny', 'Cool'], loc = 'best')
    plt.show()
    return

# ====================================================================================

def Clustering(points, x_labels, y_labels, n_clusters=20):
    '''unsupervisored learning'''
    y_pred = KMeans(n_clusters=20, random_state=170).fit_predict(points)
    fig = plt.figure()
    clustering_fig = fig.add_subplot(111)
    clustering_fig.set_title('Clustering based on %s'%(x_labels))
    plt.xlabel(x_labels)
    plt.ylabel(y_labels)
    clustering_fig.set_ylim(ymin=0, ymax=6)
    clustering_fig.scatter(points[:,0], points[:,1], c=y_pred, s=1)
    plt.show()
    return 

# =================================Question 4===================================================

def Get_duration(day_time):
    '''Get duration from Mon|hh:mm-hh:mm and return like 7.5 hours'''
    opt, endt = day_time.split('-')
    op_hour, op_min = opt.split(':')
    end_hour, end_min = endt.split(':')
    hours = int(end_hour)-int(op_hour)
    minutes = int(end_min)-int(op_min)
    if hours <= 0:
        hours += 24
    if minutes < 0:
        hours -= 1
        minutes += 60
    return hours + float(float(minutes)/60)

def Get_Id_Hours_Stars(ids, hours, ratings):
    '''get businessID, Hours, and classify all Ratings'''
    hour_rating = dict()
    for index in range(len(ids)):
        if ids[index] not in hour_rating:
            hour_rating[ids[index]] = hour_rating.setdefault(ids[index], dict())
            hour_rating[ids[index]]['Avg_Stars'] = ratings[index]
            hour_rating[ids[index]]['Operating_hours'] = 0
        hour_rating[ids[index]]['Operating_hours'] += hours[index]

    cnt=0
    for key in hour_rating.keys():
       if hour_rating[key]['Operating_hours'] == 0:
           cnt += 1
           print(key)
    print(cnt)
    return hour_rating

def Percentage_each_rating(operating_Hours, Stars):
    ''''''
    time_step = 4
    operating_hr_after_timerange = []
    hour_average_rating = dict()
    for index in range(len(operating_Hours)):
        time_range = int(operating_Hours[index]/time_step)
        operating_hr_after_timerange.append(time_range)
        if time_range not in hour_average_rating:
            hour_average_rating[time_range] = hour_average_rating.setdefault(time_range, dict())
            hour_average_rating[time_range]['Total'] = 1
            for i in range(1, 6):
                hour_average_rating[time_range][i] = 0
        else:
            hour_average_rating[time_range]['Total'] += 1
        rating = int(Stars[index]/1)
        hour_average_rating[time_range][rating] += 1
    time, percentages = [], [[] for _ in range(5)]
    for hour in hour_average_rating.keys():
        time.append(hour)
        for i in range(5):
            percentages[i].append(float(hour_average_rating[hour][i+1])/float(hour_average_rating[hour]['Total']))
    return time, percentages, operating_hr_after_timerange
    
def plot_cumulative_histogram(normalized_time_sequence, percentages):
    '''plot the percentage of every rating level for each time range'''
    y1, y2, y3, y4, y5 = np.array(percentages[0]), np.array(percentages[1]), np.array(percentages[2]), np.array(percentages[3]), np.array(percentages[4])
    x = normalized_time_sequence
    plt.bar(x, y1, color='teal', label='Rating: 1-2',edgecolor='black')
    plt.bar(x, y2, bottom=y1, color='lightcoral', label='Rating: 2-3')
    plt.bar(x, y3, bottom=y1+y2, color='mediumslateblue', label='Rating: 3-4')
    plt.bar(x, y4, bottom=y1+y2+y3, color='yellow', label='Rating: 4-5')
    plt.bar(x, y5, bottom=y1+y2+y3+y4, color='yellowgreen', label='Rating: 5')
    plt.ylim((0, 1))
    plt.legend(loc=[1, 0], frameon=False) 
    plt.xlabel('Operating Time')
    plt.ylabel('Percentage Of Each Rating')
    plt.show()
    return

def plot_time_distribution(normalized_hours, time_range):
    '''plot the operating hours distribution'''
    plt.figure("hist")
    n, bins, patches = plt.hist(normalized_hours, bins=time_range, normed=1,edgecolor='black',facecolor='yellowgreen') 
    plt.xlabel('Operating Time')
    plt.ylabel('Number of Business')
    plt.show()
    return

def Hours_and_Rating():
    '''Operating hours and Rating'''
    sql = "select hours, business_id, stars from hours H inner join business B on H.business_id = B.id;"

    result = executeQuery(conn, sql)

    id_labels, hours_labels, rating_labels = list(), list(), list()
    for row in result:
        id_labels.append(row[1])
        rating_labels.append(row[2])
        duration = Get_duration(row[0].split('|')[1])
        hours_labels.append(duration)
    hour_rating = Get_Id_Hours_Stars(id_labels, hours_labels, rating_labels)
    
    points = list()
    for business_id in hour_rating.values():
        if business_id['Operating_hours'] > 168:
            business_id['Operating_hours'] = 168
        points.append((business_id['Operating_hours'], business_id['Avg_Stars']))
    points = np.array(points)
    operating_Hours, Stars = points[:,0], points[:,1]
    get_correlation_rate(operating_Hours, Stars, 'Operating Hours', compare='Average_Stars')
    x, percentages, normalized_hours = Percentage_each_rating(operating_Hours, Stars)
    plot_time_distribution(normalized_hours, len(x))
    plot_cumulative_histogram(x, percentages)
    
    Clustering(points, 'Operating Hours', 'Average_Stars', 20)
    return

if __name__ == '__main__':
    #open connection to the database
    conn = open_conn()
    rating_in_time_series()
    length_and_useful()
    #Clustering()
    Hours_and_Rating()
    Rating_Based_Past()
    close_conn(conn)
