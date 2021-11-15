# How to increase swap space for Android project compilation.
If you encounter system freezes while compiling Android on a 16GB system, you are most probably encountering OOM (Out of Memory) issues on Linux. This stems firstly from a lack of physical memory installed on your device because 16GB of ram is barely enough for compilation. If your ram is occupied by other applications such as multiple Chrome tabs, multiple Visual Studio Code projects open or any other Electron based application (ie. Teams, Spotify) there might not be enough memory left for compilation. At this point Linux starts to swap memory to disk. This will slow down the system significantly, however things will continue to run. If you also run out of swap space, Linux will start killing processes. This may result in system freezes that last for an hour in some cases and your compilation failing.

Since adding more phsical memory is out of the question, we should provide enough swap space. To be on the safe side, allocate as much swap space as there is phsical memory. In this case, our swap file will be 16GB.

To check the size of your swap partition or swap file issue the following command:
<pre><code>swapon --show
</code></pre>
The result will be something like the following if you have a swap partition available:
<pre><code>NAME      TYPE      SIZE   USED PRIO
/dev/sda3 partition 7.5G 563.8M   -2
</code></pre>
Check the UUID of your swap partition. Instead of sda3, grep for whatever your partition name was in the first step:
<pre><code>sudo blkid | grep sda3
</code></pre>
The result will be something like this:
<pre><code>/dev/sda3: UUID="97d0440b-4967-4615-ac39-23bc185d1078" TYPE="swap" PARTUUID="0032566e-01"
</code></pre>
Take note of the UUID, you'll look for it in /etc/fstab in the following steps.

To turn off this swap partition issue, the following command:
<pre><code>sudo swapoff -a
</code></pre>
After turning off the swap partition, you'll need to remove it from /etc/fstab so Linux won't enable it the next time you reboot. Open /etc/fstab with a text editor:
<pre><code>sudo gedit /etc/fstab
</code></pre>
Comment out the line that references swap and the UUID of your swap partition, it will look something like this when it is commented out:
<pre><code>#UUID=97d0440b-4967-4615-ac39-23bc185d1078 none   swap    sw      0       0
</code></pre>
Now we need to create a 16GB swapfile, turn on swap and add it to /etc/fstab.

The following commands create a 16GB swapfile, assigns the proper permissions, sets up the swap area and enables swap:
<pre><code>sudo fallocate -l 16G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
</code></pre>
After running these commands check to see if it was successful. You should see something like this:
<pre><code>sudo swapon --show

NAME      TYPE SIZE USED PRIO
/swapfile file  16G 2,4G   -2
</code></pre>
To make this swapfile survive a reboot, it should be added to /etc/fstab. Open /etc/fstab with a text editor:
<pre><code>sudo gedit /etc/fstab
</code></pre>
At the end of the file add the following line:
<pre><code>/swapfile swap swap defaults 0 0
</code></pre>
You are now ready to compile Android.

If you want to reclaim the disk space that was previously formatted as a swap partition. You can easily do this using an application like gparted. Delete the swap partition and resize your root partition to fill the space.

If your boot times increase by around 30 seconds after disabling the swap partition, check to see if the system is trying to resume from the old swap partition:
<pre><code>cat /etc/initramfs-tools/conf.d/resume

RESUME=UUID=97d0440b-4967-4615-ac39-23bc185d1078
</code></pre>
If this file exists and there is a UUID after RESUME, open /etc/initramfs-tools/conf.d/resume with a text editor:
<pre><code>sudo gedit /etc/initramfs-tools/conf.d/resume
</code></pre>
Change the line to:
<pre><code>RESUME=none
</code></pre>
After saving the above file, run the following command so it takes effect:
<pre><code>sudo update-initramfs -u
</code></pre>
After you reboot your device, it will no longer wait for 30 seconds before booting.



