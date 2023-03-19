
```
From: Ece Eksi <eksi@ohsu.edu>
Date: Tuesday, March 14, 2023 at 6:17 PM

Here is the key:

R = round number
c = channel ID (there are four channels for each image c2-c5)
Q = indicates a quenching round. These images are captured to measure tissue autofluorescence. There is no real marker signal in these images. There are three quench rounds R0Q, R3Q and R10Q.

Example:
R5_CDX2.CD8.CD163.CD66b_31022-6_2020_08_22__8832-Scene-001_c3_ORG.tif

RoundNumber5_MarkerName.MarkerName.MarkerName.MarkerName_TissueID_DateOfImaging__RandomFileSpecificNumber_ChannelID

Example 2:
R3Q_Q3c2.Q3c3.Q3c4.Q3c5_31022-6_2020_08_18__8785-Scene-001_c5_ORG.tif

Q means this is a quench round imaging. 
Q3c1 = no markers were captured, therefore each channel (c) is marked with a Q3cX instead of marker name.
```