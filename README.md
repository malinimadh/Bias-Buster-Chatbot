# CHATBOT - BIAS BUSTER
A chatbot engineered to illuminate the nuances of media bias, offering users a panoramic view of political events. Distinct from conventional platforms, this chatbot harnesses the power of advanced data science 
techniques to sift through the vast online media ecosystem, distinguishing factual reports from opinion-laden articles. Our approach employs both classification and clustering techniques, aimed at equipping users
with the discernment necessary to navigate the complex media landscape. 


## RoBERTa

The choice to use RoBERTa, particularly its distilled version distilroberta-base, for the classification task likely stems from RoBERTa's robust performance across a wide range of NLP tasks and its efficiency in handling text data. 
RoBERTa is an optimized version of BERT, designed to improve BERT's language understanding capabilities by training on a larger dataset and with more extensive computational resources. The distilled version, while smaller and faster, 
aims to retain much of the original model's ability to understand and process language, making it an excellent choice for tasks requiring nuanced language understanding, such as distinguishing between biased and non-biased texts. 

The results from the Roberta.ipynb indicate that the fine-tuned distilroberta-base model achieved commendable performance on the validation set, with the following metrics: 

Loss: 0.4774, suggesting the average difference between the predicted values and the actual labels is relatively low, indicating good model performance. 

Accuracy: 82.95%, showing that the model correctly identified the label of nearly four out of every five texts it was presented with, a strong result especially considering the task's complexity and the dataset's imbalanced nature. 

F1 Score: 79.73%, which balances precision and recall, providing a more comprehensive measure of the model's performance than accuracy alone. This score is particularly important for imbalanced datasets, as it indicates the model's 
robustness in identifying both classes without significant bias towards the majority class. 

## Chatbot development

app.py, a Flask applica􀆟on serves as a backend for a chatbot API. It receives webhook requests from chatbot pla􀆞orm, processes the requests, and returns appropriate responses based on the defined logic.
Chatbot in this project was constructed utilizing the Google Dialogflow SDK. The bot is connected to the local system using ngrok via webhook integration in the dialogflow. 
The integration of the ML model with Dialogflow is facilitated through a Flask application deployed on the local systems, acting as the backend infrastructure, while associated resources are maintained in the local system. 
Upon receiving a POST request from Dialogflow—triggered by user queries that align with predefined intents—our Flask application undertakes the processing of these requests to formulate appropriate responses. These responses are subsequently relayed back to Dialogflow, which, in turn, forwards them to the user, completing the interaction loop. 

### Dialog Flow intent snapshots
![image](https://github.com/user-attachments/assets/2aedaf41-6037-4bad-8c07-2f0af07eec95)

![image](https://github.com/user-attachments/assets/f20bd0b7-4cdd-489f-9b2b-3e7b58253188)

### Chatbot screenshots
![image](https://github.com/user-attachments/assets/1171869f-f8a2-49d3-bf19-9c38370347f9)

![image](https://github.com/user-attachments/assets/99d8825a-abd3-4f99-ba3c-228ef625b42e)

![image](https://github.com/user-attachments/assets/33399e58-4362-4c58-a9b3-9ecb85715d2c)

![image](https://github.com/user-attachments/assets/a6ac6594-81c9-49b4-bb03-df45791161fc)
