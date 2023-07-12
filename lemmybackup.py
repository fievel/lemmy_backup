import plemmy
import os
import json
import sys
import logging
import io

class NullOutput(io.IOBase):
    def write(self, line):
        pass

class LemmyReader:
    def __init__(self, instanceUrl, login, password):
        self.__login = login
        self.__srv = plemmy.LemmyHttp(instanceUrl)
        self.__srv.login(login, password)

    def GetSubscribedCommunities(self):
        myCommunities = []
        currentPage = 1
        BY_PAGE_LIMIT = 50
        fetchedItems = BY_PAGE_LIMIT
        while fetchedItems == BY_PAGE_LIMIT:
            api_resp = self.__srv.list_communities(limit=BY_PAGE_LIMIT, page=currentPage, type_="Subscribed")
            communityList = plemmy.responses.ListCommunitiesResponse(api_resp)

            fetchedItems = len(communityList.communities)
            currentPage += 1

            for c in communityList.communities:
                myCommunities.append(c.community)

        return myCommunities

    def GetProfile(self):
        apiResp = self.__srv.get_person_details(username=self.__login)
        apiRespJson = apiResp.json()
        personView = plemmy.views.PersonView(apiRespJson["person_view"])
        return personView.person

def getArgParser():
    import argparse

    parser = argparse.ArgumentParser(description="Allows to backup various lemmy data, like subscribed communities. "
                                     "Output on stdout in human-readable format. "
                                     "Use --export option to generate a json file.")
    
    parser.add_argument("instance",
                        help="Lemmy instance url (i.e. https://lemmy.ml)",
                        action='store',
                        type=str)

    parser.add_argument("username",
                        help="Lemmy username",
                        action='store',
                        type=str)

    parser.add_argument("password",
                        help="Lemmy password",
                        action='store',
                        type=str)

    parser.add_argument("-e", "--export",
                        help="Export data to file. Location must be write-able.",
                        action='store',
                        type=str)

    parser.add_argument("-q", "--quiet",
                        help="Do not output on console",
                        action="store_true")

    backup_data_group = parser.add_argument_group("Backup Data", "Data to backup (if none specified, all will be saved)")
    backup_data_group.add_argument("--communities",
                        help="Backup subscribed communities",
                        action='store_true')

    backup_data_group.add_argument("--profile",
                        help="Backup profile data (bio)",
                        action='store_true')

    return parser


def main():
    args = getArgParser().parse_args()

    if not args.communities and not args.profile:
        args.communities = True
        args.profile = True

    ostrm = sys.stdout if not args.quiet else NullOutput()


    backupData = dict()

    try:
        lr = LemmyReader(args.instance, args.username, args.password)
    except:
        logging.error("Cannot connect to Lemmy, check your credentials and instance URL")
        sys.exit(1)

    if args.profile:
        profile = lr.GetProfile()

        backupData["profile"] = {"name": profile.name, "bio": profile.bio}

        print("\nCurrent user:", file=ostrm)
        print("-------------", file=ostrm)
        print("Login: {login}".format(login=profile.name), file=ostrm)
        print("\nBio:\n", file=ostrm)
        print(profile.bio, file=ostrm)

    if args.communities:
        communities = lr.GetSubscribedCommunities()

        backupData["communities"] = []

        print("\nSubscribed Communities:", file=ostrm)
        print("-----------------------", file=ostrm)
        HDR = "{title:^40.40} | {id:^7} | {url:^40}".format(title="TITLE", id="ID", url="URL")
        FMT = "{title:40.40} | {id:>7} | {url:40}"
        print(HDR, file=ostrm)
        for c in communities:
            backupData["communities"].append({"id": c.id, "actor_id": c.actor_id, "title": c.title})
            print(FMT.format(id=c.id, url=c.actor_id, title=c.title), file=ostrm)

    if args.export:
        with open(args.export, "w") as exportFile:
            json.dump(backupData, exportFile)

if __name__ == "__main__":
    main()
