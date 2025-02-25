import pandas as pd
import os
from lib.common_functions import call_api, write_api_results_to_json, get_max_result_id
from lib import configuration

def api_call(url):

    response_dict = call_api(url)

    response_count = response_dict['MRData']['total']
    print(f'{url} - {response_count}')

    return response_count

def create_latest_folder(round_season):
    
    latest_folder = f'{configuration.bronze_folder_path}/results/inc/{round_season}'
    
    os.makedirs(latest_folder, exist_ok=True)
    
    return latest_folder
        
def main(latest, season, round):
    
    all_rows_df = pd.DataFrame()
    i_res=get_max_result_id()
    
    if latest == False:
        response_dict = call_api(f'https://ergast.com/api/f1/{season}/{round}/results')
    else:
        response_dict = call_api('http://ergast.com/api/f1/current/last/results')
        
    response_list = response_dict['MRData'][f'RaceTable']['Races']

    season = response_list[0]["season"]
    round = response_list[0]["round"]
    
    if len(round) == 1:
        round = "0"+round
    
    round_season = int(season+round)
    latest_folder = create_latest_folder(round_season)
    output_file = f'{latest_folder}/{round_season}.json'

    for rl in response_list:
        for res in rl['Results']:

            df_new_row = pd.DataFrame({"resultId":round_season,"raceId_join":rl["raceName"]+rl["season"],"driverId_join":res["Driver"]["driverId"],"constructorId_join":res["Constructor"]["constructorId"],"number":res["number"],"grid":res["grid"],"position":res["position"],"positionText":res["positionText"],"positionOrder":"positionOrder","points":res["points"],"laps":res["laps"],"statusId":res["status"]}, index=[0])
            all_rows_df = pd.concat([all_rows_df,df_new_row], ignore_index=True)
                        
            i_res+=1
            
    write_api_results_to_json('json',output_file,all_rows_df)

if __name__ == '__main__':
    main(latest=False,season=2024,round=25)
    
    # for i in range(14):
    #     main(latest=False,season=2024,round=i+1)