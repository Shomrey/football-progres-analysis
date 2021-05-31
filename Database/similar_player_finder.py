#from Database.database_query_wrapper import run_query, run_query_pandas
from database_query_wrapper import run_query, run_query_pandas
import pandas as pd

def generate_arg_query_part(argument, value):
    return " CAST(ABS({arg}-{val}) as REAL)/{val} ".format(arg = argument, val = value)

def args_to_list(list_of_args):
    tmp = list_of_args.copy()
    result = tmp.pop(0)
    for arg in tmp:
        result += ', '
        result += arg

    return result

# search arguments
player_guid = 227
year = 2017
arguments = ['goals_scored', 'assists']
number_of_players = 5

# finding result of the player
player_values_query = "SELECT {args} FROM player_statistics WHERE Guid = {guid} AND Year = {year}"
player_stats_run_query = player_values_query.format(args = args_to_list(arguments), guid = player_guid, year = year)
player_stat_result = run_query(player_stats_run_query)
# refactor of data representation
player_stats = []
for arg in player_stat_result[0]:
    player_stats.append(arg)

# creating formula that is used to determine similar players
tmp_arguments = arguments.copy()
formula = generate_arg_query_part(tmp_arguments.pop(0), player_stats.pop(0))
for idx, arg in enumerate(tmp_arguments):
    formula += ' + '
    formula += generate_arg_query_part(arg, player_stats[idx])
# finding the most similar players
score_query = "SELECT guid, first_name ||' ' ||second_name as name, {formula} as coeff FROM player_statistics WHERE year = {year} AND guid != {guid} order by {formula} asc LIMIT {no_of_players}"
score_run_query = score_query.format(formula = formula, year = year, guid = player_guid, no_of_players = number_of_players)
results = run_query(score_run_query)

#print(score_run_query)
#print(results)

# presenting data
result_query = "SELECT first_name ||' ' ||second_name as name, {args}, * FROM player_statistics WHERE year = {year} AND guid = {guid}"
result_player_guids = [player_guid]
# adding guids
for res in results:
    result_player_guids.append(res[0])

final_results = []
for res_player_guid in result_player_guids:
    query = result_query.format(args = args_to_list(arguments), year = year, guid = res_player_guid)
    player_data = run_query(query)
    final_results.append(player_data)

#print(final_results)
df = pd.DataFrame(final_results)
print(df)