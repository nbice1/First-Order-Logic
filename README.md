# First-Order Logic with Identity

This project is aimed at developing a program to evaluate the truth-value of sentences in First-Order Logic with Identity and construct proofs.

There are two main functions, evaluator() and prover(), located in fol_evaluator.py and fol_proof_system.py, respectively. Functions are executed when the programs are run. 

## Syntax

The syntax is as follows: 

'U' - universal quantifier 

'X' - existential quantifier

'>' - material conditional

'~' - negation

'=' - identity symbol

'-' - biconditional

'^' - conjunction

'v' - disjunction

'T' - True

'F' - False

Atomic sentences have the form P(a,b,...,s). This also holds of the identity predicate, e.g. =(1,1) is a sentence while 1 = 1 is not. 'T' and 'F' are also treated as atomic sentences. 

Any formula with a binary connective as its main connective must be surrounded by parentheses. Any other formula must not be surrounded by parentheses. 

Example sentences: 

(P(a) v Q(a))

UxP(x)

UxXy(G(y,x) v =(x,1))

G(2,1)

Strings that are NOT sentences: 

P(a) v Q(a)

Ux(P(x))

a = a

(UxP(x))

### Determining the Truth-Value of Sentences Relative to a Model

After running evaluator(), you can input "model", "evaluate", or "exit". 

You should first define a model. After typing "model", you will be prompted to specify a domain of objects (separate inputs with commas). An example would be: 1,2,3,4. Note that the python "eval()" function is used to determine the intended datatypes. 

After specifying the domain, you will be prompted to specify the interpretations of expressions in the language. '=' is already interpreted as identity by default. First, specify an expression. Expressions should consist of letters and numbers. Constants begin with a lower-case letter or a number and predicates begin with an upper-case letter or '='. Note that 'T', 'F', 'U', 'X', and 'v' have logical meanings and should not be used. 

Then, specify the interpretation of the expression. One-place predicates should be given a sequence of objects as an interpretation, e.g. 1,2,3. Relational predicates should be given a sequence of tuples of objects as an interpretation, e.g. (3,1),(3,2),(2,1). Note that you should always make sure to only include objects located in the domain of the model, since the program currently will not check for this. The program also currently does not check that the arity is consistent. 

Type "done" to finish your intepretation. You will then be asked if you want to add additional variables to the language. Default variables are 'u','v','w','x','y','z'. Separate new variables with commas. 

With your model constructed, it is time to determine the truth-value of a sentence. After inputting "evaluate", input a sentence to determine its truth-value relative to the constructed model. 

### Constructing a Proof

The derivation system is designed to be sound and complete. Hence, any mathematical proof could in-principle be translated into this system and checked for validity. 

The derivation system is a natural deduction system for first-order logic with identity. One will first be asked to state the premises. One will then be asked to apply inference rules. One can always input "Exit" to exit the program. 

Proofs will be printed as follows: 

0    (P(a) ^ P(b))

1    P(c)
_______________

2    P(a)

3    (P(a) ^ P(c))

4    | Q(d)

5    | (P(a) ^ P(c))

6

7    (Q(d) > (P(a) ^ P(c))

Here, lines 0 and 1 are premises. Line 4 begins a subproof. Line 6 ends the subproof. Line 7 is the desired conclusion. 

Separate premises with commas. If no input is given, the proof will proceed without premises. The rest of the system consists of applying inference rules. The following commands can be used at any point: 

Exit - Exit the program.

delete - Remove the last line of the proof.

Finish - Output the theorem proved.

The following commands are the basic inference rules: 

Assume,p - Begin a subproof with assumption p, where p is a sentence.

End - Exit the current subproof.

R,n - Apply Reiteration to the formula at line n. 

^EL,n - Apply Conjunction Elimination to the left conjunct of the conjunciton at line n.

^ER,n - Apply Conjunction Elimination to the right conjunct of the conjunction at line n.

^I,n,m - Apply Conjunction Introduction to the formulas at lines n and m.

TI - Apply Tautology Introduction.

FI,n,m - Apply Contradiction Introduction to formulas at lines n and m. The second formula must be the negation of the first.

FE,n - Apply Contradiction Elimination to the formula F at line n. 

vIL,n,p - Apply Disjunction Introduction to the formula at line n, resulting in a formula with formula p as its left disjunct. 

vIR,n,p - Apply Disjunction Introduction to the formula at line n, resulting in a formula with formula p as its right disjunct. 

vE,j,k-l,m-n - Apply Disjunction Elimination to the disjunction at line j using subproofs k-l and m-n. Subproofs k-l and m-n must begin with the left and right disjunct, respectively, of the disjunction and must end with the same formula, which will be outputted. 

>E,n,m - Apply Conditional Elimination to the conditional at line m using its antecendent at line n. 

>I,n-m - Apply Conditional Introduction to the subproof from line n to m. 

~E,n - Apply Negation Elimination to the double negation at line n. 

~I,n-m - Apply Negation Introduction to the subformula from line n to m. The formula at line m must be F. 

-ER,n,m - Apply Biconditional Elimination to the formula at line n using the left subformula at line m, outputting the right subformula. 

-EL,n,m - Apply Biconditional Elimination to the formula at line n using the right subformula at line m, outputting the left subformula. 
