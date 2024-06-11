import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def plot_music(music_data, save=False, test=True):
    methods = music_data['methodCompression'].unique()
    params = ['ws', 'ds', 'nf', 'sh']

    # Create a figure for the plots
    fig, axs = plt.subplots(2, 2, figsize=(15, 10))

    # Plot Accuracy per parameter
    for i, param in enumerate(params):
        row, col = divmod(i, 2)
        for method in methods:
            subset = music_data[music_data['methodCompression'] == method]
            avg_accuracy = subset.groupby(param)['accuracy'].mean()
            axs[row, col].plot(avg_accuracy.index, avg_accuracy.values, marker='o', label=method)

        axs[row, col].set_xscale('log', base=2)
        axs[row, col].set_title(f'Accuracy per {param}')
        axs[row, col].set_xlabel(param)
        axs[row, col].set_ylabel('Accuracy')
        axs[row, col].legend()

    plt.tight_layout()
    if save:
        plt.savefig(f"plots/music_algorithm_per_parameter_{'test' if test else 'unseen'}.png")
        plt.show()
    else:
        plt.show()


# Load all the CSV files
classification_music_unseen = pd.read_csv('./classification_music_unseen.csv')
classification_genre_noise_test = pd.read_csv('./classification_genre_noise_test.csv')
classification_genre_noise_unseen = pd.read_csv('./classification_genre_noise_unseen.csv')
classification_genre_unseen = pd.read_csv('./classification_genre_unseen.csv')
classification_music_noise_test = pd.read_csv('./classification_music_noise_test.csv')
classification_music_noise_unseen = pd.read_csv('./classification_music_noise_unseen.csv')
classification_music_test = pd.read_csv('./classification_music_test.csv')

# Combine relevant data from all dataframes to identify notable results
# This analysis will focus on the `accuracy` and `noise_level` columns across the different datasets

# Extract relevant columns for each dataset
music_unseen = classification_music_unseen[['accuracy', 'methodCompression', 'partition']]
genre_noise_test = classification_genre_noise_test[['noise_level', 'accuracy', 'methodCompression', 'partition']]
genre_noise_unseen = classification_genre_noise_unseen[['noise_level', 'accuracy', 'methodCompression', 'partition']]
genre_unseen = classification_genre_unseen[['accuracy', 'methodCompression', 'partition']]
music_noise_test = classification_music_noise_test[['noise_level', 'accuracy', 'methodCompression', 'partition']]
music_noise_unseen = classification_music_noise_unseen[['noise_level', 'accuracy', 'methodCompression', 'partition']]
music_test = classification_music_test[['accuracy', 'methodCompression', 'partition']]

# Concatenate dataframes for a comprehensive view
combined_data = pd.concat(
    [music_unseen, genre_noise_test, genre_noise_unseen, genre_unseen, music_noise_test, music_noise_unseen,
     music_test], keys=[
        'music_unseen', 'genre_noise_test', 'genre_noise_unseen', 'genre_unseen', 'music_noise_test',
        'music_noise_unseen', 'music_test'
    ])

# Group by noise level and methodCompression to calculate mean accuracy for each combination
summary = combined_data.groupby(['noise_level', 'methodCompression']).agg({'accuracy': ['mean', 'std']}).reset_index()
summary.columns = ['noise_level', 'methodCompression', 'mean_accuracy', 'std_accuracy']

# Create the line chart: Accuracy vs. Noise Level for Each Compression Method
summary_pivot = summary.pivot(index='noise_level', columns='methodCompression', values='mean_accuracy')

plt.figure(figsize=(12, 10))
for method in summary_pivot.columns:
    plt.plot(summary_pivot.index, summary_pivot[method], marker='o', label=method)

plt.xlabel('Noise Level')
plt.ylabel('Mean Accuracy')
plt.title('Mean Accuracy vs. Noise Level by Compression Method')
plt.legend(title='Compression Method')
plt.grid(True)
plt.savefig('./plots/accuracy_vs_noise_level_line_chart.png')
plt.show()

# Create the box plot: Accuracy Distribution by Noise Level and Compression Method
plt.figure(figsize=(12, 8))
sns.boxplot(x='noise_level', y='accuracy', hue='methodCompression', data=combined_data)
plt.xlabel('Noise Level')
plt.ylabel('Accuracy')
plt.title('Accuracy Distribution by Noise Level and Compression Method')
plt.legend(title='Compression Method', loc='lower right')
plt.savefig('./plots/accuracy_distribution_box_plot.png')
plt.show()

# Save the summary data to a CSV file
plot_music(classification_music_test, save=True)
