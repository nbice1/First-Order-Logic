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

## Determining the Truth-Value of Sentences Relative to a Model

After running evaluator(), you can input "model", "evaluate", or "exit". 

You should first define a model. After typing "model", you will be prompted to specify a domain of objects (separate inputs with commas). An example would be: 1,2,3,4. Note that the python "eval()" function is used to determine the intended datatypes. 

After specifying the domain, you will be prompted to specify the interpretations of expressions in the language. '=' is already interpreted as identity by default. First, specify an expression. Expressions should consist of letters and numbers. Constants begin with a lower-case letter or a number and predicates begin with an upper-case letter or '='. Note that 'T', 'F', 'U', 'X', and 'v' have logical meanings and should not be used. 

Then, specify the interpretation of the expression. One-place predicates should be given a sequence of objects as an interpretation, e.g. 1,2,3. Relational predicates should be given a sequence of tuples of objects as an interpretation, e.g. (3,1),(3,2),(2,1). Note that you should always make sure to only include objects located in the domain of the model, since the program currently will not check for this. The program also currently does not check that the arity is consistent. 

Type "done" to finish your intepretation. You will then be asked if you want to add additional variables to the language. Default variables are 'u','v','w','x','y','z'. Separate new variables with commas. 

With your model constructed, it is time to determine the truth-value of a sentence. After inputting "evaluate", input a sentence to determine its truth-value relative to the constructed model. 

## Constructing a Proof

The derivation system is designed to be sound and complete. Hence, any mathematical proof could in-principle be translated into this system and checked for validity. 

The derivation system is a natural deduction system for first-order logic with identity. One will first be asked to state the premises. One will then be asked to apply inference rules. One can always input "Exit" to exit the program. 

Proofs will be printed as follows: 

0    (P(a) ^ P(b))  
1    P(c)  
\_______________

2    P(a)  
3    (P(a) ^ P(c))  
4    | Q(d)  
5    | (P(a) ^ P(c))  
6  
7    (Q(d) > (P(a) ^ P(c))

Here, lines 0 and 1 are premises. Line 4 begins a subproof. Line 6 ends the subproof. Line 7 is the desired conclusion. 

Separate premises with commas. If no input is given, the proof will proceed without premises. The rest of the system consists of applying inference rules. The following commands can be used at any point: 

Exit - Exit the program.

Delete - Remove the last line of the proof.

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

\>E,n,m - Apply Conditional Elimination to the conditional at line m using its antecendent at line n. 

\>I,n-m - Apply Conditional Introduction to the subproof from line n to m. 

~E,n - Apply Negation Elimination to the double negation at line n. 

~I,n-m - Apply Negation Introduction to the subformula from line n to m. The formula at line m must be F. 

-ER,n,m - Apply Biconditional Elimination to the formula at line n using the left subformula at line m, outputting the right subformula. 

-EL,n,m - Apply Biconditional Elimination to the formula at line n using the right subformula at line m, outputting the left subformula. 

-I,k-l,m-n - Apply Biconditional Introduction using the formulas from k to l and m to n. The formula at k must be identical to the formula at n and the formula at l must be identical to the formula at m. 

=I,c - Apply Identity Introduction with constant c, outputting =(c,c). 

=E,n,m - Apply Identity Elimination using the identity at line n and replacing instances of the first constant by the second at line m. 

XI,n,c,x - Apply Existential Introduction to the formula at line n, replacing each instance of constant c by variable x. 

XE,k,n,m,c - Apply Existential Elimination to the existentially-quantified formula at line k and the subproof beginning at n and ending at m. The formula at line n must be the subformula of the formula at line k with the free instances of its variable replaced by the constant c. This constant must not appear earlier in the proof, nor can it be in the formula at line m. The formula at line m will be outputted. 

UE,n,c - Apply Universal Elimination to the formula at line n, replacing each free instance of its variable with the constant c. 

UI,n,c,x - Apply Universal Introduction to the formula at line n, replacing each instance of constant c by variable x. Constant c cannot appear in a premise or an active assumption. 

## A Proof that the Uniform Continuity of a Real Function Implies its Continuity at p

Here without loss of generality I don't bother assuming that the function always produces a unique output (i.e. is well-defined). H(r,s) means that function H outputs s on input r. L(x,y,e) means that the distance between x and y is less than e. 

0     UeXdUxUy(L(x,y,d) > XuXv((H(x,u) ^ H(y,v)) ^ L(u,v,e)))  - premise  
\_________________
 
1      XdUxUy(L(x,y,d) > XuXv((H(x,u) ^ H(y,v)) ^ L(u,v,e1)))  - UE,0,e1  
2     | UxUy(L(x,y,d1) > XuXv((H(x,u) ^ H(y,v)) ^ L(u,v,e1)))  - Assume,UxUy(L(x,y,d1) > XuXv((H(x,u) ^ H(y,v)) ^ L(u,v,e1)))  
3     | Uy(L(r,y,d1) > XuXv((H(r,u) ^ H(y,v)) ^ L(u,v,e1)))    - UE,2,r  
4     | (L(r,p,d1) > XuXv((H(r,u) ^ H(p,v)) ^ L(u,v,e1)))      - UE,3,p  
5     | Xd(L(r,p,d) > XuXv((H(r,u) ^ H(p,v)) ^ L(u,v,e1)))     - XI,4,d1,d  
6       
7      Xd(L(r,p,d) > XuXv((H(r,u) ^ H(p,v)) ^ L(u,v,e1)))      - XE,1,2,5,d1  
8      UxXd(L(x,p,d) > XuXv((H(x,u) ^ H(p,v)) ^ L(u,v,e1)))    - UI,7,r,x  
9      UeUxXd(L(x,p,d) > XuXv((H(x,u) ^ H(p,v)) ^ L(u,v,e)))   - UI,8,e1,e  

Theorem: If UeXdUxUy(L(x,y,d) > XuXv((H(x,u) ^ H(y,v)) ^ L(u,v,e))) then UeUxXd(L(x,p,d) > XuXv((H(x,u) ^ H(p,v)) ^ L(u,v,e))).

Some rules can currently be used in nonstandard ways, but the system should remain sound. Finding any violations of soundness would be greatly appreciated. 
