# Cab Pool Matcher

A command-line app that matches BITSians to shared cabs, giving seniors first pick.

## How to run
Python version 3.14.7 was used, nothing is required beside the standard python library. 

cabs.json must be in the same folder

## Menu options
### 1. Add a ride request

**What it does:** asks for the student's name, destination, time slot and year,
then adds them to the waiting list for that trip. Nobody gets a seat yet. Seats
are only handed out when a cab is dispatched (option 4).

**Input checks:**
- Name can't be empty.
- Destination must be Delhi or Jaipur. Time slot must be Morning, Afternoon,
  Evening or Night. Lower case like `delhi` is accepted and corrected to `Delhi`.
- Year must be a whole number from 1 to 5. Text like `abc` or `Year 7` asks again
  instead of crashing.

**Design choice:** each request gets a number from a counter that goes up by one
every time. This records who asked first, and it breaks ties between students in
the same year (see "How seniority works").

### 2. View waiting students and all cabs

**What it does:** Displays all the waiting requests including the details of name , destination , time slot and year. Also displays the cab driver name , destination , time slot ,seats taken out of the seats available and its status

**Edge cases:**
- If nobody is waiting, it prints "No requests yet"
- If no cabs were loaded, it prints "No cabs loaded"
- A cab that has left shows "Left" at the end in the details

**Design choice:** it doesn't check whether the `waiting` dictionary is empty. After a cab is dispatched, its trip's heap can become empty while the trip's key stays in the dictionary, so `len(waiting)` can be more than 0 even when nobody is waiting. Instead, a flag (`anyone_waiting`) becomes True only when a student is actually printed. If it's still False at the end, the app prints "No requests yet".

### 3. Find matches 

**What it does:** for every open cab, shows which waiting students would get a
seat if that cab left right now. It's only a preview as its a triala run and only shows who would get it but nobody gets assigned a spot.

**Edge cases:**
- If a cab has nobody waiting for its trip, it shows "(nobody waiting)"
- Cabs that have already left are skipped as the code "if cab.has_left: continue"
- If no cabs are open at all, it prints "No open cabs for (destination), (time slot) - students keep waiting"

**Design choice:** it works on a copy of each trip's waiting line instead of the
real one, because its only a preview and using the real one would change the orignal list. When two open cabs share a trip (like Ram and Shyam for
Delhi, Morning), the first cab takes the maximum number of kids it can and the second cab shows takes the rest of the kids which are left. This means the preview always matches exactly what Dispatch would do.


### 4. Dispatch a cab

**What it does:** asks for a destination and time slot, finds the first open cab
for that trip (in the order of `cabs.json`), fills it with the senior-most and if that is the same then the person who asked first and marks it as left.

**Edge cases:**
- If nobody is waiting for that trip, it prints "Nobody is waiting for (destination),(time slot)" and changes nothing.
- If every cab for that trip has already left, it prints No open cab and the students keep waiting
- If fewer students are waiting than there are seats, the cab leaves with the students even though it isnt full.

**Design choice:** it checks both conditions (someone waiting, an open cab)
before changing anything, so that dispatch happens or doesnt at all. Cabs are always searched in file order so
that same action give same result.


### 5. Quit

**What it does:** prints "Bye!" adn ends the program.

**Note:** data is not saved yet, so closing the app clears all waiting students and resets all cabs to open. The next run starts fresh from "cabs.json".


## Tricky situations
1. Half-empty cab: The cab leaves. This occurs when the seats are filled up completly or there ar wno waiting students. The seats cant be filled after it has left.

2. No cabs left: If eveyry cab for a trip has gone, It prints "No open cabs for (destination), (time slot) - students keep waiting" and changes nothing. Students stay in line and new requests get added to it. Nothing gets deleted.

3. Same year: If studenst are in the same year the onewho asked first gets the seat.

4. Lots of students (Big-O):
   - Adding one request: Finding the trip in the dictionary is O(1) but the 'heappush' is O(log n) because heap only moves item up one path.
   - Adding all 1,000: On adding 1000 requests , each time isO(log n) hence final is O(log n) as well.
   - Dispatching one cab: Finding the cab is O(c) and popping the studetns is O(log n). HEnce , O(logn + c)
   - Finding an open cab: it can go from 1(first cab is open)or upto all 'c' cabs. Best pick is O(c).