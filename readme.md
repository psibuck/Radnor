Radnor is an application I developed to help me manage stats and finances for my sunday league football team.

It takes advantage of another little application I developed, Starling, which takes retrieves raw Starling bank data and collates it in an easy to process format.

Currently it is a desktop application, written in Python. The UI is written in Tkinter.


Goals/Ambitions
I think this is best suited to having a web front-end that can be accessed by varying users. The public could view it to see a summary of stats and results for the club. Players could use it to check their outstanding debt and transaction history. To do this we would need to make the following changes:
1. Refactor data retrieval to use https requests and responses
2. Separate the UI and logic out as separate applications
3. Develop web front-end that mimics current UI
4. Add concept of users and login and begin
