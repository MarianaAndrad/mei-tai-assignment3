import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
file_path = './classification_genre_test.csv'
data = pd.read_csv(file_path)

# General statistical description
stats = data.describe(include='all')
print("General Descriptive Statistics:")
print(stats)

# Performance Analysis by Genre
performance_by_genre = data.groupby('genre').mean(numeric_only=True)[['precision', 'recall', 'f1-score', 'accuracy']]
performance_by_genre.plot(kind='bar', figsize=(12, 8), title='Performance by Genre', ylim=(0, 1))
plt.ylabel('Metric')
plt.legend(loc='upper right')
plt.savefig('./plots/classification_genre_test_genre.png')
plt.show()

# Impact of Compression Method
performance_by_compression = data.groupby('methodCompression').mean(numeric_only=True)[['precision', 'recall', 'f1-score', 'accuracy']]
performance_by_compression.plot(kind='bar', figsize=(12, 8), title='Impact of Compression Method', ylim=(0, 1))
plt.ylabel('Metric')
plt.legend(loc='upper right')
plt.savefig('./plots/classification_genre_test_methodCompression.png')
plt.show()

# Effect of Data Partition
performance_by_partition = data.groupby('partition').mean(numeric_only=True)[['precision', 'recall', 'f1-score', 'accuracy']]
performance_by_partition.plot(kind='bar', figsize=(12, 8), title='Effect of Data Partition', ylim=(0, 1))
plt.ylabel('Metric')
plt.legend(loc='upper right')
plt.savefig('./plots/classification_genre_test.png')
plt.show()

# Load the CSV file
file_path = './classification_genre_noise_test.csv'
data = pd.read_csv(file_path)

# Impact of Noise Level
data_with_noise = data.dropna(subset=['noise_level'])
performance_by_noise_level = data_with_noise.groupby('noise_level').mean(numeric_only=True)[['precision', 'recall', 'f1-score', 'accuracy']]
performance_by_noise_level.plot(kind='bar', figsize=(12, 8), title='Impact of Noise Level', ylim=(0, 1))
plt.ylabel('Metric')
plt.legend(loc='upper right')
plt.savefig('./plots/classification_genre_noise_test.png')
plt.show()

# Load the CSV file
file_path = './classification_genre_unseen.csv'
data = pd.read_csv(file_path)

# General statistical description
stats = data.describe(include='all')
print("General Descriptive Statistics:")
print(stats)

# Performance Analysis by Genre
performance_by_genre = data.groupby('genre').mean(numeric_only=True)[['precision', 'recall', 'f1-score', 'accuracy']]
performance_by_genre.plot(kind='bar', figsize=(12, 8), title='Performance by Genre', ylim=(0, 1))
plt.ylabel('Metric')
plt.legend(loc='upper right')
plt.savefig('./plots/classification_genre_unseen_genre.png')
plt.show()

# Impact of Compression Method
performance_by_compression = data.groupby('methodCompression').mean(numeric_only=True)[['precision', 'recall', 'f1-score', 'accuracy']]
performance_by_compression.plot(kind='bar', figsize=(12, 8), title='Impact of Compression Method', ylim=(0, 1))
plt.ylabel('Metric')
plt.legend(loc='upper right')
plt.savefig('./plots/classification_genre_unseen_methodCompression.png')
plt.show()

# Effect of Data Partition
performance_by_partition = data.groupby('partition').mean(numeric_only=True)[['precision', 'recall', 'f1-score', 'accuracy']]
performance_by_partition.plot(kind='bar', figsize=(12, 8), title='Effect of Data Partition', ylim=(0, 1))
plt.ylabel('Metric')
plt.legend(loc='upper right')
plt.savefig('./plots/classification_genre_unseen_partition.png')
plt.show()
