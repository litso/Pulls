import csv
from error import LambdaError
from github import Github
import io
import keys

class Pulls:
    def __init__(self, token, organization, filter_login, filter_from, filter_to):
        self.g = Github(token) 
        self.organization = organization
        self.filter_login = filter_login
        self.filter_from = filter_from
        self.filter_to = filter_to

    def as_csv(self):
        user = self.__get_user(self.g, self.organization, self.filter_login)

        if user is None:
            raise LambdaError("[BadRequest] Login Not in Organization")

        results = self.__get_pulls(self.g, user.login, self.filter_from, self.filter_to)

        output = io.StringIO()
        writer = csv.DictWriter(output, keys.all(), quoting=csv.QUOTE_NONNUMERIC)
        writer.writeheader()
        writer.writerows(results)

        return output.getvalue()

    def __get_user(self, g, organization, login):
        org = g.get_organization(organization)

        for member in org.get_members():
            if member.login == login:
                return member 
    
    def __get_pulls(self, g, user, filter_from, filter_to):
        issues = g.search_issues(
            f'is:pr author:{user} is:closed created:>{filter_from} merged:<{filter_to}',
            sort='created',
            order='desc'
        )

        results = []

        for issue in issues:
            pr = issue.as_pull_request()
            if pr is None:
                continue

            results.append(
                {
                    keys.CREATED_AT: pr.created_at,
                    keys.PR_NUMBER: pr.number,
                    keys.TITLE: pr.title,
                    keys.URL: pr.html_url
                }
            )
        return results
