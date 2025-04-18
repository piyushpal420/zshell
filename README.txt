This is an pbl project for Software Engineering.
Led By Mehdi Zaidi and contributers include Kirri Tharun, Tushar Dwivedi and Piyush Pal.
This Project implements a custom shell for linux using the readline library from GNU.


*************INSTRUCTIONS FOR RUNNING CODE****************


NOTE: This code will run only on UNIX/LINUX systems so either install WSL on your windows or use a VM with ubuntu.

JUST RUN frontend.py FILE AND THE SHELL WILL RUN

1. Install GNU's readLine library using:-

sudo apt-get install libreadline-dev        (linux)

2. After its finished installing, your system is now ready to run readLine library function.

3. For running test.c, you can just execute the a.out

4. And if you want to make changes and compile test.c then:-

gcc test.c -lreadline -lcurses
                                                                
This line adds linkage with the GNU Readline library. I have made use of readline() and add_history() functions,
which are part of the readline library, which cannot be used without linking it during compilation.


*************INSTRUCTIONS FOR RUNNING CODE****************
