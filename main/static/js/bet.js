let betSlip = [];
let totalOdds = 0;

// Event listener for match odds selection
document.querySelectorAll('.match-odds').forEach(oddElement => {
    oddElement.addEventListener('click', function() {
        const match = this.getAttribute('data-match');
        const matchId = this.getAttribute('data-match-id'); // Retrieve match_id
        const event = this.getAttribute('data-event');
        const odds = parseFloat(this.getAttribute('data-odds'));

        // Prevent duplicate bets on the same match
        const existingBet = betSlip.find(bet => bet.matchId === matchId); // Compare by matchId now
        if (existingBet) {
            alert(`You have already selected a bet for this match: ${match}. Please remove it before adding another.`);
            return;
        }

        // Add to the bet slip array
        betSlip.push({ matchId, match, event, odds }); // Include matchId
        this.classList.add('selected-bet');
        // Update the bet slip UI
        updateBetSlip();
    });
});

// Function to update the bet slip UI and calculate total odds
function updateBetSlip() {
    const betSlipContent = document.getElementById('bet-slip-content');
    betSlipContent.innerHTML = ''; // Clear previous content
    totalOdds = 1; // Reset total odds

    // Iterate over the bet slip and update the UI
    betSlip.forEach((bet, index) => {
        const betElement = document.createElement('div');
        betElement.className = 'bet-item';
        betElement.innerHTML = `
            <p>${bet.match} - ${bet.event}: <strong>${bet.odds}</strong></p>
            <button onclick="removeBet(${index})" class="btn btn-danger btn-sm">Remove</button>
        `;
        betSlipContent.appendChild(betElement);
        totalOdds *= bet.odds; // Calculate total odds
    });

    // Handle case when no bets are added
    if (betSlip.length === 0) {
        betSlipContent.innerHTML = '<p>No bets added.</p>';
    }

    // Update total odds in the slip
    document.getElementById('total-odds').innerText = totalOdds.toFixed(2);
    document.getElementById('total-odds-field').value = totalOdds.toFixed(2); // Hidden input for form submission

    // Set bet slip data for form submission
    document.getElementById('bet-slip-data').value = JSON.stringify(betSlip); // Serialize bet slip for the form
}

// Function to remove a bet from the bet slip
function removeBet(index) {
    // Get the match ID of the bet being removed
    const removedBet = betSlip[index];
    const matchId = removedBet.matchId;

    // Remove the bet at the specified index from the bet slip
    betSlip.splice(index, 1);

    // Update the UI after removing the bet
    updateBetSlip();

    // Revert the appearance of all match odds for the removed match
    document.querySelectorAll(`.match-odds[data-match-id="${matchId}"]`).forEach(element => {
        element.classList.remove('selected-bet'); // Remove the highlight class
    });

}

// Function to calculate potential winnings based on stake and total odds
function calculateWinnings() {
    // Ensure there is at least one bet in the bet slip
    if (betSlip.length === 0) {
        alert('Please add at least one bet to the bet slip.');
        return;
    }

    // Retrieve and validate the stake entered by the user
    const stake = parseFloat(document.getElementById('stake').value);
    if (isNaN(stake) || stake <= 0) {
        alert('Please enter a valid stake.');
        return;
    }

    // Calculate potential winnings
    const potentialWinnings = stake * totalOdds;
    document.getElementById('potential-winnings').innerText = potentialWinnings.toFixed(2);

    // Set the stake value in the hidden form field (if necessary for submission)
    document.getElementById('stake-field').value = stake;
}
