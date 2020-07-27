# MessengerCLI
A command line app for Facebook Messenger, designed so you only see the messages you want to see.


### Installation & Quick Start

1. [Clone](https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository) this repository
2. Run the following commands from the cloned folder:
```
$ pip3 install fbchat pickle PyInquirer
$ sh install.sh
```
The first command installs the necessary modules, while the second runs a shell script that installs the app itself.

To run the MessengerCLI, just run the ```messenger``` command from anywhere in your command line.

### Features
 - **Read messages**
     - Gives you the option of reading from a user-configured favorites list, your most recent conversations, or a specific account.
     - Displays the five most recent messages from each conversation.
 
 - **Send messages**
     - Prompts you for the account you want to send a message to as well as the content of the message you want to send.
 
 - **Set up and modify your favorites list**
     - Add to or delete from your favorites list with the two options in the main menu, ensuring that you only see the messages you want to see. Your favorites list is saved in your local storage, so it remains the same even if you restart your session!


### FAQs

**The app asks me for my Facebook login details. Do you store them?**

No, we don't. The details are used for a one-time login, and deleted when you exit the app. In fact, the app is set up to log you out at the end of every session, which is why you have to re-enter your details every time you start it up. The only data that gets written into storage is your favorites list, which exists strictly on your local device and is not shared with anyone else.
