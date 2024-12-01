import platform
import subprocess
import os


def main():
    num_terminals = int(input("Enter the number of terminals to open: "))
    num_repetition = int(
        input("How many times do you want to run the test? (Max: 1000): ")
    )

    # Prepare the command to execute
    system_platform = platform.system()
    working_directory = os.getcwd()

    for i in range(num_terminals):
        if system_platform == "Windows":
            command = f"python main.py {num_repetition}"
            subprocess.Popen(
                ["cmd", "/c", f"start cmd /c {command}"], shell=True
                # ["cmd", "/c", f"start cmd /k {command}"], shell=True
            )

        elif system_platform == "Darwin":
            command = f"python3 main.py {num_repetition}"
            apple_script = f'''
            tell application "Terminal"
                do script "cd {working_directory} && {command}; exit"
                delay 0.5 -- Ensure the command starts before we proceed
                tell application "System Events" to keystroke "w" using command down
            end tell
            '''
            subprocess.Popen(["osascript", "-e", apple_script])

        else:
            command = f"python3 main.py {num_repetition}"
            subprocess.Popen(
                ["gnome-terminal", "--", "bash", "-c",
                 f'{command}; exit; exec bash']
            )


if __name__ == "__main__":
    main()
