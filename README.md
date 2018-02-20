# purestorage-volumes
Polls the Pure Storage API checking to see if the current volumes are the same as the previously found volumes on the system. Also checks to ensure that the snapshots found are the same as the previous snapshots. The missing ones are checked to make sure that they are more than a day old before they were deleted.

If these cases do not match alarms are raised using the UIM API for action to be taken by the Storage Team