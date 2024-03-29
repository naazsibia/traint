from .models import Rating, Dress, Cluster
from django.contrib.auth.models import User
from sklearn.cluster import KMeans
from scipy.sparse import dok_matrix, csr_matrix
import numpy as np

# Credit: https://www.codementor.io/jadianes/build-data-products-django-machine-learning-clustering-user-preferences-du107s5mk
def update_clusters():
    num_ratings = Rating.objects.count()
    update_step = ((num_ratings/100)+1) * 5
    if num_ratings % update_step == 0: # using some magic numbers here, sorry...
        # Create a sparse matrix from user ratings
        all_user_names = map(lambda x: x.username, User.objects.only("username"))
        all_dress_ids = set(map(lambda x: x.dress.id, Rating.objects.only("dress")))
        num_users = len(all_user_names)
        ratings_m = dok_matrix((num_users, max(all_dress_ids)+1), dtype=np.float32)
        for i in range(num_users): # each user corresponds to a row, in the order of all_user_names
            user_ratings = Rating.objects.filter(user_name=all_user_names[i])
            for user_rating in user_ratings:
                ratings_m[i,user_rating.dress.id] = user_rating.rating

        # Perform kmeans clustering
        k = int(num_users / 10) + 2
        kmeans = KMeans(n_clusters=k)
        clustering = kmeans.fit(ratings_m.tocsr())
        
        # Update clusters
        Cluster.objects.all().delete()
        new_clusters = {i: Cluster(name=i) for i in range(k)}
        for cluster in new_clusters.values(): # clusters need to be saved before referring to users
            cluster.save()
        for i,cluster_label in enumerate(clustering.labels_):
            new_clusters[cluster_label].users.add(User.objects.get(username=all_user_names[i]))