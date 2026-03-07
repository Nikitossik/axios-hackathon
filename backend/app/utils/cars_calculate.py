import pandas as pd
import numpy as np

def oblicz_liczbe_samochodow_krakow(row):
   
    hour = int(row['time'])
    
    day = int(row['day'])
    is_off = int(row['off']) in ['tak', 'true', '1']
    is_weekend = day >= 5
    is_holiday = is_off or is_weekend
    
    is_oneway = str(row['Oneway']).strip().lower() in ['tak', 'true', '1', 'yes', True]
    lanes = int(row['Lanes']) if pd.notna(row['Lanes']) else 2
    length = float(row['Length'])/1000
    maxspeed = float(row['maxspeed']) if pd.notna(row['maxspeed']) else 50.0
    
    psr = 'C' 
    if is_holiday:
        if hour >= 22 or hour < 7:
            psr = 'A' 
        elif 7 <= hour < 11 or 19 <= hour < 22:
            psr = 'B' 
        elif 11 <= hour < 14:
            psr = 'C' 
        elif 14 <= hour < 19:
            psr = 'D' 
    else:
        if hour >= 21 or hour < 6:
            psr = 'A' # Noc
        elif 6 <= hour < 7 or 18 <= hour < 21:
            psr = 'D'
        elif 9 <= hour < 14:
            psr = 'E'
        elif (7 <= hour < 9) or (14 <= hour < 18):
            psr = 'F'
            
    use_table_1 = is_oneway or (not is_oneway and lanes >= 3)
    
    k = 0.0
    if use_table_1:
        if psr == 'A': k = 3.5     
        elif psr == 'B': k = 9.0   
        elif psr == 'C': k = 13.5  
        elif psr == 'D': k = 19.0  
        elif psr == 'E':
            if maxspeed >= 100: k = 24.5    
            elif maxspeed >= 90: k = 25.5   
            elif maxspeed >= 80: k = 26.5   
            else: k = 27.5                  
        else:
            k = 30.0 
    else:
        if psr == 'A': k = 2.5     
        elif psr == 'B': k = 7.5   
        elif psr == 'C': k = 12.5  
        elif psr == 'D': k = 17.5  
        elif psr == 'E': k = 22.5  
        else:
            k = 30.0 
            
    
    N = k * length * lanes
        
    if row['strefa'] == 0:
        
        return round(N * 2)
    elif row['strefa'] == 1:
        return round(N * 1.8)
    elif row['strefa'] == 2:
        return round(N * 1.7)
    elif row['strefa'] == 3:
        return round(N * 1.5)
    else:
        return round(N * 1.3)
