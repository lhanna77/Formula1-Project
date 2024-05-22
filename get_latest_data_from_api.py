from lib.common_functions import call_api, add_header_to_excel
import pandas as pd

def api_call(url):

    response_dict = call_api(url)

    response_count = response_dict['MRData']['total']
    print(f'{url} - {response_count}')

    #response_list = response_dict['MRData']['DriverTable']['Drivers']

api_call('http://ergast.com/api/f1/drivers')
api_call('http://ergast.com/api/f1/constructors')
api_call('http://ergast.com/api/f1/circuits')
api_call('http://ergast.com/api/f1/races')
api_call('http://ergast.com/api/f1/results')

def get_json_from_api(target_data = 'Drivers', file_type = 'json'):
    
    target_data_lower = target_data.lower()
    target_data_singular = target_data[:-1]

    response_dict = call_api(f'http://ergast.com/api/f1/{target_data_lower}')
    response_list = response_dict['MRData'][f'{target_data_singular}Table'][f'{target_data}']

    output_file = f'files/latest_data_from_api/{target_data_lower}.{file_type}'
    all_rows_df = pd.DataFrame()
    i=1

    if file_type == 'json':

        with open(output_file, 'w', encoding='utf-8') as file:

            for rl in response_list:

                if target_data == 'Drivers':

                    file.write(str({"driverId":i,"driverRef":rl["driverId"],"number":"999","code":"CODE","name":{"forename":rl["givenName"],"surname":rl["familyName"]},"dob":rl["dateOfBirth"],"nationality":rl["nationality"],"url":rl["url"]}).replace("'",'"'))
                    file.write('\n')

                    #print(str({"driverId":i,"driverRef":rl["driverId"],"number":"999","code":"CODE","name":{"forename":rl["givenName"],"surname":rl["familyName"]},"dob":rl["dateOfBirth"],"nationality":rl["nationality"],"url":rl["url"]}).replace("'",'"'))

                elif target_data == 'Constructors':
                    
                    file.write(str({"constructorId":i,"constructorRef":rl["constructorId"],"name":rl["name"],"nationality":rl["nationality"],"url":rl["url"]}).replace("'",'"'))
                    file.write('\n')

                    #print(str({"constructorId":i,"constructorRef":rl["constructorId"],"name":rl["name"],"nationality":rl["nationality"],"url":rl["url"]}).replace("'",'"'))

                i+=1
                
    elif file_type == 'csv':
        
        for rl in response_list:
            
            if target_data == 'Circuits':

                df_new_row = pd.DataFrame({"circuitId": i,"circuitRef": rl["circuitId"],"name": rl["circuitName"],"location": rl["Location"]["locality"],"country": rl["Location"]["country"],"lat": rl["Location"]["lat"],"lng": rl["Location"]["long"],"alt": "alt","url": rl["url"]}, index=[0])
                all_rows_df = pd.concat([all_rows_df,df_new_row], ignore_index=True)
                
            i+=1
    
    print(f'File - {output_file} populated from API')        
    return output_file,all_rows_df

#get_json_from_api('Drivers','json')
#get_json_from_api('Constructors','json')

output_file,all_rows_df = get_json_from_api('Circuits','csv')
all_rows_df.to_csv(output_file, index=False)





