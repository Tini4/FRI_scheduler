# FRI scheduler

Create your schedule for UL FRI.

## Usage

Run the script with IDs of subjects you are taking, e.g. `FRI_scheduler 63220 63216 63280`.
Use `-u` to change the URL to the timetable (it is se to current timetable by default),
e.g. `-u https://urnik.fri.uni-lj.si/timetable/fri-2024_2025-letni`.
If the faculty timetable changes, add `-c` to refresh the cache.

Once the schedule is generated, open the printed link to view your timetable.
You can remove entries by clicking on them. To undo a removal, press Ctrl+Z.

## Warning

Removing entries from the schedule is done in your browser.
If you close or refresh the page, any changes made will be lost.
