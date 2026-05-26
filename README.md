[🇷🇺 Русский](README_RU.md)

# **PyChat**
An application for exchanging messages and files within a local network.

## Purpose of creation
The project was completed as part of training at the Yandex Academy Lyceum. The main task is to master in practice the creation of a client-server GUI application with user registration, personal and group chats, file transfer and changing themes.

![2022-02-10_09-31-16.png](imgs/2022-02-10_09-31-16.png)
![2022-02-10_09-31-21.png](imgs/2022-02-10_09-31-21.png)

In the authorization window, you need to enter the login and password you created during registration. If there is an error in the data, the corresponding error is displayed. If the data is entered correctly, the authorization window closes and the main window opens.

![2022-02-10_09-31-45.png](imgs/2022-02-10_09-31-45.png)

The main window presents most of the program's functionality. A new user is greeted with an empty list of conversations and personal chats. The left side shows the main panel with buttons. The very first (top) button with a plus icon opens a new window with a list of all users of the program, except for the user himself and those with whom he is already in correspondence; there is also a field for entering keywords (search) and a button with a magnifying glass icon that activates the search. The user list is a list of buttons with user names, their logins and photos. If you enter any keywords into the search and click on the “search” button, the list will be updated and only users corresponding to the request will remain in it. When you click on a user, the window closes in the main window, the corresponding user is added to the chat list and a correspondence window with the user opens.

![2022-02-10_09-32-221.png](imgs/2022-02-10_09-32-221.png)

In it we can see the message history, a text input field, a send button, window refresh, settings, information about the user’s last authorization session, and a button containing his name and photo. When you type and send text, a corresponding message is added to the widget. A button with a paperclip icon “send file”, when clicked, a window opens in which you can select a file, when you select a file, a button is added to the widget, when clicked, which, if the file is an image, opens a window where you can view the photo and then, if necessary, save it. In the situation with all other file types, a window opens in which we can select the directory in which to save the file. The button with the photo and the name of the interlocutor, when pressed, opens a window with information about the user (photo, name, login and the “write message” button), the button with the gear icon - “settings”, when pressed, a window with three buttons opens, we can clear the widget (will only delete the display of messages), clear the history (will delete all messages from the correspondence) and delete the chat (will delete the user from contacts, correspondence history, the user will no longer be displayed on the main window). The "refresh" button updates the widget.

![2022-02-10_09-33-09.png](imgs/2022-02-10_09-33-09.png)
![2022-02-10_09-33-28.png](imgs/2022-02-10_09-33-28.png)

The second button on the main window, “new conversation,” opens a window with a list of users with whom we are already in correspondence, we can select the users we need by checking the box and find the desired users from the list using the keyword input line and the “search” button
When you click on the “create” button, a window will open where we must enter the name of the conversation and, if desired, select a photo of the conversation. When you click on the “create” button, the window will close, on the main window the conversation we created will be added to the list of chats, and the window of the conversation itself will open, in it we will see a text input field, a widget displaying messages, a send message button, a file send button, an update button, a button with the number of participants and a “manage” button, a button with information about the number of participants opens a window with a list of participants. The “manage” button opens the conversation management window; if you are not the conversation creator, then you can only add new participants, clear the conversation widget, or exit the conversation. If you are the creator of a conversation, you can change the title of the conversation, clear the conversation widget, clear the conversation history, change the photo of the conversation, delete the conversation, add new participants, and remove the participants you want from the conversation.
The third button of the main window has the profile photo under which you are logged in; when clicked, a window opens in which you can change your profile photo, username and password.

![2022-02-10_09-32-22.png](imgs/2022-02-10_09-32-22.png)
![2022-02-10_09-33-40.png](imgs/2022-02-10_09-33-40.png)
![2022-02-10_09-38-00.png](imgs/2022-02-10_09-38-00.png)

The fourth button of the main menu allows you to find any user of the program. When you click on the button, a list of users opens, regardless of whether you correspond with someone or not, you can search for the user you need, when you click on the user, a window opens with information about the user (profile photo, name, login).

![2022-02-10_09-32-31.png](imgs/2022-02-10_09-32-31.png)

The fifth button of the main menu, updates the main menu.

The sixth (bottom) button of the main menu changes the theme to dark and back. When you click the button, you should re-open the remaining windows, if any, so that the theme is applied to them.

The main widget displays a list of all personal correspondence and conversations in which you are a member. When you click on any item in the list, a window opens depending on the item you clicked, described above.
## **Contacts**
Email - andreiduvakin@gmail.com

## License
MIT. See file [LICENSE](LICENSE).
