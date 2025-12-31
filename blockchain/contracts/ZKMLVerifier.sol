// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

// Verifier.sol ফাইলটিকে ইমপোর্ট করা হচ্ছে
import "./Verifier.sol";

contract ZKMLVerifier {
    // আপনার ফাইলের কন্ট্রাক্ট নাম 'Groth16Verifier', তাই এখানে সেটিই ব্যবহার করতে হবে
    Groth16Verifier public verifier;

    constructor(address _verifier) {
        // ডিক্লেয়ার করা এড্রেসকে Groth16Verifier টাইপে কনভার্ট করা হচ্ছে
        verifier = Groth16Verifier(_verifier);
    }

    /**
     * @dev ML ইনফারেন্স ভেরিফাই করার ফাংশন
     * @param a Proof পার্ট A
     * @param b Proof পার্ট B
     * @param c Proof পার্ট C
     * @param input পাবলিক সিগন্যাল (যেমন: ML Prediction 0 বা 1)
     */
    function verifyMLInference(
        uint[2] memory a,
        uint[2][2] memory b,
        uint[2] memory c,
        uint[1] memory input
    ) public view returns (bool) {
        // Groth16Verifier কন্ট্রাক্টের verifyProof ফাংশনকে কল করা হচ্ছে
        return verifier.verifyProof(a, b, c, input);
    }
}