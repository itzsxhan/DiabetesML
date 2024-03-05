import keras_tuner
import keras
import numpy as np
import pandas as pd
from keras.src.applications.densenet import layers
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, classification_report
from sklearn.model_selection import train_test_split
from keras import metrics
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB

dataset = pd.read_csv('diabetes_binary_health_indicators_BRFSS2015.csv')

df = dataset.copy()

# Set all columns except for "BMI" to int type
columns_to_convert = df.columns.difference(['BMI'])
df[columns_to_convert] = df[columns_to_convert].astype(int)

# Proportion of target classes
print("Proportion of Target Classes (Overall dataset):")
print(df['Diabetes_binary'].value_counts(normalize=True),"\n")

#Checking for duplicated rows
print("Duplicate rows:", df.duplicated().sum())

duplicates_df = df[df.duplicated()]
duplicates_df['Diabetes_binary'].value_counts()

df.drop_duplicates(inplace = True)

# Separate target variable & features
X = df.drop(columns = 'Diabetes_binary')
y = df['Diabetes_binary']

print(X.shape, y.shape)



X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=88, stratify = y)

print(X_train.shape, X_test.shape, y_train.shape, y_test.shape)


class MyHyperModel(keras_tuner.HyperModel):

# Tune the architecture of the neural network
    def build(self, hp):
        model = keras.Sequential()

        # Tune first hidden layer
        model.add(
            layers.Dense(
                # Tune number of neuron units
                units=hp.Int("units1", min_value=16, max_value=64, step=8),
                # Tune the activation function to use.
                activation=hp.Choice("activation1", ["relu", "tanh", "softplus"]),
                input_shape=(21,)
            )
        )

        # Decide whether to use 2nd hidden layer
        if hp.Boolean("hidden2"):
            model.add(
                layers.Dense(
                    # If 2nd hidden layer is used, tune number of units & activation function to use
                    units=hp.Int("units2", min_value=16, max_value=64, step=8),
                    activation=hp.Choice("activation2", ["relu", "tanh", "softplus"])
                    )
                )

        # Output layer
        model.add(
            layers.Dense(1, name="output",activation="sigmoid"))

        model.compile(
            optimizer=hp.Choice("optimizer", ["rmsprop","adam","adamax"]),
            loss="binary_crossentropy",
            metrics=["accuracy","AUC"]
        )
        return model

# Tune the training parameters of the neural network
    def fit(self, hp, model, *args, **kwargs):
        return model.fit(
            *args,
            # Tune batch size
            batch_size=hp.Choice("batch_size", [32, 64, 128]),
            **kwargs,
        )

MyHyperModel(keras_tuner.HyperParameters())

tuner = keras_tuner.RandomSearch(
    MyHyperModel(),
    objective=keras_tuner.Objective("val_auc", direction="max"),
    max_trials=15,
    overwrite=True,
    directory="my_dir",
    project_name="DBA5106_Bonus2",
)

tuner.search_space_summary()

# Model the NN architecture based on the results of the best combination from KerasTuner

# Define Sequential model
model = keras.models.Sequential()

# 1st hidden dense layer
model.add(keras.layers.Dense(56, name="hidden1", input_shape=(21,), activation="softplus"))

# # 2nd hidden dense layer
# model.add(keras.layers.Dense(48, name="hidden2", activation="tanh"))

# Define output dense layer (Binary classification)
model.add(keras.layers.Dense(1, name="output", activation="sigmoid"))

# print summary of model
model.summary()

# Compile the model
model.compile(loss="binary_crossentropy", optimizer="adamax", metrics=[metrics.AUC(curve="ROC", name="auc-roc"),
metrics.TruePositives(name="TP"),    # True Positives
metrics.TrueNegatives(name="TN"),    # True Negatives
metrics.FalsePositives(name="FP"),   # False Positives
metrics.FalseNegatives(name="FN")    # False Negatives
])

# Train the model
history = model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_test, y_test))

def round_class_prediction(prediction):
  if prediction <= 0.18:
    return 0
  else:
    return 1


# Define function to evaluate Neural Network model & display confusion matrix
def evaluate_model_NN(model, X_test, y_test):

    # Evaluate the model - display validation loss, accuracy & AUC
    model.evaluate(X_test, y_test)

    # Predict the class labels, then round off to a value of 0 or 1
    Y_test_pred = model.predict(X_test, verbose=0)
    Y_test_pred_rounded = np.vectorize(round_class_prediction)(Y_test_pred)

    # Draw the Confusion matrix
    cm = confusion_matrix(y_test, Y_test_pred_rounded)
    disp = ConfusionMatrixDisplay(cm)

    print("\n")
    print(classification_report(y_test, Y_test_pred_rounded), "\n")

    return disp.plot()

# Evaluate the model & plot the confusion matrix
evaluate_model_NN(model, X_test, y_test)

'''
knn : 
#nc=KNeighborsClassifier(n_neighbors=5).fit(x_train,y_train)
nc=KNeighborsClassifier(16).fit(x_train_p_smote, y_train_p_smote)
scores=get_performance_scores(nc,x_test,y_test)
print("Neighbors Classifier")
print(scores)

gbn=GaussianNB().fit(x_train,y_train)
scores=get_performance_scores(gbn,x_test,y_test)
print("guassianGB")
print(scores)
'''