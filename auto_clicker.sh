#!/bin/bash
bold=$(tput bold)
normal=$(tput sgr0)

mice=$(xinput --list | grep -E 'mouse|Mouse|Touchpad' | grep pointer) #list all input devices, select ones that are mice
mice_ids=($(echo $mice | grep -oP '(?<==)\w+')) #get their id values into an array

echo "This script auto clicks a chosen point every 5 seconds.
Then restores the pointer location and focus back to the original window.
If you want to pause the script, turn on Num Lock.
Mouse will not be moved if a mouse button is pressed down.
Script will retry in 0.5 seconds in that case."
read -p "${bold}Hover over the button you want to press and press enter.${normal}" #wait for enter key
button_location=($(xdotool getmouselocation | grep -oP '(?<=:)\w+')) #record x and y positions of mouse into an array
echo "The chosen position will be clicked every 5 seconds."
while [ 1 ]; do
  skip="false"
  numlock_status=$(xset -q | grep -oP '(?<=01: Num Lock:)(.*)(?=02: Scroll Lock:)')
  if [[ $numlock_status == *"on"* ]]; then
    echo "Num Lock is on."
    skip="true"
  fi  
  for id in ${mice_ids[@]}; do
    button_states=($(xinput --query-state $id | grep -oP '(?<==)\w+' | grep -E 'up|down')) #get button states for all device ids
    for state in $button_states; do
      if [ "$state" = "down" ]; then #if one of the buttons are pressed down, user is busy.
        skip="true"
        echo "Mouse button is pressed."
        break 2
      fi
    done
  done
  if [ "$skip" = "false" ]; then
    active_window=$(xdotool getactivewindow) #get active window before pressing selected button
    mouse_location=($(xdotool getmouselocation | grep -oP '(?<=:)\w+')) #get mouse location before pressing selected button
    xdotool mousemove ${button_location[0]} ${button_location[1]} click 1 & #move to the button and click
    sleep 0.1 #sleep for 0.1 seconds, sometimes a race condition occurs
    xdotool mousemove ${mouse_location[0]} ${mouse_location[1]} & #move the cursor back to the original position
    xdotool windowactivate $active_window #restore focus to original window
    sleep 5
  else
    echo "User busy, skipping..."
    sleep 0.5
  fi
done
