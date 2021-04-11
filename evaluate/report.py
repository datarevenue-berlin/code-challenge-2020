#' % Report
#' % Nikita Vinokurov
#' % 11-04-2021

#+ echo = False, results = 'hidden'
import shap
from catboost import CatBoostRegressor
from typing import Tuple
import pandas as pd
import numpy as np
import pickle
from catboost.utils import eval_metric
import itertools
import plotly
import plotly.graph_objs as go
from IPython.display import display_html


#+ echo = False, results = 'hidden'
def load_model(name: str) -> Tuple[CatBoostRegressor, pd.DataFrame, pd.Series]:
    model = CatBoostRegressor()
    model.load_model(fname='/usr/share/data/models/{}.cbm'.format(name), format='cbm')
    test_data = pickle.load(open('/usr/share/data/models/{}_test_pool.pickle'.format(name), 'rb'))
    test_label, test_data = test_data['labels'], test_data['data']
    return model, test_data, test_label

def get_group_data(column_name: str, data: pd.DataFrame, margins: np.array) -> pd.DataFrame:
    plot_data = []
    for group_name, group in itertools.groupby(sorted(zip(data[column_name].values, margins),
                                                      key=lambda x: x[0]),
                                               key=lambda x: x[0]):
        data = [x[1] for x in group]
        if len(data) > 10:
            plot_data.append((group_name, len(data), np.median(data)))
    return pd.DataFrame(plot_data, columns=[column_name, 'length', 'median_margin'])

def get_html(column: str, plot_data: pd.DataFrame) -> str:
    fig = go.Figure(layout_title_text="Errors by {}".format(column))
    fig.add_trace(go.Histogram(histfunc="sum",
                               x=plot_data[column],
                               y=plot_data['median_margin']
                              ))
    plotly_html = plotly.offline.plot(
        fig,
        include_plotlyjs="cdn",
        show_link=False,
        output_type='div'
    )
    return plotly_html

#' ## Description
#' 2 models were developed. The first model uses all factors that can be extracted. Second use factors which can be used in a real system that's why all description features and information about tasters like taster_name were deleted. Firstly we will analyze both models, their metric and feature dependencies, and then understand errors by groups.  

#+ echo = False, results = 'hidden'

model_full, test_full, test_labels_full = load_model('model_full')
model_real, test_real, test_labels_real = load_model('model_real')
predictions_full, predictions_real = model_full.predict(test_full), model_real.predict(test_real)
metric_full = round(eval_metric(test_labels_full.values, predictions_full, 'MAE')[0], 2)
metric_real = round(eval_metric(test_labels_real.values, predictions_real, 'MAE')[0], 2)
margins_real = np.abs(test_labels_real.values - predictions_real)

#' Full model has MAE = <%=metric_full%>, real has MAE = <%=metric_real%>

#' Importance of the variable and their dependencies for model with all variables
#+ echo = False

shap.initjs()
explainer = shap.TreeExplainer(model_full)
shap_values = explainer.shap_values(test_full)
shap.summary_plot(shap_values, test_full, max_display=40)


#' Importance of the variable and their dependencies for real model
#+ echo = False

shap.initjs()
explainer = shap.TreeExplainer(model_real)
shap_values = explainer.shap_values(test_real)
shap.summary_plot(shap_values, test_real, max_display=40)

#' Dependency of price to result variable
#+ echo = False
shap.dependence_plot("price", 
                     shap_values,
                     test_real,
                     interaction_index=None)

#' Dependency of year to result variable
#+ echo = False
shap.dependence_plot("year", 
                     shap_values,
                     test_real,
                     interaction_index=None)

#' Group analysis of countries

#+ echo = False
plot_data = get_group_data('country', test_real, margins_real)
plotly_html = get_html('country', plot_data)
display_html(plotly_html, raw=True)

#' Group analysis of designation

#+ echo = False
plot_data = get_group_data('designation', test_real, margins_real)
plotly_html = get_html('designation', plot_data)
display_html(plotly_html, raw=True)


#' Let's look on explaining of 3 random case
#+ echo = False
indecies = np.random.randint(len(test_labels_real), size=3)

#' Real label = <%=test_labels_real[indecies[0]]%>
#+ echo = False
ind = indecies[0]
shap.force_plot(explainer.expected_value, shap_values[ind], test_real.iloc[ind])

#' Real label = <%=test_labels_real[indecies[1]]%>
#+ echo = False
ind = indecies[1]
shap.force_plot(explainer.expected_value, shap_values[ind], test_real.iloc[ind])

#' Real label = <%=test_labels_real[indecies[2]]%>
#+ echo = False
ind = indecies[2]
shap.force_plot(explainer.expected_value, shap_values[ind], test_real.iloc[ind])


#' Let's look on explaining of 3 worth case errors
#+ echo = False
indecies = np.argsort(margins_real)[::-1][:3]

#' Real label = <%=test_labels_real[indecies[0]]%>
#+ echo = False
ind = indecies[0]
shap.force_plot(explainer.expected_value, shap_values[ind], test_real.iloc[ind])

#' Real label = <%=test_labels_real[indecies[1]]%>
#+ echo = False
ind = indecies[1]
shap.force_plot(explainer.expected_value, shap_values[ind], test_real.iloc[ind])

#' Real label = <%=test_labels_real[indecies[2]]%>
#+ echo = False
ind = indecies[2]
shap.force_plot(explainer.expected_value, shap_values[ind], test_real.iloc[ind])