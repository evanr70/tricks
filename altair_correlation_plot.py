import pandas as pd
import altair as alt

def one_hot_encode(dataframe, columns, restrict=False):
    assert isinstance(columns, list), "`columns` must be passed in a list"
    one_hot = pd.get_dummies(dataframe[columns]).corr()
    return one_hot


def tidy_correlation_matrix(correlation_matrix, columns=False):
    if columns:
        correlation_matrix = correlation_matrix[[column for column in correlation_matrix.columns if columns[0] not in column]].loc[[row for row in correlation_matrix.index if columns[1] not in row]]
    tidy_data = correlation_matrix.stack().reset_index()
    tidy_data.columns = ['x', 'y', 'val']
    return tidy_data

def plot_tidy_corr(tidy_data, xargs={}, yargs={}):
    heatmap = alt.Chart(tidy_data).mark_rect().encode(
        x=alt.X('x:N', **xargs),
        y=alt.Y('y:N', **yargs),
        color='val:Q',
        tooltip=['x:N', 'y:N', 'val:Q']
    )

    return heatmap

def generate_heatmap(dataframe, columns, restrict=False, xargs={}, yargs={}):
    correlation_matrix = one_hot_encode(dataframe, columns, restrict)
    tidy_data = tidy_correlation_matrix(correlation_matrix, columns)
    heatmap = plot_tidy_corr(tidy_data, xargs, yargs)
    return heatmap
