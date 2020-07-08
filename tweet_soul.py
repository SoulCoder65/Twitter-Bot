import tweepy
import tweepy.cursor
import datetime
from tkinter import *
from tkinter.ttk import *
from PIL import ImageTk,Image
import itertools
from tkinter import messagebox
import time

access_token=#Place accesstoken here
access_token_secret=#Place accesstoken_secret here
consumer_key=#Place consumer_key here
consumer_secret=#Place consumer_secret here
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth,wait_on_rate_limit=True,wait_on_rate_limit_notify=True)


def paginate(iterable, page_size):
    while True:
        i1, i2 = itertools.tee(iterable)
        iterable, page = (itertools.islice(i1, page_size, None),
                list(itertools.islice(i2, page_size)))
        if len(page) == 0:
            break
        yield page


def read_tweets():
    no_tweets = int(no_of_tweets_var.get())
    global result_field_new
    global new_window
    new_window = Toplevel(window_screen)
    new_window.title("Bot Result")
    new_window.geometry("600x450")

    result_field_new = Text(new_window)
    result_field_new.pack()
    result_field_new.config(background='#e8ead3',foreground='#654062',font=("Courier", 13, "bold")
)
    exit_btn = Button(new_window, text="Exit", command=exit_new_window)
    exit_btn.pack()
    for tweets in tweepy.Cursor(api.home_timeline).items(no_tweets):
        char_list = [tweets.text[j] for j in range(len(tweets.text)) if ord(tweets.text[j]) in range(65536)]
        tweet = ''
        for j in char_list:
            tweet = tweet + j

        result_field_new.insert(END,f"\n {tweets.user.name} said: {tweet}")





def check_followers():
    name=name_of_user_var.get()
    global result_field_new
    global new_window
    new_window = Toplevel(window_screen)
    new_window.title("Bot Result")
    new_window.geometry("600x450")

    result_field_new = Text(new_window)
    result_field_new.pack()
    exit_btn = Button(new_window, text="Exit", command=exit_new_window)
    exit_btn.pack()
    result_field_new.config(background='#e8ead3',foreground='#654062',font=("Courier", 13, "bold"))

    count_followers=0

    followers = api.followers_ids(f"@{name}")

    result_field_new.insert(END,"***************Followers List***********************\n")


    for page in paginate(followers, 100):
        results = api.lookup_users(user_ids=page)

        for result in results:
            count_followers += 1
            print(result.screen_name)
            result_field_new.insert(END,result.screen_name+"\n")
    result_field_new.insert(END, f"\nTotal Follwers {count_followers}\n\n")

    # Following
    count_following = 0
    following = api.friends_ids(f"@{name}")
    result_field_new.insert(END,"\n\n***************Following List***********************\n")
    for page in paginate(following, 100):
        results = api.lookup_users(user_ids=page)

        for result in results:
            count_following += 1
            result_field_new.insert(END,result.screen_name+"\n")
    result_field_new.insert(END, f"\nTotal Follwing {count_following}")

def user_details():
    name = user_details_var.get()
    global result_field_new
    global new_window
    new_window = Toplevel(window_screen)
    new_window.title("Bot Result")
    new_window.geometry("600x450")

    result_field_new = Text(new_window)
    result_field_new.pack()
    exit_btn = Button(new_window, text="Exit", command=exit_new_window)
    exit_btn.pack()
    result_field_new.config(background='#e8ead3', foreground='#654062', font=("Courier", 13, "bold"))
    user=api.get_user(name)

    result_field_new.insert(END,f'''
        *****Details of User*****
    Screen Name :- {user.name}
    User Id :- {user.id_str}
    Bio :- {user.description}
    Account was created on :- {user.created_at}
    Days to create account :- {datetime.datetime.now()-user.created_at}
    Followers count :- {user.followers_count}
    Following  count :- {user.friends_count}
    No. of tweets :- {user.statuses_count}
    No. of liked tweets :- {user.favourites_count}
    verified or not :- {user.verified}
    
        ''')

