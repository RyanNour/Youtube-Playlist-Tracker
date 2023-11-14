import smtplib
from email.message import EmailMessage
from datetime import datetime
import sys
import requests


# ////////////////global variables///////////////////////////

api_key = "ENTER KEY HERE"     

# ///////////////auxilairy functions////////////////////////

def print_video_info(video):            #function that prints info about video to console

    if "videoOwnerChannelTitle" in video["snippet"]:
        print(str(video["snippet"]["position"]+1) + ". " + video["snippet"]["title"] + "\n\t channel:" 
                    + video["snippet"]["videoOwnerChannelTitle"] + "\t video id:" + video["snippet"]["resourceId"]["videoId"] + "\n")
    
    else:
        print(str(video["snippet"]["position"]+1) + ". " + video["snippet"]["title"]
                    + "\n\t video id:" + video["snippet"]["resourceId"]["videoId"] + "\n")

def string_video_info(video):           #function that returns string with info about video

    if "videoOwnerChannelTitle" in video["snippet"]:
        return (str(video["snippet"]["position"]+1) + ". " + video["snippet"]["title"] + "\n\t channel:" 
                    + video["snippet"]["videoOwnerChannelTitle"] + "\t video id:" + video["snippet"]["resourceId"]["videoId"] + "\n")
    
    else:
        return (str(video["snippet"]["position"]+1) + ". " + video["snippet"]["title"]
                    + "\n\t video id:" + video["snippet"]["resourceId"]["videoId"] + "\n")


def get_channel_playlists(channel_id):      #function that returns list of all playlists made by channel with provided id

    playlists = []
    
    response = requests.get("https://youtube.googleapis.com/youtube/v3/playlists?part=id&channelId=" + channel_id + "&maxResults=50&key=" + api_key)

    if response.status_code  >= 300:                    #Handle errors from api
        print("an error has occured while accessing YT API, error code: " + str(response.status_code))
        print(response.json())
        sys.exit(1)

    for playlist in response.json()["items"]:
        playlists.append(playlist["id"])
    
    return playlists


# //////////////////////main/////////////////////////

playlist_list = get_channel_playlists("ENTER CHANNEL ID HERE")               #Get list of playlists from main channel

now = datetime.now()
dt_string = now.strftime("%d.%m.%Y %H %M %S")       #String containing current time

output = open("YT playlist backup " + dt_string + ".txt", "w",encoding='utf-8') #Create output file

for playlist in playlist_list:

        playlist_response = requests.get("https://youtube.googleapis.com/youtube/v3/playlists?part=snippet&id=" + playlist + "&maxResults=50&key=" + api_key)       #get the name of the playlist

        if playlist_response.status_code  >= 300:                    #Handle errors from api
            print("an error has occured while accessing YT API, error code: " + str(playlist_response.status_code))
            print(response.json())
            sys.exit(1)
        
        
        print("playlist: " + playlist + "\t\tplaylist name: " + playlist_response.json()["items"][0]["snippet"]["title"] +"\n")
        output.write("playlist: " + playlist + "\t\tplaylist name: " + playlist_response.json()["items"][0]["snippet"]["title"] +"\n\n")    #save the name to the file

        response = requests.get("https://youtube.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=50&playlistId=" + playlist + "&key=" + api_key)    #get the list of songs

        if response.status_code  >= 300:                    #Handle errors from api
            print("an error has occured while accessing YT API, error code: " + str(response.status_code))
            print(response.json())
            sys.exit(1)
        
        
        for movie in response.json()["items"]:                  #write video info to file
            #print_video_info(movie)
            output.write(string_video_info(movie) + "\n")

        while "nextPageToken" in response.json():               #repeat until there are more pages with videos

            response = requests.get("https://youtube.googleapis.com/youtube/v3/playlistItems?part=snippet&maxResults=50&pageToken="
                                                 + response.json()["nextPageToken"] + "&playlistId=" + playlist + "&key=" + api_key)

            if response.status_code  >= 300:                    #Handle errors from api
                print("an error has occured while accessing YT API, error code: " + str(response.status_code))
                print(response.json())
                sys.exit(1)
            
            for movie in response.json()["items"]:
                #print_video_info(movie)
                output.write(string_video_info(movie) + "\n")  
            
output.close()      #close the file

stringInput = input("Enter the file name just created:\n")

    
msg=EmailMessage()
msg['Subject']='Youtube playlist videos'
msg['From'] = 'Python Script'
msg['To']= 'ENTER EMAIL NAME TO BE SENT TO'


with open(stringInput) as myfile:
    data = myfile.read()
    msg.set_content(data)

with smtplib.SMTP_SSL('smtp.gmail.com',465) as server:
    server = smtplib.SMTP_SSL('smtp.gmail.com',465)
    server.login("ENTER YOUR EMAIL HERE,ENTER PASSWORD HERE")
    server.send_message(msg)


print("Email sent")