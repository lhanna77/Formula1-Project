import pandas as pd
from lib.common_functions import call_api, write_api_results_to_json,remove_old_api_files,create_inc_results_folder

def api_call(url):

    response_dict = call_api(url)

    response_count = response_dict['MRData']['total']
    print(f'{url} - {response_count}')

    return response_count



def get_json_from_api(target_data, file_type, file_folder='files/latest_data_from_api', limit=1000, offset=0, counter_start=1):
    
    target_data_lower = target_data.lower()
    target_data_singular = target_data[:-1]
    
    if target_data == 'Results':
        target_data_singular = 'Race'
        target_data = 'Races'
        output_file = f'{file_folder}/{target_data_lower}_{offset}.{file_type}'
    else:
        output_file = f'{file_folder}/{target_data_lower}.{file_type}'

    response_dict = call_api(f'http://ergast.com/api/f1/{target_data_lower}', limit, offset)
    response_list = response_dict['MRData'][f'{target_data_singular}Table'][target_data]

    all_rows_df = pd.DataFrame()
    i=counter_start
    i_res=counter_start

    for rl in response_list:

        if target_data == 'Drivers':

            df_new_row = pd.DataFrame({"driverId":i,"driverRef":rl["driverId"],"number":"999","code":"CODE","name":rl["givenName"] +' '+rl["familyName"],"dob":rl["dateOfBirth"],"nationality":rl["nationality"],"url":rl["url"]}, index=[0])
            all_rows_df = pd.concat([all_rows_df,df_new_row], ignore_index=True)

        elif target_data == 'Constructors':
            
            df_new_row = pd.DataFrame({"constructorId":i,"constructorRef":rl["constructorId"],"name":rl["name"],"nationality":rl["nationality"],"url":rl["url"]}, index=[0])
            all_rows_df = pd.concat([all_rows_df,df_new_row], ignore_index=True)

        elif target_data_lower == 'results':
            
            season = rl["season"]
            round = rl["round"]
            
            if len(round) == 1:
                round = "0"+round
            
            round_season = int(season+round)
            
            for res in rl['Results']:
            
                df_new_row = pd.DataFrame({"resultId":round_season,"raceId_join":rl["raceName"]+rl["season"],"driverId_join":res["Driver"]["driverId"],"constructorId_join":res["Constructor"]["constructorId"],"number":res["number"],"grid":res["grid"],"position":res["position"],"positionText":res["positionText"],"positionOrder":"positionOrder","points":res["points"],"laps":res["laps"],"statusId":res["status"]}, index=[0])
                all_rows_df = pd.concat([all_rows_df,df_new_row], ignore_index=True)
                            
                i_res+=1

        elif target_data == 'Circuits':

            df_new_row = pd.DataFrame({"circuitId": i,"circuitRef": rl["circuitId"],"name": rl["circuitName"],"location": rl["Location"]["locality"],"country": rl["Location"]["country"],"lat": rl["Location"]["lat"],"lng": rl["Location"]["long"],"alt": "alt","url": rl["url"]}, index=[0])
            all_rows_df = pd.concat([all_rows_df,df_new_row], ignore_index=True)
            
        elif target_data == 'Races':

            df_new_row = pd.DataFrame({"raceId": i,"year": rl["season"],"round": rl["round"],"circuitId": rl["Circuit"]["circuitName"],"name": rl["raceName"],"date": rl["date"],"time": "06:00:00","url": rl["url"]}, index=[0])
            all_rows_df = pd.concat([all_rows_df,df_new_row], ignore_index=True)
            
        i+=1

    return output_file,all_rows_df

def main():

    remove_old_api_files()
    create_inc_results_folder()

    api_call('http://ergast.com/api/f1/drivers')
    api_call('http://ergast.com/api/f1/constructors')
    api_call('http://ergast.com/api/f1/circuits')
    api_call('http://ergast.com/api/f1/races')
    result_total = api_call('http://ergast.com/api/f1/results')
    
    output_file,all_rows_df = get_json_from_api('Drivers','json')
    write_api_results_to_json('json',output_file,all_rows_df)

    output_file,all_rows_df = get_json_from_api('Constructors','json')
    write_api_results_to_json('json',output_file,all_rows_df)

    output_file,all_rows_df = get_json_from_api('Circuits','csv')
    all_rows_df.to_csv(output_file, index=False)
    print(f'File - {output_file} populated from API') 

    output_file,all_rows_df = get_json_from_api('Races','csv')
    all_rows_df.to_csv('files/latest_data_from_api/races/races_0.csv', index=False)
    print(f'File - {output_file} populated from API') 

    output_file,all_rows_df = get_json_from_api('Races','csv',limit=250,offset=1000,counter_start=1001)
    all_rows_df.to_csv('files/latest_data_from_api/races/races_1000.csv', index=False)
    print(f'File - {output_file} populated from API') 

    output_file,all_rows_df = get_json_from_api('Results','json','files/latest_data_from_api/results')
    write_api_results_to_json('json',output_file,all_rows_df)

    loop_count = int((round(int(result_total),-3)+1000)/1000)
    i=1000

    for x in range(loop_count):
        output_file,all_rows_df = get_json_from_api('Results','json','files/latest_data_from_api/results',limit=1000,offset=i,counter_start=i+1)
        write_api_results_to_json('json',output_file,all_rows_df)
        print(f'File - {output_file} populated from API') 
        i+=1000
        
    return output_file,all_rows_df

    # target_data = 'Results'
    # file_type = 'json'
    # limit=1000
    # offset=0
    # counter_start=1

if __name__ == '__main__':
    
    output_file,all_rows_df = main()
