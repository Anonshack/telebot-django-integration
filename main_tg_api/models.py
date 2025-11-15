from django.db import models


class BotUsers(models.Model):
    user_id = models.CharField(
        max_length=60,
        unique=True,
        db_index=True,
        verbose_name="Telegram User ID"
    )
    name = models.CharField(
        max_length=60,
        null=True,
        blank=True,
        verbose_name="Full Name"
    )
    username = models.CharField(
        max_length=60,
        null=True,
        blank=True,
        verbose_name="Telegram Username"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Registered At"
    )

    class Meta:
        verbose_name = "Bot User"
        verbose_name_plural = "Bot Users"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name or 'No Name'} (@{self.username or 'No username'})"

    @property
    def clean_username(self):
        if self.username:
            return self.username.replace("@", "")
        return None

    def get_info(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "username": self.username,
            "joined": self.created_at.strftime("%Y-%m-%d %H:%M")
        }


class FeedbackForAdmin(models.Model):
    user = models.ForeignKey(
        BotUsers,
        on_delete=models.CASCADE,
        related_name="feedbacks",
        verbose_name="User"
    )
    text = models.TextField(verbose_name="Feedback Message")
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Sent At"
    )

    class Meta:
        verbose_name = "User Feedback"
        verbose_name_plural = "All User Feedbacks"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Feedback from @{self.user.username or 'Unknown'}"

    def short_text(self):
        return (self.text[:30] + "...") if len(self.text) > 30 else self.text
