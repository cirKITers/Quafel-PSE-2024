
# Create your views here.



from django.contrib.auth.decorators import login_required
from django.shortcuts import render

import plotly.express as px
import pandas as pd

@login_required
def index(request):
    # Generate the plot
    df = pd.DataFrame({
        "Qbits": list(range(16)),
        "Duration": list(1000 * (i ** 2) for i in range(16))
    })
    fig = px.density_contour(df, x="Qbits", y="Duration")
    graph_div = fig.to_html(full_html=False)

    # Pass the plot to the HTML template
    context = {'graph_div': graph_div}
    return render(request, 'index.html', context)