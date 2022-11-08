import pandas as pd
from engagement_stats_calc import(
                        get_counts,
                        comparing_date_rows,
                        clicks_opens_metrics_reporting,
                        unique_ip_engagement_metrics_reporting,
                        translate_user_names,
                        clean_ips,
                        get_unique_ips)

from marklogic_queries.retrieve_doc_titles import find_document_title

# from Outlook import Outlook
from datetime import datetime, timedelta


current_time = datetime.now()
weekago = current_time - timedelta(days = 7)
execute_time = weekago.strftime('%Y-%m-%d')

time_for_email = weekago.strftime("%m/%d/%Y")

all_clicks_df, clicks_df, email_open_df = get_counts(date = str(execute_time) + ' 08:00:00')

print("all_clicks_df", all_clicks_df)
print("clicks_df", clicks_df)
print("email_open_df", email_open_df)
print("completed fetch of clicks metrics")

#Applying rounding 
ungrouped_rounded_clicks, rounded_clicks_df = comparing_date_rows(df = clicks_df, timelimit = 3)

ungrouped_rounded_opens, rounded_email_open_df  = comparing_date_rows(df = email_open_df, timelimit = 3)

#Find the unique clicked on docs list:
full_unique_list_of_docs = ungrouped_rounded_clicks['solr_id'].unique()
print(len(full_unique_list_of_docs), '----- this is the number of documents that are clicked on across all alert groups')


#Reading out the final metrics
clicks_per_user, all_non_comp_res_clicks, listed_clicks_doc_ids_per_user = clicks_opens_metrics_reporting(rounded_clicks_df, clicks = True)
opens_per_user, all_non_comp_res_opens, listed_opens_doc_ids_per_user = clicks_opens_metrics_reporting(rounded_email_open_df, clicks = False)

#Email opens ips
unique_open_ips = unique_ip_engagement_metrics_reporting(ungrouped_rounded_opens,engagement_type = 'opens')


#Email clicks ips
unique_click_ips = unique_ip_engagement_metrics_reporting(ungrouped_rounded_clicks,engagement_type = 'clicks')

#email opens and clicks ips
both_clicks_and_opens = pd.concat([ungrouped_rounded_clicks, ungrouped_rounded_opens])
unique_clicks_and_opens_ips = unique_ip_engagement_metrics_reporting(both_clicks_and_opens, engagement_type = 'both')
   

#Print out the number of all clicks including comp res for this week
total_clicks = len(all_clicks_df)



##Retrieve titles for each document clicked on per user, then write to date specific text file

all_users_found_doc_titles = {}

translated_listed_clicks_doc_ids_per_user = translate_user_names(listed_clicks_doc_ids_per_user)

translated_listed_clicks_doc_ids_per_user['user'] = translated_listed_clicks_doc_ids_per_user['user'].fillna('Missing')

for user,ls_of_docids in zip(translated_listed_clicks_doc_ids_per_user['user'],translated_listed_clicks_doc_ids_per_user['doc_ids']):

    unique_titles_per_user = []

    print(user, '--- this is the user we are searching')
    if len(ls_of_docids) > 0:
        for pos, docid in enumerate(ls_of_docids):
            print(str(pos) + '/' + str(len(ls_of_docids)), '---- progress through document list')
            doc_title = find_document_title(test_doc_id = docid)

            if doc_title not in unique_titles_per_user and doc_title != []:

                unique_titles_per_user.append(doc_title)

            else:
                pass

    all_users_found_doc_titles[user] = unique_titles_per_user


with open('./user_title_lists.txt', 'w') as myfile:
    for k,v in all_users_found_doc_titles.items():
        string_of_doc_titles = '\n'.join(v)
        name_of_user = str(k)
        line_break = '\n'

        section_break = '\n --------- \n'

        myfile.write(section_break + name_of_user + ':' + string_of_doc_titles + line_break)



##Find the unique IPs per alerts sent:

ips_per_user_group = ungrouped_rounded_clicks
ips_per_user_group['ip_address'] = ips_per_user_group['user'].apply(lambda x: x.split('_')[-1])
ips_per_user_group['user'] = ips_per_user_group['user'].apply(lambda x: x.split('_')[:-1])
ips_per_user_group['user'] = ips_per_user_group['user'].apply(lambda x: '_'.join(x) + '_')

#ips_per_user_group['user'] = ips_per_user_group['user'].apply(lambda x: clean_ips(x))

ips_per_user_group = translate_user_names(ips_per_user_group)

ip_per_user_group = ips_per_user_group.groupby('user')['ip_address'].nunique()

ip_per_user_group.to_csv('./unique_ips_per_group.csv')
print("ip_per_user_group", ip_per_user_group)