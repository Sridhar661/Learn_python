# def get_worst_team_captain(teams):
#     """
#     Selects the captain of the worst team.
    
#     Parameters:
#     teams (list of lists): A list where each team is a list structured as 
#                            [Coach, Captain, Player1, Player2, ...] 
#                            ordered from best team to worst team.
                           
#     Returns:
#     str: The name of the captain of the worst team, or None if the list is empty/invalid.
#     """
#     if not teams:
#         return None  # Handle empty list case
        
#     worst_team = teams[-1]  # The worst team is at the end of the list
    
#     if len(worst_team) < 2:
#         return None  # Handle case where a team list doesn't have a captain listed
        
#     return worst_team[1]  # The captain is the second element (index 1)

# # --- Example Usage ---
# sports_teams = [
#     ["Coach Alex", "Captain Bob", "Player 1", "Player 2"],   # Best Team
#     ["Coach Charlie", "Captain Dave", "Player 3"],           # Middle Team
#     ["Coach Eve", "Captain Frank", "Player 5", "Player 6"]   # Worst Team
# ]

# print(get_worst_team_captain(sports_teams))  # Output: Captain Frank






i = 0
while i < 10:
    print(i, end=' ')
    i += 1 