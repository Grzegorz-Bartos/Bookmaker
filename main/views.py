import csv
import json
from django.shortcuts import render, redirect
from .forms import CSVUploadForm
from .models import Match, Coupon, Bet, BetSelection
from django.shortcuts import get_object_or_404
from datetime import datetime
from .utils import update_coupon_status
from django.db.models.functions import TruncDate


def main(request):
    return render(request, "base.html")

def upload_csv(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file'].read().decode('utf-8').splitlines()
            reader = csv.reader(csv_file)
            next(reader)  # Skip the header row

            for row in reader:
                # Parse the date from the format 'Jul 21 2023 - 4:00pm' to 'YYYY-MM-DD HH:MM'
                match_date = datetime.strptime(row[1], '%b %d %Y - %I:%M%p').strftime('%Y-%m-%d %H:%M')

                # Extract the goals for home and away teams
                home_goals = int(row[12])  # home_team_goal_count column
                away_goals = int(row[13])  # away_team_goal_count column

                # Determine the result based on goal counts
                if home_goals > away_goals:
                    result = "1"  # Home win
                elif home_goals == away_goals:
                    result = "0"  # Draw
                else:
                    result = "2"  # Away win

                # Create the match object
                Match.objects.create(
                    team1=row[4],  # home_team_name
                    team2=row[5],  # away_team_name
                    match_date=match_date,  # Use the converted match date
                    odds_ft_home_team_win=row[56],  # odds_ft_home_team_win
                    odds_ft_draw=row[57],  # odds_ft_draw from CSV
                    odds_ft_away_team_win=row[58],  # odds_ft_away_team_win
                    result=result  # Save the calculated result
                )

            return render(request, 'upload_success.html')
    else:
        form = CSVUploadForm()
    return render(request, 'upload.html', {'form': form})


def match_list(request):
    matches = Match.objects.all()

    unique_dates = Match.objects.annotate(
        date=TruncDate('match_date')).values_list('date', flat=True).distinct()
    context = {
        'matches': matches,
        'unique_dates': unique_dates,
    }
    return render(request, 'match_list.html', context)


def create_coupon(request):
    if request.method == 'POST':
        bets = []
        total_odds = 1

        # Retrieve and validate the stake
        stake = request.POST.get('stake', None)
        if not stake or stake == "":
            return render(request, 'match_list.html', {'error': 'Stake is required.'})

        try:
            stake = float(stake)
            if stake <= 0:
                raise ValueError("Stake must be a positive number.")
        except ValueError:
            return render(request, 'match_list.html', {'error': 'Invalid stake value.'})

        # Retrieve the bet-slip-data (as JSON string)
        bet_slip_data = request.POST.get('bet-slip-data', None)
        if not bet_slip_data:
            return render(request, 'match_list.html', {'error': 'No bet selections found.'})

        # Deserialize the bet-slip-data into a Python list
        bet_slip = json.loads(bet_slip_data)

        # Loop through the bet slip and process each bet to calculate total odds
        for bet in bet_slip:
            odds = float(bet.get('odds'))
            total_odds *= odds  # Multiply the total odds

            # Append the bet details
            bets.append({
                'matchId': bet.get('matchId'),
                'event': bet.get('event'),
                'odds': odds
            })

        # Calculate potential winnings
        potential_winnings = stake * total_odds

        # Store the coupon in the database before creating BetSelection entries
        coupon = Coupon.objects.create(stake=stake, total_odds=total_odds, potential_winnings=potential_winnings)

        # Now create the BetSelection entries tied to the coupon
        for bet in bets:
            match_instance = Match.objects.get(id=bet['matchId'])  # Fetch match using matchId
            BetSelection.objects.create(
                coupon=coupon,
                match=match_instance,
                event=bet['event'],
                odds=bet['odds']
            )

        update_coupon_status(coupon)

        # Redirect to coupon success page after successful creation
        return redirect('coupon', coupon_id=coupon.id)

    return redirect('match_list')


def coupon_list(request):
    # Retrieve all coupons, order by the most recent
    coupons = Coupon.objects.all().order_by('-created_at')
    return render(request, 'coupon_list.html', {'coupons': coupons})

def coupon(request, coupon_id=None):
    # Retrieve the coupon object
    coupon = get_object_or_404(Coupon, id=coupon_id)

    # Retrieve all related BetSelection objects for this coupon
    bet_selections = BetSelection.objects.filter(coupon=coupon)

    # Render the coupon and its details, including bet selections
    return render(request, 'coupon.html', {
        'coupon': coupon,
        'bet_selections': bet_selections  # Pass the bet selections to the template
    })
