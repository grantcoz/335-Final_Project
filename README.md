# 335-Final_Project
The Titan Campus Algorithmic Assistant (TCAA) is an interactive Python-based GUI application designed to demonstrate core algorithmic concepts through real-world applications.

The system integrates multiple algorithm categories into one platform:

Graph Algorithms → Campus navigation
Greedy & Dynamic Programming → Task optimization
String Matching Algorithms → Document search

This project allows users to execute, compare, and analyze algorithms interactively.

Features
Interactive Tkinter GUI
Real-time algorithm execution
Multiple algorithm implementations:
BFS, DFS, Dijkstra, Prim’s MST
Greedy scheduling & 0/1 Knapsack
Naive, Rabin-Karp, and KMP search
Performance comparison between algorithms
Supports TXT, PDF, DOCX file inputs
Modular and scalable code design

GUI Modules & Instructions
1. Campus Navigator (Graph Algorithms)
Purpose: Navigate between campus buildings using graph algorithms.

How to Use:

Select a start building
Select an end building
Choose an algorithm:
BFS → Finds path with fewest hops
DFS → Displays traversal order
Dijkstra → Finds shortest distance path
Prim’s MST → Builds minimum spanning tree
Click Run
View results:
Path output
Distance (Dijkstra)
Traversal order (DFS)
MST edges and total cost

2. Study Planner (Greedy vs Dynamic Programming)
Purpose: Select optimal tasks based on time and value constraints.

How to Use:

Add tasks:
Task name
Time required
Value
Enter total available time
Run:
Greedy Algorithm (fast, approximate)
Dynamic Programming (Knapsack) (optimal solution)
Compare results:
Selected tasks
Total value
Time usage

3. Notes Search Engine (String Matching)
Purpose: Search for patterns in documents using different algorithms.

How to Use:

Upload a file:
TXT, PDF, or DOCX
Enter a search pattern
Choose an algorithm:
Naive
Rabin-Karp
KMP
ALL (compare performance)
Click Search
View:
Match positions
Execution time comparison

4. Algorithm Info Tab
Purpose: Provides explanations and theory behind the algorithms.

Includes:
Time complexity for each algorithm
Descriptions of:
Graph algorithms
Greedy vs Dynamic Programming
String matching algorithms
Overview of P vs NP problem
Algorithm Complexity Summary
Algorithm	Time Complexity
BFS / DFS	O(V + E)
Dijkstra	O((V + E) log V)
Prim’s MST	O((V + E) log V)
Greedy	O(n log n)
Knapsack (DP)	O(n × capacity)
KMP	O(n + m)
Rabin-Karp	O(n + m) (average)