#DONE
def like_tweets():
    try:
        no_tweet=int(like_tweet_no_text.get())
        global result_field_new
        global new_window
        new_window = Toplevel(window_screen)
        new_window.title("Bot Result")
        new_window.geometry("600x450")

        result_field_new = Text(new_window)
        result_field_new.pack()
        exit_btn = Button(new_window, text="Exit", command=exit_new_window)
        exit_btn.pack()
        result_field_new.config(background='#e8ead3', foreground='#654062', font=("Courier", 13, "bold"))
        tweets=api.home_timeline(count=no_tweet)
        count_tweet=0
        for tweet in tweets:
            api.create_favorite(tweet.id)
            count_tweet+=1
            result_field_new.insert(END, f"Liking tweet {tweet.id} of {tweet.author.name}\n")
        new_window.mainloop()
    except tweepy.TweepError as e:
        result_field_new.insert(END, f"Only {count_tweet} new tweets!! ")
def blocked_users():
    global result_field_new
    global new_window
    new_window = Toplevel(window_screen)
    new_window.title("Bot Result")
    new_window.geometry("600x450")

    result_field_new = Text(new_window)
    result_field_new.pack()
    exit_btn = Button(new_window, text="Exit", command=exit_new_window)
    exit_btn.pack()
    result_field_new.config(background='#e8ead3', foreground='#654062', font=("Courier", 13, "bold"))
    result_field_new.insert(END,"*************Blocked List*************\n")
    if api.blocks():
        for block in api.blocks():
            result_field_new.insert(END, block.name+"\n")
    else:
        result_field_new.insert(END," No block User found\n")
def search_tweets():
    search_query=search_tweet_var.get()
    global result_field_new
    global new_window
    new_window = Toplevel(window_screen)
    new_window.title("Bot Result")
    new_window.geometry("600x450")

    result_field_new = Text(new_window)
    result_field_new.pack()
    exit_btn = Button(new_window, text="Exit", command=exit_new_window)
    exit_btn.pack()
    result_field_new.config(background='#e8ead3', foreground='#654062', font=("Courier", 13, "bold"))
    try:
        for tweets in api.search(q=search_query,lang="en",rpp=10):
            char_list = [tweets.text[j] for j in range(len(tweets.text)) if ord(tweets.text[j]) in range(65536)]
            tweet = ''
            for j in char_list:
                tweet = tweet + j
            print(f"{tweets.user.name} : {tweet}")
            result_field_new.insert(END, f"{tweets.user.name} : {tweet}\n\n")
    except Exception as e:
        pass

#DONE
def find_trends():
    global result_field_new
    global new_window
    new_window = Toplevel(window_screen)
    new_window.title("Bot Result")
    new_window.geometry("600x450")

    result_field_new = Text(new_window)
    result_field_new.pack()
    exit_btn = Button(new_window, text="Exit", command=exit_new_window)
    exit_btn.pack()
    result_field_new.config(background='#e8ead3', foreground='#654062', font=("Courier", 13, "bold"))
    trends=api.trends_place(1)
    result_field_new.insert(END, "**************Trends Across World**********\n")
    for trend in trends[0]["trends"]:
        result_field_new.insert(END,trend["name"]+"\n")
def mention_tweet():
    tweets=api.mentions_timeline()
    for tweet in tweets:
        tweet.favorite()

        tweet.user.follow()
# DONE

def do_tweet():
    message=do_tweet_var.get()
    api.update_status(message)
    time.sleep(2)
    messagebox.showinfo("Tweeted","Tweet Post Successfully!!!")

# DONE

def follow_user():
    try:
        username=follow_user_var.get()
        api.create_friendship(f"@{username}")
        time.sleep(2)
        messagebox.showinfo("Done",f"Start Following {username} ")
    except tweepy.TweepError as e:
        messagebox.showwarning("Not Found!!",f"No user Found named {username}")
# DONE

def update_profile_bio():
    description=new_profile_bio_text.get()
    api.update_profile(description=description)
    messagebox.showinfo("Updated!!","Profile Bio Updated")

