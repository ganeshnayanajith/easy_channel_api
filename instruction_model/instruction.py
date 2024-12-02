# Importing libraries
import pandas as pd
from sklearn.model_selection import train_test_split
import ktrain
from ktrain import text

# Read the data from csv file
dataset = pd.read_csv('data\emergency_data.csv')

# Split data into features and labels
X = dataset.iloc[:, 0].values
y = dataset.iloc[:, 1].values

X
y

# Split data into training and testing features and labels
x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)

MODEL_NAME = 'distilbert-base-uncased'

# Define the transformer model
t = text.Transformer(MODEL_NAME, maxlen=500, class_names=y_train)

# Preprocessing training set
print('Preprocessing training set')
trn = t.preprocess_train(x_train, y_train)

# Preprocessing test set
print('Preprocessing test set')
val = t.preprocess_test(x_test, y_test)

print('Getting classifier')
model = t.get_classifier()

print('Defining ktrain learner')
learner = ktrain.get_learner(model, train_data=trn, val_data=val, batch_size=6)

learner.fit_onecycle(5e-5, 4)

learner.validate(class_names=t.get_classes())

learner.view_top_losses(n=1, preproc=t)

print(x_test[50])

# Getting the predicting model
print('Getting the predicting model')
predictor = ktrain.get_predictor(learner.model, preproc=t)

predictor.predict('Razor Cuts')

# predicted probability scores for each category
predictor.predict_proba('Razor Cuts')

predictor.get_classes()

predictor.explain('Razor Cuts')

# Save predictor model
predictor.save('instructions_predictor')

# Load predictor model
reloaded_predictor = ktrain.load_predictor('instructions_predictor')

reloaded_predictor.predict('Razor Cuts')

reloaded_predictor.predict('Dog Bite')

reloaded_predictor.predict('i have Dog Bite')
