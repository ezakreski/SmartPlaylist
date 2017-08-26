# SmartPlaylist
Simulating a night of television

I made this script to be able to watch episodes of shows without having to literally choose them. I think of it like a night of tv for a certain channel. I put a couple of different modes for the playlist to be generated. 

usage:
-import script or modify original

- play(mode,shows) is the method to use
  
  -mode is the order of the shows/episodes to watch
  -6 different modes to choose from (0-5)
  -default mode is 0
  -mode 0 --> given shows played in given order, episodes played sequentially
  -mode 1 --> given shows played in given order, episodes played randomly
  -mode 2 --> given shows played in random order, episodes played sequentially
  -mode 3 --> given shows played in random order, episodes played randomly
  -mode 4 --> all shows played in random order, episodes played sequentially
  -mode 5 --> all shows played in random order, episodes played randomly
  
  shows is a list of directories of tv series
  -at least 1 directory is needed for modes 0-3, only 1 is needed for modes 4,5. if more than 1 is supplied then the first is used

example usage:
*modes 0-3 must be in list form, modes 4,5 can also work as strings*
play(0,["/path/to/tv/showA","/path/to/tv/showB/","/path/to/tv/showC"])
*The trailing slash is REQUIRED for modes 4,5 but optional for all other modes*
play(4,["/path/to/tv/"]) or play(5,'/path/to/tv/')


Assumptions/Requirements:
-Television directory structure is assumed to be organized in the following fashion:
  each series can be organized in one of the following ways
  /home/user/TV/SeriesName/Season#/Episode
  /home/user/TV/SeriesName/Season#/EpisodeDir/episode
  /home/user/TV/SeriesName/Episode

-Episode/Season naming schemes need to be alphabetizable for a computer( not case sensitive though)
    eg "Season 1" is bad, "Season 01" is good
        "show.ep1" is bad, "show.ep01" is good  
    -consistency in a naming scheme is key otherwise you can have unexpected playing orders

-mplayer must be installed





