# The purpose of this function is to favorite a tweet based on a hashtag search
# Hashtag is provided by the user
import tweepy
import credentials

# Get the results from the Twitter API
def get_tweets(a):
    return list( tweepy.Cursor(credentials.api.search, q=a, result_type='recent', include_rts = False, exclude_replies = True).items(15) )

# Return only the tweets that came from the API
def get_all_the_tweets(b):
    print("----------\n")

    for each_tweet in b:
        print("> " + strip_tweet(each_tweet) + "\n")

    print("----------\n")
    
# Have the tweet encoded in utf-8 for any weird characters
# Strip the tweet of unnecessary characters
# Return said tweet
def strip_tweet(c):
    original_tweet = str(c.text.encode('utf-8') )
    original_tweet = original_tweet.replace("b\'", "\'")
    original_tweet = original_tweet.replace("b\"", "\"")
    return original_tweet
        
# Favorite the tweet
# Unless it already has been, then have the user choose to unfavorite or not
def favorite_all_the_tweets(d):
    
    for tweet in d:
        
        try:
            tweet.favorite()
            print("\n----------FAVORITED----------\n")
            print(strip_tweet(tweet) + ".")

        except tweepy.TweepError as e:
            if(e.reason == "[{'message': 'You have already favorited this status.', 'code': 139}]"):
                print("\n----------ERROR----------\n")
                print("The tweet, " + strip_tweet(tweet) + ", has already been favorited!\n")

                continue_to_unfavorite = input("Would you like to unfollow this tweet? (y/n): ").lower()

                if continue_to_unfavorite == 'y' or continue_to_unfavorite == 'yes':
                    credentials.api.destroy_favorite(tweet.id)

                    print("\nYou have successfully unfavorited the tweet.")
                else:
                    print("\nOkie doke. We'll let you keep the tweet favorited for now.\n")

# Initiate a hashtag counter
tweet_count = 0

# Declare the hashtag symbol as unicode
hashtag_symbol = "%23"

# Prompt the user for input
hashtag_keyword = input("\nWhat is the hashtag you'd like to search for? No need to include the '#' key: ").lower()

# Combine the hashtag unicode and keyword
hashtag_search = hashtag_symbol + hashtag_keyword

search_results = get_tweets(hashtag_search)

for ticker in search_results:
    tweet_count += 1

if tweet_count == 0:
    print("\nThere are " + str(tweet_count) + " tweets containing the hashtag: '" + hashtag_keyword + "'.\n")
elif tweet_count == 1:
    print("\nThere is " + str(tweet_count) + " tweet containing the hashtag: '" + hashtag_keyword + "'.\n")

    print("Here is the tweet:\n")

    get_all_the_tweets(search_results)

else:
    print("\nThere are " + str(tweet_count) + " tweets containing the hashtag: '" + hashtag_keyword + "'.\n")

    print("Here are the tweets:\n")

    get_all_the_tweets(search_results)

if(tweet_count > 0):

    continue_to_favorite = input("Would you like to favorite the tweet(s)? (y/n): ").lower()
    
    if(continue_to_favorite == 'y' or continue_to_favorite == 'yes'):
        favorite_all_the_tweets(search_results)
