from user_agents import parse
import pandas as pd

'''
ua_string = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
user_agent = parse(ua_string)
print(user_agent)  
'''
# Leggere il dataset
data = pd.read_csv('mydata.csv',)
df = pd.DataFrame()
df['UA'] = data['transaction.request.headers_map.user-agent'].copy().unique()

# Selezionare la colonna di interesse
df["browser"] = ""
df["osFamily"]=""
df["deviceFamily"]=""
df["brandFamily"]=""
df["bot"]=""

# Iterare per ogni riga del dataset
for index, value in df.iterrows():    
    user_agent = parse(df.at[index, "UA"])
    #print("useragent: "+str(user_agent))
    df.at[index,"browser"] = user_agent.browser.family
    df.at[index,"osFamily"]=user_agent.os.family
    df.at[index,"deviceFamily"]=user_agent.device.family
    df.at[index,"brandFamily"]=user_agent.device.brand
    df.at[index,"bot"]=user_agent.is_bot
    if df.at[index,"bot"] == True:
        #drop row
        df.drop(index, inplace=True)
print("ciao")
