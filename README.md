Generating Relevant Trending Hashtags for Tweets


Abstract:


Hashtags are a type of labelling tag commonly used on social networks to make it easier for users to find posts aligned with a specific theme. Due to their categorization and searchable nature, hashtags have proven central to social movements in popular culture, politics, and otherwise, allowing users to jointly express sentiment for a particular idea or event. From the concept of hashtags has developed the idea of the “trending hashtag” which signifies the most common hashtags for a given period which commonly align with real-world ideas or events that are popular amongst a social network’s users. As such, these trending hashtags change frequently (weekly, daily, or hourly) to reflect the most popular ideas discussed on a particular social network at a given time. The rise in popularity of the hashtag was largely due to the success of Twitter, a social network that allowed users to publicly express sentiment about anything through a short entry along with categorizing hashtags.


Since trending hashtags change in accordance with trends in the real world, it may often be difficult to realize which trending hashtag a particular tweet should be assigned to or to realize that a trending hashtag applies to a tweet in the first place. In addition, since hashtags are customizable and many similar hashtags often arise around a particular idea or event, many tweets often fall under different hashtags that essentially reflect sentiment for similar ideals. For our project, we are aiming to develop a system that identifies and suggests relevant trending hashtags for a particular tweet that a user has entered. As an example, if a user enters a political tweet about a particular presidential candidate, the system would suggest a relevant currently trending hashtag that the tweet coincides with, if one exists (ie. #electionday). Through suggesting relevant trending hashtags, the system will be able to incorporate more people under the same discussion who otherwise would be categorized differently. In addition, such a system would be able to identify trending hashtags and suggest to users a “correct” hashtag that would better unify users under the same idea.


There are essentially two different, but related, problems in processing a tweet and determining the most relevant trending hashtags: (1) encoding the tweet in a vector representation and (2) using a model to appropriately label the tweet. Work has been done in generating tweet2vec representations (Vosoughi et. al. 2016) and learning vector representations for words in a Tweet; however, because of the constantly-changing trending topics, we would need to be able to perform these embeddings relatively quickly.

