# -*- coding: utf-8 -*-
"""
Created on Wed May 19 16:34:14 2021

@author: cody.schiffer
"""
import pandas as pd

from sqlalchemy import create_engine
from datetime import datetime, timedelta


#all_ips = pd.read_csv('C:/Users/cody.schiffer/Documents/ip_addresses_to_analyze_05_13_2021.csv')

def get_counts(date):
    print("date passed", date)
    all_click_queries = """SELECT *
                            FROM ome_alert_tracking
                            where click_date >= '{}'
                            and solr_id NOT like '%%email_open%%'""".format(date)


    user_click_queries = """SELECT idome_alert_tracking, user, solr_id, DATE_FORMAT(click_date, "%Y-%m-%d %H:%i:%S") as click_date
                        FROM ome_alert_tracking
                        where click_date >= '{}'
                        and solr_id NOT LIKE "%%email_open%%"
                        and (user LIKE '%%elt%%' 
                        OR user LIKE '%%vant%%'
                        OR user LIKE '%%aces%%'
                        OR user like '%%myovant%%'
                        or user like '%%masa%%'
                        or user like '%%myrtle.potter%%'
                        or user like '%%dsp_gbd%%'
                        or user like '%%kenton_stewart%%'
                        or user like '%%rob%%'
                        or user like '%%chris%%'
                        or user like '%%jasmine%%'
                        or user like '%%frank%%'
                        or user like '%%mark%%'
                        or user like '%%yuval%%'
                        or user like '%%gaelle%%'
                        or user like '%%masato_yabuki%%'
                        or user like '%%redirect_user%%')""".format(date)
                                                
                        
    email_open_queries = """SELECT idome_alert_tracking, user, solr_id,  DATE_FORMAT(click_date, "%Y-%m-%d %H:%i:%S") as click_date
                        FROM ome_alert_tracking
                        where click_date >= '{}'
                        and solr_id LIKE "%%email_open%%"
                        and (user LIKE '%%elt%%' 
                        OR user LIKE '%%vant%%'
                        OR user LIKE '%%aces%%'
                        OR user like '%%myovant%%'
                        or user like '%%masa%%'
                        or user like '%%myrtle.potter%%'
                        or user like '%%dsp_gbd%%'
                        or user like '%%kenton_stewart%%'
                        or user like '%%rob%%'
                        or user like '%%chris%%'
                        or user like '%%jasmine%%'
                        or user like '%%frank%%'
                        or user like '%%mark%%'
                        or user like '%%yuval%%'
                        or user like '%%gaelle%%'
                        or user like '%%masato_yabuki%%'
                        or user like '%%redirect_user%%')""".format(date)
                        
    with open('/root/Documents/joqim/UserEngagement_FE/api/yoann_sql_access.txt', 'r') as myfile:
        yoann_sql_pw = myfile.read().rstrip()

    #db_connection_str = 'mysql://roivant:'+ str(yoann_sql_pw) + '@184.72.215.98/ome_alert_public'
    db_connection_str = 'mysql://roivant:'+ str(yoann_sql_pw) + '@10.115.3.177/ome_alert_public'
    db_connection = create_engine(db_connection_str)
    
    all_clicks_df = pd.read_sql(all_click_queries, con = db_connection)

    user_clicks_df = pd.read_sql(user_click_queries, con = db_connection)
    
    email_open_df = pd.read_sql(email_open_queries, con = db_connection)
    
    #Need to clean up the ips to remove the dynamic portion
    clicks_df = get_unique_ips(user_clicks_df)
    email_open_df = get_unique_ips(email_open_df)
    all_clicks_df = get_unique_ips(all_clicks_df)
    
    return all_clicks_df, clicks_df, email_open_df

def clean_ips(ls_item):
    actual_ip = ls_item.split('_')[-1]
    split_ip = actual_ip.split('.')
    dynamic_ip_address = split_ip[-1]
    
    
    #Remove the dynamic_ip_address from the split ip address
    if split_ip.count(dynamic_ip_address) <= 1:
        split_ip.remove(dynamic_ip_address)
        
    new_ip = '.'.join(split_ip)
    
    new_engagement_track = ls_item.replace(actual_ip, new_ip)
    
    return new_engagement_track

def get_unique_ips(df):
     
    #NOTE evaluate clean_ips() output data structure to convert to json format 
    df['user'] = df['user'].apply(lambda x: clean_ips(x))
    
    return df

def turn_to_datetime(string):
    datetime_object = datetime.strptime(str(string), '%Y-%m-%d %H:%M:%S')
    return datetime_object
    
