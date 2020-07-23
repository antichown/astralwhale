import json
import os
from datetime import datetime, timedelta
from enum import Enum, unique

FILENAME_INTERACTED_USERS = "interacted_users.json"
USER_LAST_INTERACTION = "last_interaction"
USER_FOLLOWING_STATUS = "following_status"


class Storage:
    interacted_users_path = ""
    interacted_users = {}

    def __init__(self, my_username):
        if not os.path.exists(my_username):
            os.makedirs(my_username)
        self.interacted_users_path = my_username + "/" + FILENAME_INTERACTED_USERS
        if os.path.exists(self.interacted_users_path):
            with open(self.interacted_users_path) as json_file:
                self.interacted_users = json.load(json_file)

    def check_user_was_interacted(self, username):
        return not self.interacted_users.get(username) is None

    def check_user_was_interacted_recently(self, username):
        user = self.interacted_users.get(username)
        if user is None:
            return False

        last_interaction = datetime.strptime(user[USER_LAST_INTERACTION], '%Y-%m-%d %H:%M:%S.%f')
        return datetime.now() - last_interaction <= timedelta(days=3)

    def get_following_status(self, username):
        user = self.interacted_users.get(username)
        return user is None and FollowingStatus.NONE or FollowingStatus[user[USER_FOLLOWING_STATUS].upper()]

    def add_interacted_user(self, username, followed=False, unfollowed=False, liked=False):
        user = self.interacted_users.get(username, {})
        user[USER_LAST_INTERACTION] = str(datetime.now())

        if followed:
            user[USER_FOLLOWING_STATUS] = FollowingStatus.FOLLOWED.name.lower()
        elif liked:
            user[USER_FOLLOWING_STATUS] = FollowingStatus.LIKED.name.lower()
        elif unfollowed:
            user[USER_FOLLOWING_STATUS] = FollowingStatus.UNFOLLOWED.name.lower()
        else:
            user[USER_FOLLOWING_STATUS] = FollowingStatus.NONE.name.lower()

        self.interacted_users[username] = user
        self._update_file()

    def _update_file(self):
        with open(self.interacted_users_path, 'w') as outfile:
            json.dump(self.interacted_users, outfile, indent=4, sort_keys=False)


@unique
class FollowingStatus(Enum):
    NONE = 0
    LIKED = 1
    FOLLOWED = 2
    UNFOLLOWED = 3
