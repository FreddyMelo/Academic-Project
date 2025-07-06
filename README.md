** DISCLAIMER **
This project is an academic project from University of Minnnesota - Twin Cities, CSCI 4271W. In collaboration with two peers, David Smith & Jaime Somero. This project examines a fictional software application, Badly Coded Manager (BCBM). The team was tasked with finding 6 vulnerabilites within the code, drafting proof-of-concept scripts, and writing a report detailing the findings. With permission, I have added this to my personal Github/resume to showcase my ability to find vulnerabilities, test, and implement real fixes to software code. I included the report within the repository to show the entire report and the communication skills I can bring. 



Below are the instructions for running and executing the attacks. 

Vulnerability ID 1: Weak authentication code spoofing (new_auth_code_brute_force.py)

What to expect: The python script goes through the list of 21 possible authentication codes, until it matches the a user's authentication code. This simulates an attacker running the script to gain access to other individuals bcbmc sessions. Although not necessary for this PoC, in a real attack the attacker would need first generate the possible authentication codes. This script can be found in the repo under the name generate_auth_code.py. Feel free to run this script first to see how these codes are generated, but the codes themselves were coded into the new_auth_code_brute_froce.py for simplicity. 

1. Download new_auth_code_brute_force.py

2. Save it to the bcbmc directory
   
4. Have bcbmc session running in 1 terminal on the VM
   
5. Open up a 2nd terminal connected to the same VM

6. Execute the script: python3 auth_code_brute_force.py

7. (For testing purposes) To view progress, navigate to the terminal running BCBMC and you will see all the keys being tested.

8. Success: the authentication code of the session you are running will print 



Vulnerability ID 2: Rank Overflow (overflow.html)

What to expect: The given overflow.html is a simulation of a user opening a malicious link that intends to cause an overflow attack through the rank field. In a real attack a victim would recieve a link to the malicious website through email or anywhere else attackers can share harmful links. This PoC simplifies the process and simulates how the contents of the link being opened could harm the user's session. 

1. Download overflow.html
   
2. Log into session of BCBM
   
3. Acquire valid authentication code
   
5. Input authentication code into given script (an attacker would utilize the script from Vulnerability ID 1 to acquire this)

6. In same seperate window of the VM were BCBM is running, run the overflow.html script

7. Success: Navigate to the top 10 bookmark page and observe the results



Vulnerability ID 3: Malicious URL (evil.html, good.html)

What to expect: When the URL to the attacker-controlled webpage is submitted into the add bookmark form, the normal confirmation page will not appear. Instead, when the title of the "evil.html" page is loaded, the contents of the page will be replaced by an embedded YouTube video from an entirely different page. This is because the the malicious "evil.html" page is able to inject HTML code into the confirmation page, which redirects the user to another page without them prompting it to. 

1. Log into BCBM in a browser, and navigate to the "Add bookmark" page

2. Enter malicious URL into textbox: https://www-users.cse.umn.edu/~somer137/evil.html

3. Click "Get started!"

4. The page will start to load the add bookmark confirmation form, which will be replaced by the contents of good.html which is primarily an embedded YouTube video

Alternatively, 

1. Run BCBMC in command line, 

2. Then run the following command in the terminal: 
    curl -L -m 2 --retry 2 -w 'curl -L -m 2 --retry 2 "http://localhost:8888%{urle.path}add/url/https%3a%2f%2fwww-users.cse.umn.edu%2f~somer137%2fevil.html/"' 'http://localhost:8888/'

3. Copy the last line of the output, which should look like a curl command with a complete URL and paste it into the command line 

4. Curl will output the HTML of the page, which will include a "<script>" portion. This is the code that replaces the content of the page  



Vulnerability ID 4: Brute forcing a key to decrypt cloud files (DecryptBookmarks.py, encrpt_message.c)

What to expect: The encrypt_message.c file is used to create a an html file that is encrypted utilizing the same exact process as is used in the sync.c file, the encryption code is copied and pasted into this file, it is simply used to create an example html file that can be decrypted to prove the vulnerability in encryption. Once the encrypt_message.c file is run, you will have a new cloud_all.ehtml file that is encrypted if you attempt to read it. In the same directory as this cloud_all.ehtml file, when the DecryptBookmarks.py script is ran it will take a few minutes to search through all the possible keys and decrypt the cloud_all.ehtml file. Once the correct key has been found, the script will terminate and you will have a file named try.html in your directory which you can open and will contain the same code placed into the original cloud_all.ehtml file that you can see within the encrypt_message.c file. You can compare the code in the encrypt_message.c file and the sync.c file in the project code in order to verify that the encryption is done exactly the same way. This clearly shows how the encryption of bookmarks in the cloud_all.ehtml file that is accessible by every user of bcbmc is faulty and can easily be brute forced and decrypted.

The expected contents of the try.html file is:

![image](https://github.umn.edu/melo0035/CSCI-4271W-Project/assets/28961/f08d0ed1-e43f-49bd-be12-4e6241adad57)


1. Download encrypt_message.c and DecryptBookmarks.py
   
2. Compile encrypt_message.c by running in the command line: gcc -o encrypt_message encrypt_message.c
   
3. Run encrypt_message.c in the command line: ./encrypt_message
   
4. Open the file cloud_all.ehtml that is generated and view how it is encrypted and cannot be read
   
5. Run the python DecryptBookmarks.py script in the command line within the same directory: python3 DecryptBookmarks.py
   
6. Wait until the terminal prints the output message containing the key that has been found and the statement: "Decrypted Bookmarks Found in try.html"
   
7. Open the try.html file that will now be located in the same directory as the C and Python programs were being ran in and see that the contents are equal to that listed above these steps.



Vulnerability ID 5: Spoofed Token Generation

What to expect: This script will create an account using a victim's email (example@email.com). The script will then go through all possible tokens and test them by attempting to reach the account completion endpoint of bcbm utilizing the generated token. Every 100 token attempts, a message will be printed showing how many tokens have been attempted. Once the token is found by the script and the account has been fully activated, the script will print out the token that is associated with the victim's email as well as which seeds were used to generate the token.

1. Download TokenGeneration.py

2. Start bcbms as per usual in a VM terminal, entering into the command line: sudo start systemctl bcbms

3. Then in the command line enter: bcbmc

4. Open a new terminal that is connected to the same VM

5. In this new terminal run the PoC script by entering: python3 TokenGeneration.py



Vulnerability ID 6: Command injection via XSS

What to expect: If the included xss.html page is loaded up while the bcbmc HTTP server is running on their computer, the javascript in xss.html will dynamically create "img" nodes that will attempt to retrieve resources from the bcbmc add bookmark page using all possible authentication codes. The GET requests will fail, as most of the authentication codes will not work, and because there are no images to retrieve in the first place. The URLs in the src attributes of these img nodes contain a command injection that will succeed, however, removing all html files from bcbmc's working directory (~/.bcbm).  

1. Run BCBMC and load it for the first time in any browser.

2. In another tab or browser, go to https://www-users.cse.umn.edu/~somer137/xss.html (the HTML code for which is in xss.html in this repo)

3. If desired, open the developer tools pane to the console to see the GET requests, which will all fail, as the "image" they're trying to load is not an image.

4. Reload the BCBMC page in the original tab, and get a 401 error and/or take a look at the .bcbm directory to see that all the .html files are missing
