import random
import string
import functools


class User:
    def __init__(self, name):
        self.name = name


class SocialGraph:
    def __init__(self):
        self.lastID = 0
        self.users = {}
        self.friendships = {}

    def addFriendship(self, userID, friendID):
        """
        Creates a bi-directional friendship
        """
        if userID == friendID:
            print("WARNING: You cannot be friends with yourself")
        elif friendID in self.friendships[userID] or userID in self.friendships[friendID]:
            print("WARNING: Friendship already exists")
            print(userID, friendID)
        else:
            self.friendships[userID].add(friendID)
            self.friendships[friendID].add(userID)

    def addUser(self, name):
        """
        Create a new user with a sequential integer ID
        """
        self.lastID += 1  # automatically increment the ID to assign the new user
        self.users[self.lastID] = User(name)
        self.friendships[self.lastID] = set()

    def populateGraph(self, numUsers, avgFriendships):
        """
        Takes a number of users and an average number of friendships
        as arguments

        Creates that number of users and a randomly distributed friendships
        between those users.

        The number of users must be greater than the average number of friendships.
        """
        # Reset graph
        self.lastID = 0
        self.users = {}
        self.friendships = {}
        # !!!! IMPLEMENT ME

        # Add users
        for _ in range(numUsers):
            self.addUser(random.choice(string.ascii_uppercase) + ''.join(
                random.choice(string.ascii_lowercase) for i in range(random.randint(1, 9))))

        # Create friendships

        # for i in range(1, len(self.users) - 1):
        #     for _ in range(1, random.randint(0, 2 * avgFriendships) - len(self.friendships[i])):
        #         self.addFriendship(i, random.randint(i + 1, numUsers))

        possible_friendships = [(x, y) for x in self.users.keys()
                                for y in self.users.keys() if x != y and x < y]
        random.shuffle(possible_friendships)
        for i in range((numUsers * avgFriendships) // 2):
            self.addFriendship(
                possible_friendships[i][0], possible_friendships[i][1])

    def getAllSocialPaths(self, userID):
        """
        Takes a user's userID as an argument

        Returns a dictionary containing every user in that user's
        extended network with the shortest friendship path between them.

        The key is the friend's ID and the value is the path.
        """
        visited = {}  # Note that this is a dictionary, not a set
        # !!!! IMPLEMENT ME
        return visited


if __name__ == '__main__':
    sg = SocialGraph()
    sg.populateGraph(10, 2)
    print([(k, v.name) for k, v in sg.users.items()])
    print(sg.friendships)
    connections = sg.getAllSocialPaths(1)
    print(connections)
    print(functools.reduce((lambda x, y: x + y),
                           [len(v) for k, v in sg.friendships.items()]) / 10)
