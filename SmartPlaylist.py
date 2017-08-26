from moviepy.editor import VideoFileClip
global process
import  os,time, subprocess,random, sys

#get all accepted video files from a directory and its subdirectories
#show path --> string path to a series
#returns a case insensitive sorted list
def get_episodes_sorted(show_path):
    episode_list = []
    for path, subdirs, files in os.walk(show_path):
        for name in files:
            if is_video(name):
                episode_list.append(str(os.path.join(path, name)))
    return sorted(episode_list, key=lambda s: s.lower())


#get all accepted video files from a directory and its subdirectories
#show path --> string path to a series
#returns a randomized list
def get_episodes_unsorted(show_path):
    episode_list = []
    for path, subdirs, files in os.walk(show_path):
        for name in files:
            if is_video(name):
                episode_list.append(str(os.path.join(path, name)))
    random.shuffle(episode_list)
    return  episode_list

#play shows in order
#show path --> list of paths
def play_show_sequential(show_path):
    #start current watch  time timer
    start_time = time.time()
    #get a list of the episodes in order
    episodes = get_episodes_sorted(show_path)
    #name of series info file
    file_name='./episode_info/' + str(os.path.basename(show_path)) + ".txt"
    #episode # and start time
    show_info = get_file_info(file_name,len(episodes))
    #play the show
    play_file(show_info[1],episodes[show_info[0]])
    #update series info file
    write_to_file((int(time.time() - start_time) + show_info[1]),
                  file_name,(int(round(VideoFileClip(episodes[show_info[0]]).duration)) - 5),show_info[0])

#play shows randomly
#show path --> string path to a series
def play_show_random(show_path):
    #get a list of the episodes from show_path
    episodes = get_episodes_unsorted(show_path)
    #start timer
    start_time = time.time()
    #play random episode
    play_file(0,episodes[0])
    #how long is the show approximately
    episode_length = VideoFileClip(episodes[0]).duration -5
    #if we haven't watched the whole show exit the program
    if int(time.time() - start_time) < episode_length:
        exit()

#update a series info file and make any needed directories/files
def write_to_file(watch_time,file_name,episode_length,current_episode):
    if not os.path.isdir("./episode_info"):
        os.mkdir("./episode_info")
    file = open(file_name,"w+")
    if watch_time < episode_length:
        file.write(str(current_episode) + "\n" + str(watch_time))
        file.close()
        exit()
    else:
        current_episode += 1
        file.write(str(current_episode) + "\n" + "0")
        file.close()

#read a file line by line
#returns string list of lines
def file_to_list(file_name):
    file = open(file_name)
    # read the file, line at a time
    lines = file.readlines()
    file.close()
    return lines

#play episodes in order as read in from a file
#file_name --> string path to file to read
def play_sequential_from_file(file_name):
        shows = file_to_list(file_name)
        for show in shows:
            play_show_sequential(show)
        exit()

#play each episode in a list
#list --> string list of paths to episodes
def play_sequential_from_list(list):
    for show in list:
         play_show_sequential(show)
    exit()

##play each episode randomly from a list
#list of shows to play
def play_random_from_list(list):
    for show in list:
        play_show_random(show)
    exit()

#play a media file using mplayer
#start_time --> int time to start the episode in seconds
#show --> string path to media(show)
def play_file(start_time,show):
    subprocess.call(['mplayer', "-ss", str(start_time), '-fs', show])

#get series info
#file_name --> string path to where info file is
#total_episodes --> the number of episode files
#returns list of current episode and episode start time
def get_file_info(file_name,total_episodes):
    if not os.path.isfile(file_name):
        current_episode = 0
        episode_start_time = 0
    else:
        lines = file_to_list(file_name)
        current_episode = int(lines[0])
        episode_start_time = int(lines[1])
        #do we have to start the series over at the beginning
        if current_episode == total_episodes:
            current_episode = 0
    return [current_episode,episode_start_time]

#check if a string ends with an acceptable video file type
def is_video(video):
    if video.lower().endswith(("avi","mkv","mp4","wmv","wm","vob","rm","qt","mpg4","mpeg","mov")):
        return True
    return False

#assuming a television base directory with each show in a subdirectory,
#tv_directory --> string path to a directory containing directories containing media
#returns  all subdirectories of tv_directory alphabetically sorted(case insensitive)
def get_all_shows(tv_directory):
   return sorted( [tv_directory + dI for dI in os.listdir(tv_directory)
                   if os.path.isdir(os.path.join(tv_directory, dI))],key=lambda s: s.lower())



#play x amount of different shows with each show being randomly chosen but played in airing order
#tv_directory --> string path to a directory containing directories containing media
def choose_random_shows_sequential( tv_directory):
    all_shows = get_all_shows(tv_directory)
    random.shuffle(all_shows)
    play_sequential_from_list(all_shows)


#play random shows from a base directory
#tv_directory --> string path to a directory containing directories containing media
def choose_random_shows(tv_directory):
    all_shows = get_all_shows(tv_directory)
    random.shuffle(all_shows)
    play_random_from_list(all_shows)
#get arguments in list form
def get_list_from_args():
    return sys.argv
#play media according to mode
#mode --> int 0-5, how will the medias order be played
#shows --> string list of show paths to be played
def play(mode,shows):
    mode = int(mode)
    #shows in order, episodes in order
    if mode == 0:
        play_sequential_from_list(shows)
    #shows in order, episodes random
    elif mode == 1:
        for x in shows:
            play_show_random(x)
    #shows random, episodes in order
    elif mode == 2:
        random.shuffle(shows)
        play_sequential_from_list(shows)
    #shows random, episodes random
    elif mode == 3:
        random.shuffle(shows)
        play_random_from_list(shows)
    #random shows in order
    elif mode == 4:
        choose_random_shows_sequential(shows)
    #random shows, random episodes
    elif mode == 5:
        choose_random_shows(shows)
    #mode was something other than 0-5
    else:
        #default is 0
        play_sequential_from_list(shows)


"""if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Argument(s) Missing")
        exit(1)
    shows = get_list_from_args()

    shows = shows[1:]
    mode = int(shows.pop())
#    shows = shows[0]
    if mode == 4 or mode == 5 :
        if isinstance(shows,list):
            shows = str(shows[0])
    play(mode, shows)
TODO
- sanitize inputs better
- make / optional for modes 4,5
- make file input an option
- make command line work better
- have exception handling for bad paths or other unexpected behavior
- attach a gui
- allow for custom episode info location
- allow to determine start times for eps and eps to start at
- maybe turn into a class
- make method to generate file to play

"""
#example usage
#modes 0-3
#play(0,["/media/Videos/Television/The Simpsons/","/media/Videos/Television/Archer/","/media/Videos/Television/Futurama/"])
#or
#modes,4,5
#play (5,"/media/Videos/Television/")