# DONE
def update_profile_name():
    name=new_profile_name_text.get()
    api.update_profile(name)
    messagebox.showinfo("Updated!!","Profile Name Updated")

# GUI


def clear_entry(event, entry):
    entry.delete(0, END)
def exit_new_window():
    window_screen.forget(new_window)


window_screen=Tk()
window_screen.title("Twitter Bot By Akshay")
window_screen.geometry("1100x650")
window_screen.config(bg='#5b8c85')
logo_img=ImageTk.PhotoImage(Image.open("images/twittlogo.png"))
logo_label=Label(window_screen,image=logo_img)
logo_label.grid(row=0,column=0,padx=400,pady=15)
logo_label.config(background='#5b8c85')

#VARIABLES
no_of_tweets_var=StringVar()
name_of_user_var=StringVar()
user_details_var=StringVar()
result_field_text=StringVar()
like_tweet_no_text=StringVar()
new_profile_name_text=StringVar()
new_profile_bio_text=StringVar()
search_tweet_var=StringVar()
do_tweet_var=StringVar()
follow_user_var=StringVar()
style=Style()

#FONT
font=("Courier", 29, "italic")
style.configure('TButton', font =
               ('calibri', 10, 'bold',),
                foreground = '#3b6978',background='#f7f5dd',activeforeground='green',activebackground='red', borderwidth = '4')
style.configure('TEntry',foreground='#900c3f')

style.configure('TLabel', background='#5b8c85',foreground='#2f2519',font=("Courier", 13, "bold")
)

#inputfield

optionsFrame=Label(window_screen)
optionsFrame.grid(row=1,column=0,sticky="w")
optionsFrame.config(background='#5b8c85')

read_tweetLabel=Label(optionsFrame,text="Read Tweets")
read_tweetLabel.grid(row=0,column=0,padx=30)
read_tweets_entry=Entry(optionsFrame,width=30,textvariable=no_of_tweets_var)
read_tweets_entry.insert(0,"No.of Tweets-")
read_tweets_entry.grid(row=1,column=0,padx=30)
read_tweets_entry.bind("<Button-1>", lambda event: clear_entry(event, read_tweets_entry))
read_tweets_btn=Button(optionsFrame,text="Read Tweets",command=read_tweets)
read_tweets_btn.grid(row=2,column=0,padx=30,pady=15)

check_followersLabel=Label(optionsFrame,text="Check Followers/Following of User")
check_followersLabel.grid(row=0,column=1,padx=30)
check_followers_entry=Entry(optionsFrame,width=30,textvariable=name_of_user_var)
check_followers_entry.insert(0,"Name of user without @")
check_followers_entry.grid(row=1,column=1,padx=30)
check_followers_entry.bind("<Button-1>", lambda event: clear_entry(event, check_followers_entry))
check_followers_btn=Button(optionsFrame,text="Show list",command=check_followers)
check_followers_btn.grid(row=2,column=1,padx=30,pady=15)

do_tweetsLabel=Label(optionsFrame,text="Write Tweet")
do_tweetsLabel.grid(row=0,column=2,padx=30)
do_tweets_entry=Entry(optionsFrame,width=30,textvariable=do_tweet_var)
do_tweets_entry.insert(0,"Enter Tweet..")
do_tweets_entry.grid(row=1,column=2,padx=30)
do_tweets_entry.bind("<Button-1>", lambda event: clear_entry(event, do_tweets_entry))
do_tweets_btn=Button(optionsFrame,text="tweet",command=do_tweet)
do_tweets_btn.grid(row=2,column=2,padx=30)

user_detailsLabel=Label(optionsFrame,text="Get Details Of User")
user_detailsLabel.grid(row=3,column=0,padx=30)
user_details_entry=Entry(optionsFrame,width=30,textvariable=user_details_var)
user_details_entry.insert(0,"Name of user-")
user_details_entry.grid(row=4,column=0,padx=30)
user_details_entry.bind("<Button-1>", lambda event: clear_entry(event, user_details_entry))
user_details_btn=Button(optionsFrame,text="Get Details",command=user_details)
user_details_btn.grid(row=5,column=0,padx=30,pady=15)


