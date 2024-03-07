import seaborn as sns
import pandas as pd
import matplotlib as plt
# Setting up the data for the bar chart
data = {
    'Metric': ['Accuracy', 'Accuracy', 'Loss', 'Loss'],
    'Model': ['Tiny', 'Tiny x10', 'Tiny', 'Tiny x10'],
    'Value': [0.716586, 0.726731, 0.846463, 0.777506]
}

df = pd.DataFrame(data)

# Plotting with seaborn
plt.figure(figsize=(8, 6))
bar_plot = sns.barplot(x='Metric', y='Value', hue='Model', data=df)

# Adding the values on top of the bars
for p in bar_plot.patches:
    bar_plot.annotate(format(p.get_height(), '.2f'), 
                      (p.get_x() + p.get_width() / 2., p.get_height()), 
                      ha = 'center', va = 'center', 
                      xytext = (0, 9), 
                      textcoords = 'offset points')

plt.title('Test Data Performance')
plt.show()
