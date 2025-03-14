from flask import Flask, request, jsonify
import pandas as pd
import json
from collections import Counter
import random

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route('/webhook', methods=['POST'])
def predict_bias():

    req = request.get_json(silent=True, force=True)
    json_data = json.dumps(req)
    print(type(req))
    data_dict = json.loads(json_data)
    display_name = data_dict['queryResult']['intent']['displayName']
    df = pd.read_csv('./Clustering/champion/Dataset_with_LDA_embeddings_all_3_models.csv')

    if display_name == 'Topic Bias':
        df_predictions = pd.read_excel("./Classification/Prediction file_Roberta.xlsx")
        print(df_predictions.columns) 
        
        topic = data_dict['queryResult']['parameters']['Topics']
        outlet = data_dict['queryResult']['parameters']['Media_Outlet']

        prediction_row = df_predictions.loc[
                (df_predictions['outlet'].str.contains(outlet, case=False, na=False)) &
                (df_predictions['topic'].str.contains(topic, case=False, na=False))
            ]
        if not prediction_row.empty:
            bias = prediction_row['Label_bias'].iloc[0]
            response_text = f"The media outlet '{outlet}' is considered '{bias}' on the topic of '{topic}'."
        else:
            response_text = "I'm sorry, I don't have information on that topic and outlet combination."

        return jsonify({"fulfillmentText": response_text})

    elif display_name == 'Media Outlet Bias':
            df_predictions = pd.read_excel("C:/Users/DELL/Downloads/labeled_dataset_noagree.xlsx")
            print(df_predictions.columns) 
            topic = data_dict['queryResult']['parameters']['Topics']
            bias_check = data_dict['queryResult']['parameters']['Bias_check']

            outlet = data_dict['queryResult']['parameters']['Outlet']  

            prediction_row = df_predictions.loc[
                    (df_predictions['outlet'].str.contains(outlet, case=False, na=False)) &
                    (df_predictions['topic'].str.contains(topic, case=False, na=False))
                ]

            if not prediction_row.empty:
                media_outlet = prediction_row['outlet'].iloc[0]
                response_text = f"Media outlets that has '{bias_check}' articles on '{topic}' is '{media_outlet}'."
            else:
                response_text = "I'm sorry, I don't have information."

            return jsonify({"fulfillmentText": response_text})
    

    elif display_name == 'Political Ideology -':

        print(df['outlet'].unique()) 
        Media_Outlet = data_dict['queryResult']['parameters']['Media_Outlet']
        Topics = data_dict['queryResult']['parameters']['Topics']
        print(Topics)
        print(Media_Outlet)
        print(df.shape)
        print
        if Topics == "":
            required_df = df[(df['outlet'] == Media_Outlet)]
            print(required_df.shape)
            counter = Counter(required_df['type'].tolist())
            print(counter)
            ideology_type = counter.most_common(1)[0][0]
        else:
            required_df = df[(df['outlet'] == Media_Outlet)&(df['topic'] == Topics)]
            counter = Counter(required_df['type'].unique().tolist())
            print('else', counter)
            ideology_type = counter.most_common(1)[0][0]
        result = f"Certainly. I'm able to offer insight into the political stance {Media_Outlet} is categorized under the {ideology_type} political ideology."
    elif display_name == 'Article Recommendation - Political ideology':
        Political_alignment = data_dict['queryResult']['parameters']['Political_alignment']
        Topics = data_dict['queryResult']['parameters']['Topics']
        if Political_alignment:
            required_df = df[(df['type'] == Political_alignment)&(df['topic'] == Topics)]
            links = df['news_link'].tolist()
            random_media = random.sample(links, k=3)
            result = f" Here are some articles regarding {Political_alignment} opinion on {Topics}: {','.join(random_media)}"
        else:
            recommendations = {}
            required_df = df[df['topic'] == Topics]
            types = required_df['type'].unique().tolist()
            for each_type in types:
                type_df = required_df[required_df['type'] == each_type]
                links = df['news_link'].tolist()
                random_media = random.sample(links, k=3)
                recommendations[each_type] = random_media
            result = f"Here are some articles regarding {Topics}: {json.dumps(recommendations, indent=4)}"
    elif display_name == 'Ideology similarity':
        Media_Outlet = data_dict['queryResult']['parameters']['Media_Outlet']
        type_counts = df.groupby(['outlet', 'type']).size().reset_index(name='count')


        top_counts_by_media = {}


        for media in type_counts['outlet'].unique():

            media_counts = type_counts[type_counts['outlet'] == media]

            top_count = media_counts.loc[media_counts['count'].idxmax()]
            
 
            top_type = top_count['type']
            top_count_value = top_count['count']
            
 
            top_counts_by_media[media] = (top_type, top_count_value)
        ideology_type, _ = top_counts_by_media[Media_Outlet] 
        result_list = []
        for media, (top_type, _) in top_counts_by_media.items():

            if top_type == ideology_type:
           
                result_list.append(media)
        result_list.remove(Media_Outlet)
        result = f"Media outlets that have a similar ({ideology_type}) ideology to {Media_Outlet} : {', '.join(result_list)}"
    fulfillmentText = result
    return {'fulfillmentText':fulfillmentText}


if __name__ == '__main__':
    app.run(debug=True)
