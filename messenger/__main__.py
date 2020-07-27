import fbchat
from fbchat import Client

import pickle
import os

from PyInquirer import Token, style_from_dict, prompt

from .funcmodule import *

#main cli function, calls other functions to carry out the actions selected by the user
def cli():

    #state variable enables the user to keep running the cli app
    runCLI = True

    try:
        # get login information from user and log in to the client
        loginInfo = login()
        email = loginInfo['email']
        pw = loginInfo['password']
        client = Client(email, pw)

    except fbchat.FBchatException as e: #the exception isn't here
        print('There was an exception: %e' % (e))

    while runCLI:

        #ask the user for actions they want to take
        action = actions()

        #reading messages
        if action.get('actionsOnStart') == 'Read messages':
            toRead = getMessages()

            #reading messages from favorite users
            if toRead.get('messagesToRead') == 'My favorites':
                if os.path.exists('favorites.csv'): 
                    #open the file if it exists
                    with open('favorites.csv', 'rb') as favoritesFile:
                        favorites = pickle.load(favoritesFile)

                    #if file exists but favorites list is empty, let the user know
                    if favorites == []:
                        print('Your favorites list is empty.')
                    
                    #otherwise get the conversations and print the conversations
                    else:
                        print('----------------------------------------------------------')
                        print('Fetching your favorite conversations...')
                        print('----------------------------------------------------------')
                        for thread in favorites: 
                            print('Your conversation with ' + thread.name + ': ')
                            readMessage(thread, client)

                # if no file exists, let the user know there are no favorites
                else:
                    print('Your favorites list is empty.')
            
            #reading messages from five most recent conversations
            elif toRead.get('messagesToRead') == 'Recent conversations':
                #fetch conversations
                threads = client.fetchThreadList(limit=5) 
                print('----------------------------------------------------------')
                print('Fetching your five most recent conversations...')
                print('----------------------------------------------------------')
                #print messages
                for thread in threads:
                    print('Your conversation with ' + thread.name + ': ')
                    readMessage(thread, client)

            #reading messages from a specific user or group
            elif toRead.get('messagesToRead') == 'Someone else':
                #get necessary information
                user = getUser()

                #search function is different for users and groups
                if user.get('userOrGroup') == 'User':
                    userToRead = client.searchForUsers(str(user.get('userToRead')))
                elif user.get('userOrGroup') == 'Group':
                    userToRead = client.searchForGroups(str(user.get('userToRead')))

                #print messages
                print('----------------------------------------------------------')
                print('Your conversation with ' + userToRead[0].name + ': ')
                readMessage(userToRead[0], client)
                
        #sending a message
        elif action.get('actionsOnStart') == 'Send a message':
            #ask for information about the message
            messageInfo = getMessageInfo()

            #send message 
            try:
                response = sendMessage(messageInfo, client)
                print("Your message was sent!")
            except Exception as exception:
                #raise exception if message cannot be sent
                raise Exception('We have an error: %s' % (exception))
        
        #adding to favorites
        elif action.get('actionsOnStart') == 'Add to favorites':
            #if file exists open it and load contents to list
            if os.path.exists('favorites.csv'):    
                with open('favorites.csv', 'rb') as favoritesFile:
                    favorites = pickle.load(favoritesFile)
            #otherwise file doesn't exist, initialize empty list
            else:
                favorites = []
            
            #get information of user/group to be added and search for said user/group
            toAdd = addFavorite()
            user = client.searchForThreads(str(toAdd.get('toAdd')))
            
            #append the new favorite if not already in favorites list
            if user[0] not in favorites:
                favorites.append(user[0])
 
            #write the entire favorites list to the file (as user objects)
            with open('favorites.csv', 'wb') as favoritesFile:
                pickle.dump(favorites, favoritesFile)

            #let the user know favorite has been added
            print(user[0].name + ' has been added to your favorites list!')

        #deleting from favorites
        elif action.get('actionsOnStart') == 'Delete from favorites':
            #if file exists, open it and load contents to list
            if os.path.exists('favorites.csv'): 
                with open('favorites.csv', 'rb') as favoritesFile:
                    favorites = pickle.load(favoritesFile)

                #if favorites is not empty, get information of user/group to be deleted
                if favorites != []:
                    toDelete = deleteFavorite(favorites)
                    userToDelete = str(toDelete.get('toDelete'))

                    #remove user if in existing favorites list
                    for user in favorites:
                        if userToDelete == user.name:
                            favorites.remove(user)
                            print(userToDelete + ' was deleted from your favorites list.')

                    #now write the modified favorites list to file
                    with open('favorites.csv', 'wb') as favoritesFile:
                        pickle.dump(favorites, favoritesFile)
            
                # if favorites list is empty let user know
                else:
                    print('There is no existing favorites list.')

            #if there is no favorites file let user know
            else:
                print('There is no existing favorites list.')

        #ask the user if they want to terminate the session
        endSession = terminate().get('terminate')
        #modify state variable if necessary
        if endSession == 'Yes':
            runCLI = False

    #logout at the end, let the user know
    client.logout()
    print('You have been logged out. See you soon!')

if __name__ == '__main__':
    cli()