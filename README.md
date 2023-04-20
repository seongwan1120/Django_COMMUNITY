# Project: Community

## Concept
* A board containing posts and comments with re-comments in it.
* It may have the functions such as agree, disagree, block, search and so on.
* People can recognize whether some articles or comments are revised by checking a mark saying 'revised' next to the content.
* Profile page shows the list of the profile user's post, recommend, decommend, followings, block and any commentaries.
---
## Modeling
* User
    * posting_best: ManytoManyField(Posting)
    * postings_worst: ManytoManyField(Posting)
    * comments_agree: ManytoManyField(Comment)
    * comments_disagree: ManytoManyField(Comment)
    * followings: ManytoManyField(self)
* Posting
    * author: ForeignKey(User)
    * created_at: DateTimeField
    * updated_at: DateTimeField
    * title: CharField(50)
    * content: TextField
* Comment
    * author: ForeignKey(User)
    * created_at: DateTimeField
    * updated_at: DateTimeField
    * content: TextField
    * posting: ForeignKey(Posting) 
* Reply
    * author: ForeignKey(User)
    * created_at: DateTimeField
    * updated_at: DateTimeField
    * content: TextField
    * comment: ForeignKey(Comment) 
---
## Plan to make

* ### Day 1: Modeling, filling in settings.py, urls.py, etc.
* ### Day 2: Making views.py and html files.
* ### Day 3: Completing this project by using bootstrap.
----
## Results
### Failed in making functions including 
1. a list of comments and replies.
2. lists of recommendation and decommendation.
3. a list of followings.
4. a list of blocks and block() in views.py.
5. Another board for best recommended articles.
6. updating comments and replies.
7. a mark showing 'revised'.
8. filter for articles based on the date in last 7 days.

### Need to know
1. Using some APIs.
2. Oauth2.0
3. Editor