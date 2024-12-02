# Importing libraries
import pandas as pd
from sklearn.model_selection import train_test_split
import ktrain
from ktrain import text

# Read the data from csv file
dataset = pd.read_csv('data\specialization_data.csv')

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

print('Fitting with learning rate')
learner.fit_onecycle(5e-5, 4)

print('Validating classes')
learner.validate(class_names=t.get_classes())

print('Viewing top lossess')
learner.view_top_losses(n=1, preproc=t)

print('Testing for 371 record')
print(x_test[371])

# Getting the predicting model
print('Getting the predicting model')
predictor = ktrain.get_predictor(learner.model, preproc=t)

predictor.predict('itching  nodal_skin_eruptions  dischromic _patches')

# predicted probability scores for each category
predictor.predict_proba('itching  nodal_skin_eruptions  dischromic _patches')

predictor.get_classes()

predictor.explain('itching  nodal_skin_eruptions  dischromic _patches')

# Save predictor model
predictor.save('specialization_predictor')

# Load predictor model
reloaded_predictor = ktrain.load_predictor('specialization_predictor')

reloaded_predictor.predict('itching  skin_rash  dischromic _patches')

reloaded_predictor.predict('continuous_sneezing  shivering  chills  watering_from_eyes')

reloaded_predictor.predict('i have itching and skin rash dischromic patches')
