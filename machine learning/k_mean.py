import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans

img = mpimg.imread('../data/girl3.jpg')
plt.imshow(img)
imgplot = plt.imshow(img)
plt.axis('off')
X = img.reshape((img.shape[0]*img.shape[1], img.shape[2]))
for K in [10]:
    kmeans = KMeans(n_clusters=K).fit(X)
    label = kmeans.predict(X)

    img4 = np.zeros_like(X)
    # replace each pixel by its center
    for k in range(K):
        img4[label == k] = kmeans.cluster_centers_[k]
    # reshape and display output image
    img5 = img4.reshape((img.shape[0], img.shape[1], img.shape[2]))
    plt.imshow(img5, interpolation='nearest')
    plt.axis('off')
    plt.show()


# KMeans function parameter
# n_clusters=8, -- So cluster
# init='k-means++'
# n_init=10, --thoi gian chay cua thuat toan
# max_iter=300, -- So lan lap toi da
# tol=0.0001, precompute_distances='auto'
# verbose=0, random_state=None,
# copy_x=True, n_jobs=1, algorithm='auto'
