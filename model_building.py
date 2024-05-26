import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression, Lasso
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_absolute_error
import statistics
import joblib

df = pd.read_csv('/Users/tunakisaaga/Desktop/ds_salary_proj-master/eda_data_old.csv')

df_model = df[
    ['avg_salary', 'Rating', 'Size', 'Type of ownership', 'Industry', 'Sector', 'Revenue', 'num_comp', 'hourly',
     'employer_provided',
     'job_state', 'same_state', 'age', 'python_yn', 'spark', 'aws', 'excel', 'job_simp', 'seniority', 'desc_len']]

# get dummy data 
df_dum = pd.get_dummies(df_model)

# train test split
X = df_dum.drop('avg_salary', axis=1)
y = df_dum.avg_salary.values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

X_test.to_csv('X_test.csv', index=False)

# multiple linear regression
X_sm = X = sm.add_constant(X)
model = sm.OLS(y, X_sm)
model.fit().summary()

lm = LinearRegression()
lm.fit(X_train, y_train)

np.mean(cross_val_score(lm, X_train, y_train, scoring='neg_mean_absolute_error', cv=3))

# lasso regression 
lm_l = Lasso(alpha=.13)
lm_l.fit(X_train, y_train)
np.mean(cross_val_score(lm_l, X_train, y_train, scoring='neg_mean_absolute_error', cv=3))

alpha = []
error = []

for i in range(1, 100):
    alpha.append(i / 100)
    lml = Lasso(alpha=(i / 100))
    error.append(np.mean(cross_val_score(lml, X_train, y_train, scoring='neg_mean_absolute_error', cv=3)))

plt.plot(alpha, error)

err = tuple(zip(alpha, error))
df_err = pd.DataFrame(err, columns=['alpha', 'error'])
df_err = df_err[df_err.error == max(df_err.error)]

# random forest 

rf = RandomForestRegressor()

np.mean(cross_val_score(rf, X_train, y_train, scoring='neg_mean_absolute_error', cv=3))

# tune models GridsearchCV

parameters = {'n_estimators': range(10, 300, 10), 'criterion': ('friedman_mse', 'absolute_error'), 'max_features': ('sqrt', 'log2')}

gs = GridSearchCV(rf, parameters, scoring='neg_mean_absolute_error', cv=3)
gs.fit(X_train, y_train)

best_score = gs.best_score_
best_estimator = gs.best_estimator_

# test ensembles 
tpred_lm = lm.predict(X_test)
tpred_lml = lm_l.predict(X_test)
tpred_rf = gs.best_estimator_.predict(X_test)

tpred_lm_err = mean_absolute_error(y_test, tpred_lm)
tpred_lml_err = mean_absolute_error(y_test, tpred_lml)
tpred_rf_err = mean_absolute_error(y_test, tpred_rf)
tpred_lm_rf_err = mean_absolute_error(y_test, (tpred_lm + tpred_rf) / 2)

print("mse lm: " + str(tpred_lm_err))
print("mse lml: " + str(tpred_lml_err))
print("mse rf: " + str(tpred_rf_err))
print("mse lm+rf: " + str(tpred_lm_rf_err))
print("\n")
print("lm: " + str(statistics.mean(tpred_lm)))
print("lml: " + str(statistics.mean(tpred_lml)))
print("rf: " + str(statistics.mean(tpred_rf)))

# Sample DataFrame
data = {
    'lm': tpred_lm,
    'lml': tpred_lml,
    'rf': tpred_rf,
    'y-real': y_test
}
df_final = pd.DataFrame(data)

df_final.to_csv('final_results.csv', index=False)

joblib.dump(gs, "./random_forest.joblib")
