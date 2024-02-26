# -*- coding: utf-8 -*-
"""194083U_CourseWork

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1TeyQnc_MejctgMbxcwEmvsx94uhiPw6s

To predict temperature using Python for the New York Stock Exchange dataset:
"""

from google.colab import drive
drive.mount("/content/gdrive")

import pandas as pd

df = pd.read_csv('/content/gdrive/My Drive/ML_Datasets/weatherHistory.csv')

# Identify missing values
missing_values = df.isna().sum()

# Impute missing values with the mean
df = df.fillna(df.mean(numeric_only=True))

df

df.info()

df.describe()

df.rename(columns={'Temperature (C)': 'Temperature',
                   'Apparent Temperature (C)': 'Apparent_Temperature',
                   'Humidity': 'Humidity',
                   'Wind Speed (km/h)': 'Wind_Speed',
                   'Wind Bearing (degrees)': 'Wind_Bearing',
                   'Visibility (km)': 'Visibility',
                   'Pressure (millibars)': 'Pressure'}, inplace=True)

"""## (a) Preprocessing

**I. Handle Missing Values and Outliers**

We can use the following steps to handle missing values and outliers:

1. **Identify missing values:** We can use the `isna()` function to identify missing values in the dataset.
2. **Remove missing values:**
"""

null_counts = {}
for col in df.columns:
    count = df[col].isnull().sum()
    if count > 0:
        null_counts[col] = count

if not null_counts:
    print("No null values in any column.")
else:
    for col, count in null_counts.items():
        print(f"Column '{col}' has {count} null values.")

"""number of null values are 517 and number of data entry is 95936. so we can remove null values"""

df.dropna(inplace = True)

"""**remove duplicate values**"""

print(df.duplicated().value_counts())

df.drop_duplicates(inplace=True)

print(df.duplicated().value_counts())

df = df.drop(["Formatted Date","Summary","Precip Type","Loud Cover","Daily Summary"],axis=1)

df.head()

df_copy = df.copy()
df_copy.head()

"""3. **Identify outliers:** We can use different methods to identify outliers, such as boxplots, interquartile range (IQR), or z-scores. For example, we can use the following code to identify outliers using boxplots:"""

import seaborn as sns

X_cols = ["Apparent_Temperature","Humidity","Wind_Speed","Wind_Bearing","Visibility","Pressure"]
y_cols = ["Temperature"]
sns.pairplot(df,x_vars= X_cols,y_vars= y_cols);

df.hist(linewidth=1.2, figsize=(20,20));

"""**Box Plots**"""

import matplotlib.pyplot as plt
import seaborn as sns

fig = plt.figure(figsize=(18, 12))
columns_to_plot = ["Temperature", "Apparent_Temperature", "Humidity", "Wind_Speed", "Wind_Bearing", "Visibility", "Pressure"]

for i, column in enumerate(columns_to_plot):
    plt.subplot(3, 3, i + 1)
    sns.boxplot(df_copy[column], color='skyblue')
    plt.xlabel(column, fontsize=12)
    plt.title(f"{column} counts", fontsize=16)

# Adjust vertical spacing (reduce the value of hspace)
plt.subplots_adjust(top=0.99, bottom=0.01, hspace=0.3, wspace=0.2)

plt.show()

q1 = df.quantile(0.25)
q3 = df.quantile(0.75)
iqr = q3 - q1
outliers = df.loc[((df < (q1 - 1.5 * iqr)) | (df > (q3 + 1.5 * iqr))).any(axis=1)]

# Remove outliers
df = df.drop(outliers.index)

# Checking the outliers in Pressure column
fig = plt.figure(figsize=(18,6))

sns.boxplot(df["Pressure"], color='tan')
plt.title('Box Plot: Pressure', fontsize=15)
plt.xlabel('Pressure', fontsize=14)

plt.show()

# Calculate quartiles and interquartile range (IQR) for the 'Pressure' column
Q1_Pressure, Q3_Pressure = df["Pressure"].quantile([0.25, 0.75])
IQR_Pressure = Q3_Pressure - Q1_Pressure

# Calculate lower and upper limits based on quantiles
lower_limit_Pressure, upper_limit_Pressure = df["Pressure"].quantile([0.05, 0.95])

# Print the results
print("Quartiles (Q1, Q3) for Pressure: {:.4f}, {:.4f}".format(Q1_Pressure, Q3_Pressure))
print("IQR for Pressure: {:.4f}".format(IQR_Pressure))
print("Lower limit for Pressure: {:.4f}".format(lower_limit_Pressure))
print("Upper limit for Pressure: {:.4f}".format(upper_limit_Pressure))

