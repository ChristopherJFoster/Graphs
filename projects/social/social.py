import random
import string
import collections


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

        # O(n^2) time:
        # possible_friendships = [(x, y) for x in self.users.keys()
        #                         for y in self.users.keys() if x != y and x < y]
        # random.shuffle(possible_friendships)
        # for i in range((numUsers * avgFriendships) // 2):
        #     self.addFriendship(
        #         possible_friendships[i][0], possible_friendships[i][1])

        # O(n) time:
        for i in range(1, len(self.users)):
            for _ in range(1, min(random.randint(0, 2 * avgFriendships) - len(self.friendships[i]), len(self.users) - i)):
                new_friend = random.randint(i + 1, numUsers)
                while new_friend in self.friendships[i]:
                    new_friend = random.randint(i + 1, numUsers)
                self.addFriendship(i, new_friend)

    def getAllSocialPaths(self, userID):
        """
        Takes a user's userID as an argument

        Returns a dictionary containing every user in that user's
        extended network with the shortest friendship path between them.

        The key is the friend's ID and the value is the path.
        """
        # !!!! IMPLEMENT ME
        visited, queue = {userID: [userID]}, collections.deque([userID])
        while queue:
            current_friend = queue.popleft()
            for next_friend in self.friendships[current_friend]:
                if next_friend not in visited:
                    path = list(visited[current_friend])
                    path.append(next_friend)
                    visited[next_friend] = path
                    queue.append(next_friend)
        return visited

    def avg_network(self, degrees=float('inf')):
        avg_num_friends = 0
        connected_friends = 0
        avg_path_len = 0

        for user in self.users:
            avg_num_friends += len(self.friendships[user])
            paths = self.getAllSocialPaths(user)
            path_lengths = 0
            for path in paths.values():
                if len(path) > 1 and len(path) <= degrees + 1:
                    path_lengths += len(path) - 1
                    connected_friends += 1
            avg_path_len += path_lengths / len(paths)

        result = (f'''Average number of friends: {avg_num_friends / len(self.users)}\n\n'''
                  f'''Average size of extended network (up to {degrees} degrees of separation): {connected_friends / len(self.users)} out of {len(self.users)} users.\n\n'''
                  f'''Average degrees of separation between friends in extended network: {avg_path_len / (connected_friends / len(self.users))}\n''')

        return result

    def list_names(self):
        result = '\n' + \
            ', '.join([user.name for user in self.users.values()]) + '\n'
        return result


if __name__ == '__main__':
    sg = SocialGraph()
    sg.populateGraph(1000, 5)
    print(sg.list_names())
    print(sg.avg_network(2))
