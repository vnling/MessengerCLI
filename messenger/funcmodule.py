import fbchat
from PyInquirer import Token, style_from_dict, prompt

style = style_from_dict({
    Token.QuestionMark: '#0abf5b bold',#'#3700B3 bold',
    Token.Answer: '#0abf5b bold',#'#BB86FC bold',
    Token.Instruction: '',  # default
    Token.Separator: '#cc5454',
    Token.Selected: '#0abf5b',  # default
    Token.Pointer: '#673ab7 bold',
    Token.Question: '',
})

'''
Functions to take in inputs, called in cli()
'''
#login information
def login():
    questions = [
        {
            'type': 'input',
            'name': 'email',
            'message': 'Please enter the e-mail you use with Facebook:',
        },
        {
            'type': 'input',
            'name': 'password',
            'message': 'Please enter your Facebook password:',
        },
    ]
    answers = prompt(questions, style=style)
    return answers

#actions that the user can choose from
def actions():
    questions = [
        {
            'type': 'list',
            'name': 'actionsOnStart',
            'message': 'Choose an action: ',
            'choices': ['Read messages', 'Send a message', 'Add to favorites', 'Delete from favorites'],
        },
    ]
    answers = prompt(questions, style=style)
    return answers

#adding a favorite user/group
def addFavorite():
    questions = [
        {
            'type': 'input',
            'name': 'toAdd',
            'message': 'Enter the name of the user or group you want to add: ',
        },
    ]
    answers = prompt(questions, style=style)
    return answers

#deleting a favorite user/group
def deleteFavorite(favorites):
    questions = [
        {
            'type': 'list',
            'name': 'toDelete',
            'message': 'Select the user or group you want to delete: ',
            'choices': [user.name for user in favorites],
        },
    ]
    answers = prompt(questions, style=style)
    return answers

#getting information about which conversations to read
def getMessages():
    questions = [
        {
            'type': 'list',
            'name': 'messagesToRead',
            'message': 'Who would you like to read messages from?',
            'choices': ['My favorites', 'Recent conversations', 'Someone else'],
        },
    ]
    answers = prompt(questions, style=style)
    return answers

#if necessary, getting specific user/group to read conversation from
def getUser():
    questions = [
        {
            'type': 'list',
            'name': 'userOrGroup',
            'message': 'Would you like to read messages from a user or a group?',
            'choices': ['User', 'Group'],
        },
        {
            'type': 'input',
            'name': 'userToRead',
            'message': 'Whose messages would you like to read?',
        },
    ]
    answers = prompt(questions, style=style)
    return answers

#getting information of message to be sent
def getMessageInfo():
    questions = [
        {
            'type': 'list',
            'name': 'userOrGroup',
            'message': 'Would you like to send your message to a user or a group?',
            'choices': ['User', 'Group'],
        },
        {
            'type': 'input',
            'name': 'sendToUser',
            'message': 'Who would you like to send your message to?',
        },
        {
            'type': 'input',
            'name': 'message',
            'message': 'What would you like to say to them?',
        },
    ]
    answers = prompt(questions, style=style)
    return answers

# deciding whether or not to end cli and logout
def terminate():
    questions = [
        {
            'type': 'list',
            'name': 'terminate',
            'message': 'Would you like to end this session?',
            'choices': ['Yes', 'No'],
        },
    ]
    answers = prompt(questions, style=style)
    return answers

'''
These functions handle the actual process of sending and receiving messages
'''
# handles message sending
def sendMessage(messageInfo, client):
    userOrGroup = str(messageInfo.get('userOrGroup'))
    sendTo = str(messageInfo.get('sendToUser'))
    message = str(messageInfo.get('message'))

    if userOrGroup == 'User':
        user = client.searchForUsers(sendTo)
    elif userOrGroup == 'Group':
        user = client.searchForGroups(sendTo)

    response = client.send(fbchat.models.Message(message), user[0].uid)
    return response

# handles message reading
def readMessage(user, client):
    try:  
        messages = client.fetchThreadMessages(thread_id=user.uid, limit=5)
        messages.reverse()
        for message in messages:
            print("— {}".format(message.text))
        print('----------------------------------------------------------')  
    except fbchat.FBchatException as e:
        print('Sorry! The messages could not be retrieved.')