import matplotlib.pyplot as plt
import seaborn as sns

fig, axes = plt.subplots(1, 2, figsize=(15, 3))

# Replace outliers in df_copy['Pressure']
df_copy['Pressure'] = df_copy['Pressure'].clip(lower=lower_limit_Pressure, upper=upper_limit_Pressure)

# Create box plots
sns.boxplot(df['Pressure'], color='slateblue', ax=axes[0])
axes[0].set_title('Box Plot: Pressure (with outliers)', fontsize=15)
axes[0].set_xlabel('Pressure', fontsize=14)

sns.boxplot(df_copy['Pressure'], color='blue', ax=axes[1])
axes[1].set_title('Box Plot: Pressure (After outliers replaced)', fontsize=15)
axes[1].set_xlabel('Pressure', fontsize=14)

plt.subplots_adjust(top=0.99, bottom=0.01, hspace=0.5, wspace=0.3)
plt.show()

"""Pressure is unwanted outlier other feature may be relate to dataset

**2. Produce Q-Q Plots and Histograms**

We can produce Q-Q plots and histograms to visualize the distribution of the features. This can help us to identify any non-normality in the data and to select the appropriate transformations.

To produce a Q-Q plot, we can use the following code:
"""

# calculating the skewness of each columns in dataset

skew = df_out.skew()
print("-------- Skewness --------")
for i in range(len(skew)):
  print("{} : {:.4f}".format(df.columns[i], skew[i]))

# Visualizing histogram and Q-Q plot before transformation
import scipy.stats as stats

plt.figure(figsize=(22, 10))

for i in list(enumerate(df_copy.columns)):
    plt.subplot(2, 7, i[0] + 1)
    sns.histplot(data = df_copy[i[1]], kde=True)  # Histogram with KDE line

for i in list(enumerate(df_copy.columns)):
    plt.subplot(2, 7,i[0] + 8)
    stats.probplot(df_copy[i[1]], dist="norm", plot=plt)   # QQ Plot
    plt.title("")

plt.tight_layout()
plt.show()

"""Continuous values are seen in data columns. When training a machine learning model, taking into account the normal distribution of the continuous data has many benefits. Using the Quartile — Quartile plot (QQ plot), we may determine whether continuous data is skewed normally.

  In the diagram above, the first row displays a histogram with a KDE line, while the second row displays a QQ plot for each of the dataset's feature columns.

**3. If it is required, apply suitable feature coding techniques.**

We don't need to use feature coding methods like label encoding or one hot encoding because our dataset simply has numerical columns (no category ones).

**4. Scale and/or standardized the features, produce relevant graphs to show the
scaling/ standardizing effect.**

If the dataset contains categorical features, we need to encode them before applying the regression models. This can be done using different techniques, such as one-hot encoding or label encoding.

For example, to one-hot encode a categorical feature, we can use the following code:
"""

# Scale the features
from sklearn.preprocessing import StandardScaler, LabelEncoder

scaler = StandardScaler()
scaled_df = scaler.fit_transform(df)

# Produce a graph to show the scaling effect
plt.figure(figsize=(10, 6))
plt.subplot(121)
plt.hist(df['Temperature'])
plt.title('Original Temperature')

plt.subplot(122)
plt.hist(scaled_df[:, 0])
plt.title('Scaled Temperature')

plt.show()

import pandas as pd

# df = pd.get_categorical(df, columns=['Humidity'])
df = pd.get_dummies(df, columns=['Humidity'])

numeric_columns = df.select_dtypes(include=['int64', 'float64'])

"""**V. Scale and/or Standardize the Features**

Scaling and/or standardizing the features can improve the performance of the regression models. This is because it ensures that all features are on the same scale and have the same variance.

To scale the features, we can use the following code:
"""

df.to_csv('preprocessed_nyse_dataset.csv', index=False)

"""## (b) Feature Engineering

**I. Apply PCA or SVD for Feature Reduction**

PCA and SVD can be used to reduce the dimensionality of the data while preserving
"""

import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# Standardize the data
scaler = StandardScaler()
X_std = scaler.fit_transform(df)  # Standardize all numeric features

# Specify the number of components to retain (choose based on explained variance)
n_components = 5  # Example: Retaining 5 principal components

# Apply PCA
pca = PCA(n_components=n_components)
X_pca = pca.fit_transform(X_std)

# Examine the explained variance
explained_variance = pca.explained_variance_ratio_
print("Explained Variance Ratios for Principal Components:")
for i, ev in enumerate(explained_variance):
    print(f"PC{i + 1}: {ev:.4f}")

