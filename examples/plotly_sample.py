# <div>
# --8<-- "figure1.html"
# </div>


import plotly.graph_objects as go
fig = go.Figure(
    data=[go.Bar(y=[2, 1, 3])],
)

fig.write_html("figure1.html", include_plotlyjs='cdn', full_html=False)