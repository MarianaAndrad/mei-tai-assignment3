import zlib
import numpy as np
from scipy.cluster.hierarchy import linkage, dendrogram
from scipy.spatial.distance import squareform
import matplotlib.pyplot as plt

def compress(data):
    """Compress data using zlib and return the compressed size."""
    return len(zlib.compress(data))

def ncd(x, y):
    """Calculate the Normalized Compression Distance between two byte sequences."""
    Cx = compress(x)
    Cy = compress(y)
    Cxy = compress(x + y)
    return (Cxy - min(Cx, Cy)) / max(Cx, Cy)

def create_distance_matrix(data):
    """Create a distance matrix using NCD for a list of byte sequences."""
    n = len(data)
    dist_matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            dist = ncd(data[i], data[j])
            dist_matrix[i, j] = dist
            dist_matrix[j, i] = dist
    return dist_matrix

def plot_dendrogram(distance_matrix, labels):
    """Plot a dendrogram from a given distance matrix."""
    # Convert the distance matrix to condensed form
    condensed_dist_matrix = squareform(distance_matrix)
    linkage_matrix = linkage(condensed_dist_matrix, method='average')
    plt.figure(figsize=(10, 5))  # Change the figure size as needed
    dendrogram(
        linkage_matrix,
        labels=labels,
        leaf_rotation=90,  # Rotate labels
        leaf_font_size=12,  # Change the font size
        color_threshold=0.5,  # Change this threshold as needed to add more colors
    )
    plt.title("Dendrogram")
    plt.xlabel("Music Pieces")
    plt.ylabel("Distance")
    plt.tight_layout()  # Adjust layout
    plt.show()

# Example usage
if __name__ == "__main__":
    # Sample data: replace with your actual music data in byte sequences
    data = [
        b"music piece 1",
        b"nova tentativa",
        b"music piece 3",
        b"music piece 3",
        b"music",
        b"music nova play",
    ]

    labels = ["Piece 1", "Piece 2", "Piece 3", "Piece 4", "Piece 5", "Piece 6"]  # Add labels for your music pieces

    dist_matrix = create_distance_matrix(data)
    plot_dendrogram(dist_matrix, labels)
