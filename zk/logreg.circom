pragma circom 2.1.6;

include "circomlib/circuits/comparators.circom";

template LogisticRegression() {

    signal input x[3];     // private input
    signal output y;       // public output (0 or 1)

    var w[3] = [6247, -4899, 2851];
    var b = 20;

    signal z;

    // Linear combination
    z <== x[0]*w[0] + x[1]*w[1] + x[2]*w[2] + b;

    // Comparator: z > 0
    component gt = GreaterThan(32);  // 32-bit comparison
    gt.in[0] <== z;
    gt.in[1] <== 0;

    y <== gt.out;
}

component main = LogisticRegression();