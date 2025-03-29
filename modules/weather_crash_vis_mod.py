import plotly.graph_objects as go
import plotly.io as pio


def init_figs():
    """
    Sets the theme
    """
    pio.templates.default = 'plotly_dark'


# The body of this function is mostly AI generated
def create_fig_CraWeath(df_CraWeath):
    """
    Takes a dataframe 

    Creates a bar chart from dataframe data

    Returns the bar chart as a plotly figure object
    """
    fig_CraWeath = go.Figure()
    fig_CraWeath.add_trace(
        go.Bar(
            x=df_CraWeath['Condition'],
            y=df_CraWeath['incidents_ratio'],
            name='Incident Rate',
            marker=dict(color='lightblue'),
        )
    )
    fig_CraWeath.add_trace(
        go.Bar(
            x=df_CraWeath['Condition'],
            y=df_CraWeath['technical_ratio'],
            name='Technical Failure Rate',
            marker=dict(color='deepskyblue'),
        )
    )
    fig_CraWeath.add_trace(
        go.Bar(
            x=df_CraWeath['Condition'],
            y=df_CraWeath['completed_ratio'],
            name='Completed Rate',
            marker=dict(color='dodgerblue'),
        )
    )
    fig_CraWeath.update_layout(
        title='Race Outcome Rates by Weather Condition',
        xaxis_title='Weather Condition',
        yaxis_title='Rate',
        barmode='group',
        plot_bgcolor='black',
        paper_bgcolor='black',
        yaxis_tickformat='.0%',
    )
    fig_CraWeath.update_traces(hovertemplate='%{y:.2%}')
    return fig_CraWeath