like_tweetsLabel=Label(optionsFrame,text="Like tweets from your timeline")
like_tweetsLabel.grid(row=3,column=1,padx=30)
like_tweets_entry=Entry(optionsFrame,width=30,textvariable=like_tweet_no_text)
like_tweets_entry.insert(0,"No. of Tweets")
like_tweets_entry.grid(row=4,column=1,padx=30)
like_tweets_entry.bind("<Button-1>", lambda event: clear_entry(event, like_tweets_entry))
like_tweets_btn=Button(optionsFrame,text="Like Tweets",command=like_tweets)
like_tweets_btn.grid(row=5,column=1,padx=30,pady=15)

update_profile_nameLabel=Label(optionsFrame,text="Update Profile Name")
update_profile_nameLabel.grid(row=3,column=2,padx=30)
update_profile_name_entry=Entry(optionsFrame,width=30,textvariable=new_profile_name_text)
update_profile_name_entry.insert(0,"New Name")
update_profile_name_entry.grid(row=4,column=2,padx=30)
update_profile_name_entry.bind("<Button-1>", lambda event: clear_entry(event, update_profile_name_entry))
update_profile_name_btn=Button(optionsFrame,text="Update Name",command=update_profile_name)
update_profile_name_btn.grid(row=5,column=2,padx=30,pady=15)

search_tweetsLabel=Label(optionsFrame,text="Search Tweets by Keyword")
search_tweetsLabel.grid(row=6,column=0,padx=30)
search_tweets_entry=Entry(optionsFrame,width=30,textvariable=search_tweet_var)
search_tweets_entry.insert(0,"Key Word...")
search_tweets_entry.grid(row=7,column=0,padx=30)
search_tweets_entry.bind("<Button-1>", lambda event: clear_entry(event, search_tweets_entry))
search_tweets_btn=Button(optionsFrame,text="Search Tweets",command=search_tweets)
search_tweets_btn.grid(row=8,column=0,padx=30)

follow_userLabel=Label(optionsFrame,text="Follow User")
follow_userLabel.grid(row=6,column=1,padx=30)
follow_user_entry=Entry(optionsFrame,width=30,textvariable=follow_user_var)
follow_user_entry.insert(0,"Name of user without @-")
follow_user_entry.grid(row=7,column=1,padx=30)
follow_user_entry.bind("<Button-1>", lambda event: clear_entry(event, follow_user_entry))
follow_user_btn=Button(optionsFrame,text="Follow",command=follow_user)
follow_user_btn.grid(row=8,column=1,padx=30)

update_profile_bioLabel=Label(optionsFrame,text="Update Profile Bio")
update_profile_bioLabel.grid(row=6,column=2,padx=30)
update_profile_bio_entry=Entry(optionsFrame,width=30,textvariable=new_profile_bio_text)
update_profile_bio_entry.insert(0,"New Bio")
update_profile_bio_entry.grid(row=7,column=2,padx=30)
update_profile_bio_entry.bind("<Button-1>", lambda event: clear_entry(event, update_profile_bio_entry))
update_profile_bio_btn=Button(optionsFrame,text="Update Bio",command=update_profile_bio)
update_profile_bio_btn.grid(row=8,column=2,padx=30,pady=15)

find_trendLabel=Label(optionsFrame,text="Find Trends across the world")
find_trendLabel.grid(row=9,column=0,padx=30)
find_trend_btn=Button(optionsFrame,text="Find",command=find_trends)
find_trend_btn.grid(row=10,column=0,padx=30,pady=15)

show_blocked_userLabel=Label(optionsFrame,text="Show Blocked Users")
show_blocked_userLabel.grid(row=9,column=1,padx=30)
show_blocked_user_btn=Button(optionsFrame,text="Show",command=blocked_users)
show_blocked_user_btn.grid(row=10,column=1,padx=30,pady=15)
window_screen.mainloop()