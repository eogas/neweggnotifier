## neweggnotifier

### summary
neweggnotifier is a quick little project I wrote to check up on a specified list of newegg products, and report price drops using notifo.  The impetus for this project was mostly based on my overheating 9600 gt and a severe case of 'broke college student'.

### future
For the purposes of finding a good deal on a new graphics card, the current implementation is adequate for my needs.  However, if I ever decide to do a full build, or I publish this repository and there is an interest for new features, some of the possible additions include:

   * UI
   * Notification on specific price threshold
   * Notification on specific price threshold of a group of products
   * Inclusion of shipping costs
   * Notification of price drops on products in a specific query

### design options

Concerning the addition of UI, I have been given multiple suggestions as to a good design.  Some possible solutions are:

* Simple UI that takes a list of items, notifo username and api key, then runs in the background.
* Feed style UI that polls a specific query or category for new items or price changes.

Note: Any GUI solution will no longer require growl for desktop notifications, however it would still be a good idea to include notifo integration for people who want further notification (notifo smartphone apps, etc)

### credits

A lot of the credit for this project needs to go to [James Sumners](https://bitbucket.org/jsumners) for his PyNotifo module and to [Douglas Hall](http://www.bemasher.net/) for his research on Newegg's unofficial JSON API.  These guys made it possible for me to write the initial implementation in a number of hours.

    * https://bitbucket.org/jsumners/pynotifo
    * http://www.bemasher.net/archives/1002

