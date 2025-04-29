πρωτόκολλο επικοινωνίας μεταξύ ενός server και
πολλαπλών client. Ο Server δρα σαν μία αναλυτική μηχανή η οποία εκτελεί τις εξής 3
πράξεις:

Α. Πολλαπλασιασμός Ν προσημασμένων ακεραίων, όπου Ν μεταξύ 2 και 10. Ο κάθε
ακέραιος που θα δέχεται ο Server πρέπει να είναι από -5 έως και 5. O server θα επιστρέφει
το αποτέλεσμα του πολλαπλασιασμού.

Β. Μέσος όρος Ν ακεραίων, όπου Ν μεταξύ 2 και 20. Ο κάθε ακέραιος που θα δέχεται ο
Server πρέπει να είναι από 0 μέχρι 200. Ο Server θα επιστρέφει το αποτέλεσμα του μέσου
όρου.

Γ. Αφαίρεση 2 σετ από Ν αριθμούς, όπου Ν μεταξύ 2 και 10. Ο κάθε ακέραιος που θα δέχεται
ο Server πρέπει να είναι από 0 έως και 60000. Ο Server θα δέχεται 2 σετ από Ν αριθμούς και
θα αφαιρεί από κάθε αριθμό του πρώτου σετ με τον αντίστοιχο αριθμό του δεύτερου σετ.
Θα επιστρέφει δηλαδή 1 σετ από Ν αριθμούς. Π.χ. αν ο client στείλει τους αριθμούς στο 1ο
σετ: 2, 4 και 6 και στο 2ο σετ 1, 3 και 4, ο server θα επιστρέψει 1, 1 και 2.

O client θα πρέπει να στέλνει στον server όσους αριθμούς χρειάζεται και την εντολή που
θέλει να εκτελεστεί, και θα πρέπει να λαμβάνει πίσω σαν απάντηση είτε το αποτέλεσμα αν
είναι επιτυχημένη η πράξη ή μήνυμα λάθους (και τι είδος λάθους - αν π.χ. δοθούν σαν είσοδο
αριθμοί μεγαλύτεροι από το προαπαιτούμενο).



communication protocol between a server and multiple clients. The server acts as an analytical engine that performs the following 3 operations:

A. Multiplication of N signed integers, where N is between 2 and 10. Each integer accepted by the server must be between -5 and 5. The server will return the result of the multiplication.

B. Average of N integers, where N is between 2 and 20. Each integer accepted by the server must be between 0 and 200. The server will return the result of the average.

C. Subtracting 2 sets of N numbers, where N is between 2 and 10. Each integer that the Server will accept must be from 0 to 60000. The Server will accept 2 sets of N numbers and will subtract from each number in the first set the corresponding number in the second set. It will return 1 set of N numbers. For example, if the client sends the numbers in the 1st set: 2, 4 and 6 and in the 2nd set 1, 3 and 4, the server will return 1, 1 and 2. 
The client should send the server as many numbers as it needs and the command it wants to execute, and should receive back as a response either the result if the operation is successful or an error message (and what type of error - if, for example, numbers greater than the prerequisite are given as input).
