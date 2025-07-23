from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings

# ================================
# ✅ Custom User Manager
# ================================

class CustomUserManager(BaseUserManager):
    def create_user(self, email, user_name, password=None, **extra_kwargs):
        if not email:
            raise ValueError("Email is required")
        if not user_name:
            raise ValueError("Username is required")

        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name, **extra_kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, user_name, password=None, **extra_kwargs):
        extra_kwargs.setdefault('is_staff', True)
        extra_kwargs.setdefault('is_active', True)
        extra_kwargs.setdefault('is_superuser', True)

        if extra_kwargs.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_kwargs.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, user_name, password, **extra_kwargs)

# ================================
# ✅ Custom User Model
# ================================

class CustomUser(AbstractBaseUser, PermissionsMixin):
    user_name = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_of_join = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.user_name


# ================================
# ✅ Abstract Base Model
# ================================

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# ================================
# ✅ Profile Model
# ================================

class ProfileModel(BaseModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    location = models.CharField(max_length=250, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# ================================
# ✅ Post Model
# ================================

class PostModel(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=100, blank=True, null=True)
    content = models.TextField()
    post_image = models.ImageField(upload_to='posts/', blank=True, null=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_posts', blank=True)

    def __str__(self):
        return self.title or self.content[:20]

    def like_count(self):
        return self.likes.count()


# ================================
# ✅ Comment Model
# ================================

class CommentModel(BaseModel):
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='liked_comments',
        blank=True
    )

    def __str__(self):
        return f"Comment by {self.user} on {self.post}"

    def like_count(self):
        return self.likes.count()  # Implement if comments are likeable


# ================================
# ✅ Follow Model
# ================================

class FollowModel(BaseModel):
    follower = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='followers')

    def __str__(self):
        return f'{self.follower} follows {self.following}'