# Evaluate the impact of dimensionality reduction on your task
# You can now use X_pca for downstream analysis, such as modeling or visualization

""" **2. Identify significant and independent features using appropriate techniques.
Show how you selected the features using suitable graphs**
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

# Compute the correlation matrix
corr_matrix = df.corr()

# Create a heatmap to visualize feature correlations
plt.figure(figsize=(12, 8))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
plt.title('Feature Correlation Heatmap')
plt.show()

# Feature Importance with Machine Learning Models
# Separate the target variable (replace 'Temperature' with your target variable)
y = df['Temperature']  # Assuming 'Temperature' is a continuous target
X = df.drop('Temperature', axis=1)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Fit a Random Forest Regressor model
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# Get feature importances
feature_importances = rf_model.feature_importances_

# Create a bar chart to visualize feature importances
plt.figure(figsize=(12, 6))
sns.barplot(x=feature_importances, y=X.columns)
plt.title('Feature Importances')
plt.show()

"""##(c)  Cross Validation

Apply the following techniques to predict the value of Y for the test dataset (K =10)
"""

import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_predict
from sklearn.linear_model import LinearRegression, LassoCV, RidgeCV
from sklearn.preprocessing import StandardScaler

# Separate the target variable (replace 'Temperature' with your target variable)
y = df['Temperature']
X = df.drop('Temperature', axis=1)

# Step 1: Split the Data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 2: Preprocess the Data
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

"""1. Linear Regression  with Cross Validation"""

linear_regression = LinearRegression()
y_pred_linear = cross_val_predict(linear_regression, X_train_scaled, y_train, cv=10)  # 10-fold cross-validation
linear_regression.fit(X_train_scaled, y_train)  # Final fit
y_pred_test_linear = linear_regression.predict(X_test_scaled)

"""2. Lasso Regression with Cross Validation"""

lasso_regression = LassoCV(alphas=[0.001, 0.01, 0.1, 1.0, 10.0], cv=10)  # Specify alpha values and use 10-fold cross-validation
y_pred_lasso = cross_val_predict(lasso_regression, X_train_scaled, y_train, cv=10)
lasso_regression.fit(X_train_scaled, y_train)
y_pred_test_lasso = lasso_regression.predict(X_test_scaled)

"""3. Ridge Regression with Cross Validation"""

ridge_regression = RidgeCV(alphas=[0.001, 0.01, 0.1, 1.0, 10.0], cv=10)  # Specify alpha values and use 10-fold cross-validation
y_pred_ridge = cross_val_predict(ridge_regression, X_train_scaled, y_train, cv=10)
ridge_regression.fit(X_train_scaled, y_train)
y_pred_test_ridge = ridge_regression.predict(X_test_scaled)

from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Calculate evaluation metrics for Linear Regression
mae_linear = mean_absolute_error(y_test, y_pred_test_linear)
mse_linear = mean_squared_error(y_test, y_pred_test_linear)
rmse_linear = mean_squared_error(y_test, y_pred_test_linear, squared=False)  # Calculate RMSE
r2_linear = r2_score(y_test, y_pred_test_linear)

# Calculate evaluation metrics for Lasso Regression
mae_lasso = mean_absolute_error(y_test, y_pred_test_lasso)
mse_lasso = mean_squared_error(y_test, y_pred_test_lasso)
rmse_lasso = mean_squared_error(y_test, y_pred_test_lasso, squared=False)  # Calculate RMSE
r2_lasso = r2_score(y_test, y_pred_test_lasso)

# Calculate evaluation metrics for Ridge Regression
mae_ridge = mean_absolute_error(y_test, y_pred_test_ridge)
mse_ridge = mean_squared_error(y_test, y_pred_test_ridge)
rmse_ridge = mean_squared_error(y_test, y_pred_test_ridge, squared=False)  # Calculate RMSE
r2_ridge = r2_score(y_test, y_pred_test_ridge)

# Print and compare the evaluation metrics
print("Linear Regression:")
print("MAE: ", mae_linear)
print("MSE: ", mse_linear)
print("RMSE: ", rmse_linear)
print("R-squared: ", r2_linear)

print("\nLasso Regression:")
print("MAE: ", mae_lasso)
print("MSE: ", mse_lasso)
print("RMSE: ", rmse_lasso)
print("R-squared: ", r2_lasso)

print("\nRidge Regression:")
print("MAE: ", mae_ridge)
print("MSE: ", mse_ridge)
print("RMSE: ", rmse_ridge)
print("R-squared: ", r2_ridge)