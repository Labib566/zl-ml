1.1 Model Selection Rationale
Objective

The goal of the machine learning model is to compute a binary decision
(e.g., approve / reject) based on a fixed-size feature vector, under the following constraints:

Deterministic inference

Compatibility with arithmetic circuits

Low multiplicative depth

Bounded numeric range

Efficient zero-knowledge proof generation

Given these constraints, we select a linear classification model with a sigmoid decision boundary, equivalent to logistic regression.

Why Logistic Regression?
Criterion	Justification
Determinism	Fully deterministic at inference time
Arithmetic Simplicity	Linear operations + sigmoid approximation
ZK Compatibility	Low-degree polynomial approximation
Explainability	Feature weights are interpretable
Constraint Efficiency	Minimal circuit depth

Note: Training complexity is irrelevant for ZK.
Only inference complexity matters.

1.2 Feature Space Definition

Let the input feature vector be:

𝑥
=
(
𝑥
1
,
𝑥
2
,
…
,
𝑥
𝑛
)
∈
𝑅
𝑛
x=(x
1
	​

,x
2
	​

,…,x
n
	​

)∈R
n

Where:

𝑛
n is fixed at compile time

All features are normalized and bounded

Feature Constraints

Each feature satisfies:

𝑥
𝑖
∈
[
𝑥
min
⁡
,
𝑥
max
⁡
]
x
i
	​

∈[x
min
	​

,x
max
	​

]

These bounds are enforced during input preprocessing and validated before proof generation.

1.3 Fixed-Point Numeric Representation (CRITICAL)
Motivation

Zero-knowledge circuits do not support floating-point arithmetic.
Therefore, all real-valued computations must be represented using fixed-point integers.

Fixed-Point Encoding

Let:

scaling factor 
𝑆
=
2
𝑘
S=2
k
, where 
𝑘
∈
𝑁
k∈N

A real value 
𝑥
x is encoded as:

𝑥
^
=
⌊
𝑥
⋅
𝑆
⌉
x
^
=⌊x⋅S⌉

Similarly, model weights 
𝑤
𝑖
w
i
	​

 and bias 
𝑏
b are encoded as:

𝑤
^
𝑖
=
⌊
𝑤
𝑖
⋅
𝑆
⌉
,
𝑏
^
=
⌊
𝑏
⋅
𝑆
⌉
w
^
i
	​

=⌊w
i
	​

⋅S⌉,
b
^
=⌊b⋅S⌉

All arithmetic inside the circuit operates on integer values 
𝑥
^
,
𝑤
^
,
𝑏
^
x
^
,
w
^
,
b
^
.

Overflow Bound Analysis

Let:

𝑛
n = number of features

𝑀
𝑥
M
x
	​

 = max absolute feature value

𝑀
𝑤
M
w
	​

 = max absolute weight value

The maximum linear sum magnitude is:

∣
∑
𝑖
=
1
𝑛
𝑤
^
𝑖
⋅
𝑥
^
𝑖
∣
≤
𝑛
⋅
(
𝑀
𝑤
𝑆
)
⋅
(
𝑀
𝑥
𝑆
)
∣
i=1
∑
n
	​

w
^
i
	​

⋅
x
^
i
	​

∣≤n⋅(M
w
	​

S)⋅(M
x
	​

S)

This bound must be strictly less than the field modulus of the zkSNARK system.

This bound will later dictate our circuit field choice and scaling factor.

1.4 Formal Inference Equation
Linear Combination

The pre-activation value is computed as:

𝑧
=
∑
𝑖
=
1
𝑛
𝑤
𝑖
𝑥
𝑖
+
𝑏
z=
i=1
∑
n
	​

w
i
	​

x
i
	​

+b

In fixed-point form:

𝑧
^
=
∑
𝑖
=
1
𝑛
𝑤
^
𝑖
⋅
𝑥
^
𝑖
+
𝑏
^
⋅
𝑆
z
^
=
i=1
∑
n
	​

w
^
i
	​

⋅
x
^
i
	​

+
b
^
⋅S

Note: One additional multiplication by 
𝑆
S is introduced to preserve scale consistency.

Sigmoid Approximation

The logistic sigmoid function:

𝜎
(
𝑧
)
=
1
1
+
𝑒
−
𝑧
σ(z)=
1+e
−z
1
	​


is not directly computable inside a ZK circuit.

Therefore, we approximate it using a low-degree polynomial:

𝜎
(
𝑧
)
≈
𝑃
(
𝑧
)
=
𝑎
0
+
𝑎
1
𝑧
+
𝑎
3
𝑧
3
σ(z)≈P(z)=a
0
	​

+a
1
	​

z+a
3
	​

z
3

Where coefficients 
𝑎
0
,
𝑎
1
,
𝑎
3
a
0
	​

,a
1
	​

,a
3
	​

 are precomputed constants.

Polynomial degree is chosen to balance:

approximation error

constraint complexity

Final Decision Rule

Let the output probability be:

𝑦
^
=
𝑃
(
𝑧
^
)
y
^
	​

=P(
z
^
)

The binary decision is defined as:

decision
=
{
1
	
if 
𝑦
^
≥
𝜏


0
	
otherwise
decision={
1
0
	​

if 
y
^
	​

≥τ
otherwise
	​


Where:

𝜏
τ is a fixed threshold encoded in fixed-point form.

1.5 Determinism Guarantee

The model guarantees determinism because:

All operations are integer arithmetic

No randomness is used

All parameters are fixed at compile time

Therefore:

∀
𝑥
,
𝑓
(
𝑥
)
 produces a unique output
∀x,f(x) produces a unique output

This property is mandatory for sound zero-knowledge verification.

1.6 Public vs Private Values
Component	Visibility
Input features	Private
Model weights	Private
Bias	Private
Threshold 
𝜏
τ	Public
Decision output	Public
Zero-knowledge proof	Public

This separation ensures:

model confidentiality,

user privacy,

public verifiability.

1.7 Phase 1 Deliverables (Checklist)

✅ Formal model selection rationale
✅ Fixed-point numeric system
✅ Overflow bounds
✅ Formal inference equation
✅ Sigmoid approximation strategy
✅ Determinism proof

👉 PHASE 1 COMPLETE