# zero-key-score

## Intro
zero-key-score is a keylogger purely made for security and educational purposes.

[NOTE] This project uses python3.


## Instructions to use
This project has two major dependencies.
  1. pyxhook
  2. pyperclip

First before running the main script. You need to install those packages.

```bash
pip3 install -r requirements.txt
```
You may need to run the above command with ```sudo``` depending on the permissions the user permissions.

There are few things to be changed in the ```src/zero-key-score.py``` file according to your needs.
  1. Change Google Form URL. Visit the example url in program and create similar one.
  ```python3
  google_form_url = <New Form URL>
  ```
  2. Change the time to wait before posting to google form
  ```python3
  wait_time_to_post = <new time>
  ```
  3. wait_time_to_listen_clip = <Time to wait before reading the copied content>(sec)
  ```python3
  wait_time_to_listen_clip = <new time>
  ```

Finally, you can run the program by following the below commands
```bash
# Change directory to the src/
cd <path>/zero-key-score/src

# Make the program executable
chmod +x zero-key-score.py

# Run the script
./zero-key-score.py
```

Coversely, you can also run the program without making it as an executable.
```bash
python3 zero-key-score.py
```
