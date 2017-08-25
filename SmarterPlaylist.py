from moviepy.editor import VideoFileClip
global process
import  os,time, subprocess,random, sys
#TODO
#args
    #folders to play, quoted and space separated eg "/home/name/TV/TheSimpsons" "C://I/think/this/is/how/windows/works"
        # if using mode 4 or 5 make sure to include a closing slash eg "/home/name/TV/",
#           also only include 1 directory   with or without is fine for other modes
    #mode (0-5)

    #example usage
            #play episodes sequentially with series order chosen randomly for the simpsons, family guy, and futurama
    #./SmarterPlaylist.py ""/home/name/TV/TheSimpsons" "/home/name/TV/Futurama/" "/home/name/TV/Family Guy/" 3
            #play a random episode of a random show
    #./SmarterPlaylist.py ""/home/name/TV/" 5

def get_episodes_sorted(show_path):
    episode_list = []
    for path, subdirs, files in os.walk(show_path):
        for name in files:
            if is_video(name):
                episode_list.append(str(os.path.join(path, name)))
    return sorted(episode_list, key=lambda s: s.lower())


def get_episodes_unsorted(show_path):
    episode_list = []
    for path, subdirs, files in os.walk(show_path):
        for name in files:
            if is_video(name):
                episode_list.append(str(os.path.join(path, name)))
    random.shuffle(episode_list)
    return  episode_list


def play_show_sequential(show_path):
    start_time = time.time()
    episodes = get_episodes_sorted(show_path)
    file_name='./episode_info/' + str(os.path.basename(show_path)) + ".txt"
    show_info = get_file_info(file_name,len(episodes))
    #ep = int(round(VideoFileClip(show_info[0]).duration)) - 5
  #  print("ep = " + str(int(round(VideoFileClip(show_info[0]).duration)) - 5))
    play_file(show_info[1],episodes[show_info[0]])
    #subprocess.call(['mplayer', "-ss", str(start_time), '-fs', show_info[0]])
    print("hery eheh")
    write_to_file((int(time.time() - start_time) + show_info[1]),
                  file_name,(int(round(VideoFileClip(episodes[show_info[0]]).duration)) - 5),show_info[0])


def play_show_random(show_path):
    episodes = get_episodes_unsorted(show_path)
    start_time = time.time()
    play_file(0,episodes[0])
    episode_length = VideoFileClip(episodes[0]).duration -5
    if int(time.time() - start_time) < episode_length:
        exit()


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


def file_to_list(file_name):
    file = open(file_name)
    # read the file, line at a time
    lines = file.readlines()
    file.close()
    return lines


def play_sequential_from_file(file_name):
        shows = file_to_list(file_name)
        for show in shows:
            play_show_sequential(show)
        exit()


def play_sequential_from_list(list):
    for show in list:
         play_show_sequential(show)
    exit()


def play_random_from_list(list):
    for show in list:
        play_show_random(show)
    exit()


def play_file(start_time,show):
    subprocess.call(['mplayer', "-ss", str(start_time), '-fs', show])


def get_file_info(file_name,total_episodes):
    if not os.path.isfile(file_name):
        current_episode = 0
        episode_start_time = 0
    else:
        lines = file_to_list(file_name)
        current_episode = int(lines[0])
        episode_start_time = int(lines[1])
        if current_episode == total_episodes:
            current_episode = 0
    return [current_episode,episode_start_time]


def is_video(video):
    if video.lower().endswith(("avi","mkv","mp4","wmv","wm","vob","rm","qt","mpg4","mpeg","mov")):
        return True
    return False

#assuming a television base directory with each show in a subdirectory, return paths for all shows
def get_all_shows(tv_directory):
   return sorted( [tv_directory + dI for dI in os.listdir(tv_directory)
                   if os.path.isdir(os.path.join(tv_directory, dI))],key=lambda s: s.lower())



#play x amount of different shows with each show being randomly chosen but played in airing order
def choose_random_shows_sequential( tv_directory):
    all_shows = get_all_shows(tv_directory)
    random.shuffle(all_shows)
    play_sequential_from_list(all_shows)


#play x amount of random shows
def choose_random_shows(tv_directory):
    all_shows = get_all_shows(tv_directory)
    random.shuffle(all_shows)
    play_random_from_list(all_shows)

def get_list_from_args():
    return sys.argv

def play(mode,shows):
    mode = int(mode)
    #shows in order, episodes in order
    if mode == 0:
        play_sequential_from_list(shows)
    #shows in order, episodes random
    if mode == 1:
        for x in shows:
            play_show_random(x)
    #shows random, episodes i order
    if mode == 2:
        random.shuffle(shows)
        play_sequential_from_list(shows)
    #shows random, episodes random
    if mode == 3:
        random.shuffle(shows)
        play_random_from_list(shows)
    #random shows in order
    if mode == 4:
        choose_random_shows_sequential(shows)
    if mode == 5:
        choose_random_shows(shows)

#TODO
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
    play(mode, shows)"""

#example usage
#modes 0-3
#play(0,["/media/Storage/Toshiba/Videos/Television/The Simpsons/","/media/Storage/Toshiba/Videos/Television/Archer/","/media/Storage/Toshiba/Videos/Television/Futurama/"])
#or
#modes,4,5
#play (5,"/media/Storage/Toshiba/Videos/Television/")




