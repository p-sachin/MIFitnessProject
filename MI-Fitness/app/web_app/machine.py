from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import numpy as np
from joblib import load
from lightgbm import LGBMClassifier
from ast import literal_eval

def csv_create(filepath):
    cols = ['timestamp','bus','car','still','train','walking','diet recommendation',
    'calories','action recommendation']

    df = pd.DataFrame(columns = cols)
    df.to_csv(filepath,index=False)

class Recommendation:
    #initialization, gets current user, input file path and frequency of observations(frequency = 1/T)
    def __init__(self,user,input_path,frequency):
        self.weight = user.info.weight
        self.height = user.info.height
        self.bmi = user.info.bmi
        self.age = user.info.age
        self.gender = user.info.gender
        self.input_path = input_path
        self.frequency = frequency
    
    # getting the data, predict target and return
    def __predict(self):
        """loads trained model. Predicts, 
        return -> {'unique values': their count }"""

        #loads the saved trained model
        model = load('web_app/static/uploads/model_new.joblib')
        X_test = pd.read_csv(self.input_path)
        #gets predictions
        predict = model.predict(X_test)
        #gets unique valus and its count
        unique, counts = np.unique(predict,return_counts=True)
        vals = unique.tolist()
        cs = counts.tolist()
        #transform array to the dictionary unique vals -> key , their count -> value
        result = {val:c for val,c in zip(vals,cs) }
        return result
    # ratio calculator for 
    def __ratios(self,list_of_numbers,x):
        """takes list of numbers and desired member of that list,
        and returns -> member/(sum of all members)"""

        total = sum(list_of_numbers)
        print(total,x)
        if total != 0:
            r = x/total
        
            print(r)
        else:
            r=0
        return r

    def __counter(self,pred_dict):
        """
        takes dictionary of predictions, if particular class is missing, makes it 0,
        returns -> modified list, where None is imputed with 0

        """
        if 'Bus' in pred_dict.keys():
            b = pred_dict['Bus']
        else:
            b = 0
        if 'Walking' in pred_dict.keys():
            w = pred_dict['Walking']
        else:
            w = 0
        if 'Still' in pred_dict.keys():
            s = pred_dict['Still']
        else:
            s = 0
        if 'Train' in pred_dict.keys():
            t = pred_dict['Train']
        else:
            t = 0
        if 'Car' in pred_dict.keys():
            c = pred_dict['Car']
        else:
            c = 0
        result = [b,w,s,t,c]
        return result

    def __counts_to_minutes(self):
        """
        takes numbers of actions, returns -> values converted into minutes
        """
        pred_dict = self.__predict()
        T = 1/self.frequency
        l = self.__counter(pred_dict)
        b,w,s,t,c = l
        result = [(b*T)//60,(c*T)//60,(s*T)//60,(t*T)//60,(w*T)//60]
        return result
    
    def __bmr_calc(self):
        """
        bmr calculator.(bmr - basal metabolic rate)
        Men: BMR = 88.362 + (13.397 x weight in kg) + (4.799 x height in cm) – (5.677 x age in years)
        Women: BMR = 447.593 + (9.247 x weight in kg) + (3.098 x height in cm) – (4.330 x age in years)
        returns the value.
        """
        if self.gender=='F':
            bmr =  4475.593 + (9.247 * self.weight ) + (3.098 * self.height ) - (4.330 * self.age)
        elif self.gender =='M':
            bmr = 88.362 + (13.397 * self.weight) + (4.799 * self.height) - (5.677 * self.age)
        return bmr

    def __daily_calories(self):

        """
        daily calories calc
        amr (active metabolic rate) = daily calories consumption
        Sedentary : your AMR = BMR x 1.2
        Lightly active : your AMR = BMR x 1.375
        Moderately active: your AMR = BMR x 1.55
        Very active : your AMR = BMR x 1.725
        
        returns -> calories
        """

        bmr_res = self.__bmr_calc()
        list = self.__counts_to_minutes()
        walking = list[-1]
        #calculates walking ratios
        walks = self.__ratios(list,walking)
        if walks < 0.1:
            calories = int(bmr_res * 1.2)
        elif walks >= 0.1 and walks<0.3:
            calories = bmr_res * 1.375
        elif walks >= 0.3 and walks<0.5:
            calories = int(bmr_res*1.55)
        else:
            calories = int(bmr_res*1.725)
        
        return calories
    
    #takes daily delta calories
    def __recommend_diet(self,daily_delta_cal):
        max = 24.9
        min = 18.5
        bmi = self.bmi
        surplus = 'calorie surplus'
        deficit = 'calorie deficit'
        #equivalent calories to 1 kg of fat
        fat = 7700
        diet = []
        h = self.height/100
        if bmi>max or bmi<min:
            if bmi<min:
                delta = bmi - min
            if bmi>max:
                delta = bmi - max
            delta_cal = round(fat * delta * h ** 2,-2)
            days = abs(delta_cal//daily_delta_cal)
            if delta_cal<0:
                diet.append(surplus)
                diet.append(days)
            elif delta_cal>0:
                diet.append(deficit)
                diet.append(days)
        return diet

    def __act_recommend(self,still_ratio,walk_ratio,transport_ratio):
        still_rec = None
        walk_rec = None
        transport_rec = None
        act_rec = []
        still_rec_text = '''It seems, your spending your time physically passive. 
        Take a walk, run, do some exercises.It really helps to maintain you blood 
        circulation at healthy state.'''
        
        walk_rec_text = """Wow! You are too active. Give some rest to your legs. 
        It seems you are speending your time more active. It can cause some calorie deficits. Resting 
        or calorie-surplus on your diet would help."""

        transport_rec_text = """You are spending your more on transport. Step outside, breathe some 
        fresh air, avoid spending too much time in closed area.(in the crowd)"""

        #if person has less bmi than normal
        bmi = self.bmi
        if bmi<18.5:
            if still_ratio>0.5:
                still_rec = still_rec_text
            if walk_ratio>0.6:
                walk_rec = walk_rec_text
            if transport_ratio>0.5 and walk_ratio<0.4:
                transport_rec = transport_rec_text

        #if person has normal bmi
        elif bmi>=18.5 and bmi<=24.9:
            if still_ratio>0.5:
                still_rec = still_rec_text
            if walk_ratio>0.5:
                walk_rec = walk_rec_text
            if transport_ratio>0.5 and walk_ratio<0.4:
                transport_rec = transport_rec_text
    
        #if has greater bmi than normal
        else:
            if still_ratio>0.3:
                still_rec = still_rec_text
            if walk_ratio>0.3:
                walk_rec = walk_rec_text
            if transport_ratio>0.4 and walk_ratio<0.4 :
                transport_rec = transport_rec_text

        if still_rec:
            act_rec.append(still_rec)
        if walk_rec:
            act_rec.append(walk_rec)
        if transport_rec:
            act_rec.append(transport_rec)

        return act_rec



    def __dict_of_recommendation(self,time):
        daily_calories = self.__daily_calories()
        preds = self.__predict()
        l = self.__counts_to_minutes()
        print(l)
        diet = self.__recommend_diet(500)
        b,c,s,t,w = l
        #transport duration
        transport = b+t+c
        tr_ratio = self.__ratios(l,transport)
        print(tr_ratio)
        #walk
        w_ratio = self.__ratios(l,w)
        #still
        s_ratio = self.__ratios(l,s)

        act_recomm = self.__act_recommend(s_ratio,w_ratio,tr_ratio)

        data = {
            'timestamp':time,
            'bus':b,
            'car':c,
            'still':s,
            'train':t,
            'walking':w,
            'diet recommendation':diet,
            'calories':int(daily_calories),
            'action recommendation':act_recomm
        }
        print(f'transport ratio:{tr_ratio}, walk:{w_ratio},still:{s_ratio}')
        return data

    def recommend(self,time,tracking_file_path):
        data = pd.DataFrame( [self.__dict_of_recommendation(time)] )
        data.to_csv(tracking_file_path,mode='a',header=False)

#access to tracking data
def get_tracks(tr_file):
    data = pd.read_csv(tr_file)
    time,bus,walking,still,train,car,diet,calories,act_rec = data.iloc[-1].tolist()

    #when one saves dataframe with cell list inside, and read again, those cell become string.
    #to contvert it again as list, literal_eval is used
    diets_rec = literal_eval(diet)
    durations=[bus,walking,still,train,car]
    action_rec = literal_eval(act_rec)
    return durations,calories,diets_rec,action_rec,time

def delta_time(tr_file):
    _,_,_,_,time  = get_tracks(tr_file)
    return time









    


    
    
        

    


    
