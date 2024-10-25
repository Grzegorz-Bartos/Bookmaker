from django.db import models

class Match(models.Model):
    match_date = models.DateTimeField()
    team1 = models.CharField(max_length=100)
    team2 = models.CharField(max_length=100)
    result = models.CharField(max_length=10, blank=True, null=True)

    odds_ft_home_team_win = models.DecimalField(max_digits=5, decimal_places=2)
    odds_ft_draw = models.DecimalField(max_digits=5, decimal_places=2)
    odds_ft_away_team_win = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.team1} vs {self.team2} on {self.match_date}"


class Coupon(models.Model):
    matches = models.ManyToManyField('Match', through='BetSelection')
    stake = models.DecimalField(max_digits=12, decimal_places=2)
    total_odds = models.DecimalField(max_digits=12, decimal_places=4)
    potential_winnings = models.DecimalField(max_digits=12, decimal_places=4)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default="Pending")

class Bet(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    selected_event = models.CharField(max_length=100)
    stake = models.DecimalField(max_digits=10, decimal_places=2)
    result = models.BooleanField(default=False)

    def __str__(self):
        return f"Bet on {self.match} - {self.selected_event}"


class BetSelection(models.Model):
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)
    match = models.ForeignKey('Match', on_delete=models.CASCADE)
    event = models.CharField(max_length=50)  # Home Win, Draw, Away Win
    odds = models.DecimalField(max_digits=5, decimal_places=2)