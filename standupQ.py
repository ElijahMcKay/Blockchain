"""
You've been hired to write the software to count the votes for a local election.
Write a function `countVotes` that receives an array of (unique) names, each one
representing a vote for that person. Your function should return the name of the
winner of the election. In the case of a tie, the person whose name comes last
alphabetically wins the election (a dumb rule to be sure, but the voters don't
need to know).
Example:
```
input: ['veronica', 'mary', 'alex', 'james', 'mary', 'michael', 'alex', 'michael'];
expected output: 'michael'
```
Analyze the time and space complexity of your solution.
"""

inputList = ['veronica', 'mary', 'alex', 'james', 'mary', 'michael', 'alex', 'michael']

def voter_count(array):
    winner = 'a'
    hashmap = {}
    votes = 0
    max_votes = []

    for name in array:
        if name not in hashmap:
            hashmap[name] = 1
        else:
            hashmap[name] += 1

        if hashmap[name] > votes:
            max_votes = [name]
            votes = hashmap[name]
            # print('greater than', max_votes)
        elif hashmap[name] == votes:
            max_votes.append(name)
            # print('equals', max_votes)
    
    if len(max_votes) == 1:
        winner = max_votes[0]
    else:
        for name in max_votes:
            if name > winner:
                winner = name

    

    return winner

print(voter_count(inputList))