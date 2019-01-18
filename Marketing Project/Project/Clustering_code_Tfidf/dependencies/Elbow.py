from sklearn.cluster import KMeans
from sklearn import metrics
import matplotlib.pyplot as plt
def elbow_curve(start,end,tfidf_matrix):
    nc = range(start,end)
    kmeans = [KMeans(n_clusters = i, n_init = 100, max_iter = 500, precompute_distances = 'auto' ) for i in nc]
    score = [kmeans[i].fit(tfidf_matrix).score(tfidf_matrix) for i in range(len(kmeans))]
    plt.plot(nc,score)
    plt.xlabel('Number of Clusters')
    plt.ylabel('Score')
    plt.title('Elbow Curve')
    plt.show()
