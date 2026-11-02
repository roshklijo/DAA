\# PowerWise – Smart Electricity Usage Optimizer



\## 1. Introduction

PowerWise is a GUI-based application that uses the 0/1 Knapsack algorithm to optimise the selection of household electrical appliances under a limited power capacity.



\## 2. Problem Statement

A household may have several electrical appliances but a limited available power capacity. Selecting appliances without considering their power consumption may exceed this limit. PowerWise finds a combination of appliances that maximises their total priority score without exceeding the specified power capacity.



\## 3. Algorithm Used

\*\*0/1 Knapsack using Dynamic Programming\*\*



Each appliance has:

\- Weight: Power consumption in watts.

\- Value: User-assigned priority score.



Each appliance can either be selected completely or not selected.



\## 4. Main Features

\- Add, edit and delete appliances.

\- Enter maximum available power capacity.

\- Find the optimal appliance combination.

\- Display selected and unselected appliances.

\- Show total power consumption and remaining capacity.

\- Visualise the Dynamic Programming table.

\- Compare optimal and greedy selections.

\- Display result charts.



\## 5. Complexity Analysis

For n appliances and capacity W:



\- Time Complexity: O(nW)

\- Space Complexity: O(nW)



\## 6. Technology

\- Python

\- Tkinter

\- Matplotlib



\## 7. Project Purpose

The purpose is to demonstrate the practical application of the 0/1 Knapsack algorithm through an interactive graphical interface.

