import pandas as pd
import matplotlib.pyplot as plt

# Carregar o arquivo CSV
file_path = './classification_genre_test.csv'
data = pd.read_csv(file_path)

# Descrição estatística geral
stats = data.describe(include='all')
print("Estatísticas Descritivas Gerais:")
print(stats)

# Análise de Desempenho por Gênero
performance_by_genre = data.groupby('genre').mean(numeric_only=True)[['precision', 'recall', 'f1-score', 'accuracy']]
performance_by_genre.plot(kind='bar', figsize=(12, 8), title='Desempenho por Gênero', ylim=(0, 1))
plt.ylabel('Métrica')
plt.legend(loc='upper right')
plt.savefig('./plots/classification_genre_test_genre.png')
plt.show()

# Impacto do Método de Compressão
performance_by_compression = data.groupby('methodCompression').mean(numeric_only=True)[['precision', 'recall', 'f1-score', 'accuracy']]
performance_by_compression.plot(kind='bar', figsize=(12, 8), title='Impacto do Método de Compressão', ylim=(0, 1))
plt.ylabel('Métrica')
plt.legend(loc='upper right')
plt.savefig('./plots/classification_genre_test_methodCompression.png')
plt.show()

# Efeito da Partição de Dados
performance_by_partition = data.groupby('partition').mean(numeric_only=True)[['precision', 'recall', 'f1-score', 'accuracy']]
performance_by_partition.plot(kind='bar', figsize=(12, 8), title='Efeito da Partição de Dados', ylim=(0, 1))
plt.ylabel('Métrica')
plt.legend(loc='upper right')
plt.savefig('./plots/classification_genre_test.png')
plt.show()

# Carregar o arquivo CSV
file_path = './classification_genre_noise_test.csv'
data = pd.read_csv(file_path)

# Impacto do Nível de Ruído
data_with_noise = data.dropna(subset=['noise_level'])
performance_by_noise_level = data_with_noise.groupby('noise_level').mean(numeric_only=True)[['precision', 'recall', 'f1-score', 'accuracy']]
performance_by_noise_level.plot(kind='bar', figsize=(12, 8), title='Impacto do Nível de Ruído', ylim=(0, 1))
plt.ylabel('Métrica')
plt.legend(loc='upper right')
plt.savefig('./plots/classification_genre_noise_test.png')
plt.show()

# Carregar o arquivo CSV
file_path = './classification_genre_unseen.csv'
data = pd.read_csv(file_path)

# Descrição estatística geral
stats = data.describe(include='all')
print("Estatísticas Descritivas Gerais:")
print(stats)

# Análise de Desempenho por Gênero
performance_by_genre = data.groupby('genre').mean(numeric_only=True)[['precision', 'recall', 'f1-score', 'accuracy']]
performance_by_genre.plot(kind='bar', figsize=(12, 8), title='Desempenho por Gênero', ylim=(0, 1))
plt.ylabel('Métrica')
plt.legend(loc='upper right')
plt.savefig('./plots/classification_genre_unseen_genre.png')
plt.show()

# Impacto do Método de Compressão
performance_by_compression = data.groupby('methodCompression').mean(numeric_only=True)[['precision', 'recall', 'f1-score', 'accuracy']]
performance_by_compression.plot(kind='bar', figsize=(12, 8), title='Impacto do Método de Compressão', ylim=(0, 1))
plt.ylabel('Métrica')
plt.legend(loc='upper right')
plt.savefig('./plots/classification_genre_unseen_methodCompression.png')
plt.show()

# Efeito da Partição de Dados
performance_by_partition = data.groupby('partition').mean(numeric_only=True)[['precision', 'recall', 'f1-score', 'accuracy']]
performance_by_partition.plot(kind='bar', figsize=(12, 8), title='Efeito da Partição de Dados', ylim=(0, 1))
plt.ylabel('Métrica')
plt.legend(loc='upper right')
plt.savefig('./plots/classification_genre_unseen_partition.png')
plt.show()

