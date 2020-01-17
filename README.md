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

Separate premises with commas. If no input is given, the proof will proceed without premises. The rest of the system consists of applying inference rules. The following commands can be used at any point: 

Exit - Exit the program

delete - remove the last line of the proof

Finish - Output the theorem proved

The following commands are the basic inference rules: 

