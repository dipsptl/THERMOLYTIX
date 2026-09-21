#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
THERMOLYTIX - model evaluation script  (for interview preparation)
==================================================================
Put this file next to cooling_data.csv and run:

    python evaluate_model.py
    python evaluate_model.py path/to/cooling_data.csv

It answers the questions an AI interviewer will ask:
  1. What does the data look like?                    (rows, missing values, ranges, correlations)
  2. What did the model learn?                        (intercept, coefficients, relative importance)
  3. How accurate is it on data it has NOT seen?      (train/test split + 5-fold cross-validation)
  4. Is it better than a dumb guess?                  (baseline = always predict the average)
  5. Is a more complex model better?                  (Random Forest, Gradient Boosting)
  6. Does the app's clipping (30-95 C) hide problems? (share of predictions outside the range)

Install once:   pip install pandas numpy scikit-learn matplotlib
"""
import sys
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split, cross_validate, KFold
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

CSV = sys.argv[1] if len(sys.argv) > 1 else "cooling_data.csv"
FEATURES = ["Load", "Ambient_Temp", "RPM", "Oil_Condition"]   # same order as the app
TARGET = "Temperature"


def line(title=""):
    print("\n" + "=" * 68)
    if title:
        print(title)
        print("=" * 68)


# ---------------------------------------------------------------- 1. data
data = pd.read_csv(CSV)
line("1. DATA")
print(f"file: {CSV}")
print(f"rows: {len(data)}   columns: {list(data.columns)}")
missing = data[FEATURES + [TARGET]].isna().sum().sum()
print(f"missing values: {missing}   duplicate rows: {data.duplicated().sum()}")
print("\nranges:")
print(data[FEATURES + [TARGET]].describe().loc[["min", "mean", "max", "std"]].round(2).to_string())
print("\ncorrelation with Temperature (how strongly each input moves with the target):")
print(data[FEATURES + [TARGET]].corr()[TARGET].drop(TARGET).round(3).to_string())
print("\ncorrelation between inputs (values near +-1 = multicollinearity problem):")
print(data[FEATURES].corr().round(2).to_string())

X = data[FEATURES]
y = data[TARGET]

# ---------------------------------------------------------------- 2. model = what the app trains
line("2. WHAT THE MODEL LEARNED (same as the app: LinearRegression on all rows)")
full = LinearRegression().fit(X, y)
print(f"intercept (w0): {full.intercept_:.4f}")
std = X.std()
rows = []
for name, w in zip(FEATURES, full.coef_):
    rows.append((name, w, w * std[name]))
print(f"{'feature':<14}{'coefficient':>14}{'effect of 1 std-dev change (C)':>34}")
for name, w, s in rows:
    print(f"{name:<14}{w:>14.5f}{s:>34.3f}")
print("\nreading: coefficient = degrees C added per +1 unit of that input, other inputs fixed.")
print("the last column makes inputs comparable (a 1-unit change of RPM is tiny, of Load is big).")

# ---------------------------------------------------------------- 3. honest accuracy
line("3. ACCURACY ON UNSEEN DATA")
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42)
m = LinearRegression().fit(X_tr, y_tr)
p_tr, p_te = m.predict(X_tr), m.predict(X_te)
rmse = lambda a, b: float(np.sqrt(mean_squared_error(a, b)))
print(f"{'':<8}{'R2':>8}{'MAE (C)':>12}{'RMSE (C)':>12}")
print(f"{'train':<8}{r2_score(y_tr, p_tr):>8.3f}{mean_absolute_error(y_tr, p_tr):>12.2f}{rmse(y_tr, p_tr):>12.2f}")
print(f"{'test':<8}{r2_score(y_te, p_te):>8.3f}{mean_absolute_error(y_te, p_te):>12.2f}{rmse(y_te, p_te):>12.2f}")
print("\nR2 = share of temperature variation the model explains (1.0 = perfect, 0 = useless)")
print("MAE = average size of the error in degrees C; RMSE punishes big errors more")
print("if train is much better than test -> overfitting.  If both are similar -> the model generalises.")

kf = KFold(n_splits=5, shuffle=True, random_state=42)
cv = cross_validate(LinearRegression(), X, y, cv=kf, scoring=("r2", "neg_mean_absolute_error"))
print(f"\n5-fold cross-validation:  R2 = {cv['test_r2'].mean():.3f} (+- {cv['test_r2'].std():.3f})"
      f"   MAE = {-cv['test_neg_mean_absolute_error'].mean():.2f} C")

base_mae = mean_absolute_error(y_te, np.full(len(y_te), y_tr.mean()))
print(f"\nbaseline (always guess the average temperature): MAE = {base_mae:.2f} C")
print(f"your model MAE = {mean_absolute_error(y_te, p_te):.2f} C  ->  "
      f"{100 * (1 - mean_absolute_error(y_te, p_te) / base_mae):.0f}% smaller error than guessing")

# ---------------------------------------------------------------- 4. compare other models
line("4. IS A MORE COMPLEX MODEL BETTER?  (5-fold CV)")
models = {
    "Linear Regression (app)": LinearRegression(),
    "Random Forest": RandomForestRegressor(n_estimators=200, random_state=42),
    "Gradient Boosting": GradientBoostingRegressor(random_state=42),
}
print(f"{'model':<26}{'R2':>8}{'MAE (C)':>12}")
for name, mdl in models.items():
    r = cross_validate(mdl, X, y, cv=kf, scoring=("r2", "neg_mean_absolute_error"))
    print(f"{name:<26}{r['test_r2'].mean():>8.3f}{-r['test_neg_mean_absolute_error'].mean():>12.2f}")
print("\nif they are about equal, keep the simple model: it is explainable and cannot overfit easily.")
print("if the tree models are clearly better, the real relationship is non-linear (interactions).")

# ---------------------------------------------------------------- 5. clipping check
line("5. DOES THE APP'S CLIPPING (30-95 C) HIDE PROBLEMS?")
raw = full.predict(X)
above, below = (raw > 95).mean() * 100, (raw < 30).mean() * 100
print(f"training predictions above 95 C: {above:.1f}%   below 30 C: {below:.1f}%")
grid = pd.DataFrame({"Load": [100], "Ambient_Temp": [50], "RPM": [1800], "Oil_Condition": [40]})
print(f"worst-case slider setting (100%, 50 C, 1800 rpm, oil 40) -> raw prediction {full.predict(grid)[0]:.1f} C")
print("if raw predictions go far beyond 95, the app shows 95 and hides that the input is out of the trained range.")

# ---------------------------------------------------------------- 6. plots
try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.2))
    ax[0].scatter(y_te, p_te, s=14, alpha=0.7)
    lo, hi = min(y_te.min(), p_te.min()), max(y_te.max(), p_te.max())
    ax[0].plot([lo, hi], [lo, hi], "r--")
    ax[0].set_xlabel("actual temperature (C)"); ax[0].set_ylabel("predicted (C)"); ax[0].set_title("Predicted vs actual (test set)")
    ax[1].scatter(p_te, y_te - p_te, s=14, alpha=0.7); ax[1].axhline(0, color="r", ls="--")
    ax[1].set_xlabel("predicted (C)"); ax[1].set_ylabel("error = actual - predicted"); ax[1].set_title("Residuals (should look like random noise)")
    plt.tight_layout(); plt.savefig("model_evaluation.png", dpi=130)
    print("\nsaved plot: model_evaluation.png  (use it in your presentation)")
except Exception as e:
    print("\n(plot skipped:", e, ")")

line("DONE - copy the numbers from sections 2 and 3 into your presentation")
