from django.db import models
from django.contrib.auth.models import User

# Create your models here.

#Post table
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    desc = models.CharField(max_length=500)
    image = models.ImageField(upload_to="images/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

#Follow table
class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')

    #for having unique pairs
    class Meta:
        unique_together = ('follower', 'following')

    def __str__(self):
        return f'{self.follower.username} follows {self.following.username}'

#Liked table
class Like(models.Model):
    likedBy = models.ForeignKey(User, on_delete=models.CASCADE)
    likedPost = models.ForeignKey(Post, on_delete=models.CASCADE)

    #again for having unique pairs
    class Meta:
        unique_together = ( 'likedBy', 'likedPost')

    def __str__(self):
        return f'{self.likedBy.username} liked {self.likedPost}'
    
#comment table
class Comment(models.Model):
    comment = models.CharField(max_length=300)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.user}: {self.comment}'