def rounding_the_click_date(dt, delta):
    
    dt_datetime = datetime.strptime(str(dt),'%Y-%m-%d %H:%M:%S')
    
    rounded = dt_datetime - (dt_datetime - datetime.min) % timedelta(seconds = delta)
    return rounded
    
def comparing_date_rows(df, timelimit):
    
    #Turn the click date into a proper 
    df['click_date'] = df['click_date'].apply(lambda x: turn_to_datetime(x))
    
    #Turn the click datetime into a rounded version for easier groupby
    df['rounded_click_date'] = df['click_date'].apply(lambda x: rounding_the_click_date(dt = x, delta = timelimit))
    
    grouped = df.groupby(['user','solr_id']).nunique()[['rounded_click_date']].reset_index(inplace = False)

    return df, grouped        


def clicks_opens_metrics_reporting(df, clicks = True):
    
    df_per_user = df
    
    df_per_user['user'] = df_per_user['user'].apply(lambda x: x.replace(x.split('_')[-1], ''))
    
    
    per_user = df.groupby(['user'])[['rounded_click_date']].sum().reset_index(inplace = False)
    # if desig = 'clicks'
    #     per_user = df.groupby(['user'])[['rounded_click_date']].sum().reset_index(inplace = False)
    # elif desig = 'opens':
    #     per_user = df.groupby(['user'])[['rounded_click_date']].count().reset_index(inplace = False)
    
    groups_per_user = df.groupby(['user'])['solr_id'].apply(list)
    
    list_per_user = groups_per_user.reset_index(name = 'doc_ids' )
    
    if clicks: 
        per_user = translate_user_names(per_user)
        print(per_user, '--- this clicks per user')
        all_non_comp_res = per_user['rounded_click_date'].sum()
    else:
        per_user = per_user.rename(columns = {'rounded_click_date':'rounded_open_date'})
        per_user = translate_user_names(per_user)
        print(per_user, '---- this is opens per user')
        
        all_non_comp_res = per_user['rounded_open_date'].sum()
    
    return per_user, all_non_comp_res, list_per_user
    
def unique_ip_engagement_metrics_reporting(df, engagement_type = 'opens'):
    
    len_unique_users_ips = len(df['user'].unique())
    
    unique_user_ips = list(df['user'].unique())
    
    
    
    if engagement_type == 'opens':
        print('There were {} unique IP addresses opening emails this week'.format(len_unique_users_ips))
        return unique_user_ips
    elif engagement_type == 'clicks':
        print('There were {} unique IP addresses clicking emails this week'.format(len_unique_users_ips))
        return unique_user_ips
    elif engagement_type == 'both':
        print('There were {} unique IP addresses clicking and opening emails this week'.format(len_unique_users_ips))
        return unique_user_ips
        
def translate_user_names(df):
    translation = {
        'redirect_user_001_': "myrtle.potter",
        'redirect_user_002_':"elt.elt",
        'redirect_user_003_':"vant.vant",
        'redirect_user_004_': 'masa.masa',
        'redirect_user_005_': 'myovant.myovant',
        'redirect_user_006_':'dsp_gbd.dsp_gbd',
        'redirect_user_007_':'kenton_stewart.kenton_stewart',
        'redirect_user_008_':'Urovant BD Efforts',
        'redirect_user_010_':'aces.aces',
        'redirect_user_011_':'rob_jacobson.rob_jacobson',
        'redirect_user_012_':'jasmine_carvalho.jasmine_carvalho',
        'redirect_user_013_':'mark_niemaszek.mark_niemaszek',
        'redirect_user_014_':'yuval_harel.yuval_harel',
        'redirect_user_015_':'jenny_alltoft.jenny_alltoft',
        'redirect_user_016_':'masato_yabuki.masato_yabuki',
        'redirect_user_017_':'gaelle.mercenne',
        'redirect_user_018_' : 'urovant_rdlt',
        'redirect_user_019_': 'james_robinson',
        'redirect_user_020_' :'sumitovant_pr',
        'redirect_user_021_' : 'hayes_dansky',
        'redirect_user_022_' : 'jim_luterman',
        "redirect_user_023" : "MDD News Alerts",
        "redirect_user_024_": "James Robinson",
        "redirect_user_025_": "Full Urovant",
        "redirect_user_026_" : "Chris Elia",
        "redirect_user_027_": "Urovant RDLT",
        "redirect_user_028_":"Urovant Corporate Communications"

        }
    
    df['user'] = df['user'].map(translation)



    return df